"""TF-IDF retriever with keyword and paragraph boosts.

The materials project stored ISO chunks in Qdrant. This project keeps the same
contract — chunk, metadata, top-k, citation — and runs locally so a recruiter
can start it without a vector database. Collection name: tp_regelwerke.
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from tp_copilot.ingest.loader import load_chunks

COLLECTION = "tp_regelwerke"

# Questions that name two ideas should open the note that compares them.
INTENT_BOOSTS: tuple[tuple[tuple[str, ...], str, float], ...] = (
    (("tnmm", "cost plus"), "oecd-tnmm-vs-costplus", 1.8),
    (("profit split", "one-sided"), "oecd-2.119", 1.2),
    (("profit split", "routine"), "oecd-2.119", 1.2),
    (("interquartile", "outside"), "astg-1-3a", 0.8),
    (("transfer package", "only"), "astg-1-3b", 0.9),
    (("transferpaket",), "astg-1-3b", 0.6),
)


class RegelwerkStore:
    def __init__(self, chunks: list[dict] | None = None):
        self.chunks = chunks if chunks is not None else load_chunks()
        corpus = [
            "\n".join(
                [
                    chunk["title"],
                    chunk["paragraph"],
                    chunk["source"],
                    " ".join(chunk["keywords"]),
                    chunk["text_en"],
                    chunk["text_de"],
                ]
            )
            for chunk in self.chunks
        ]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query: str, k: int = 4) -> list[dict]:
        if not query.strip() or not self.chunks:
            return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        query_lower = query.lower()
        for index, chunk in enumerate(self.chunks):
            paragraph = chunk["paragraph"].lower()
            if paragraph and paragraph in query_lower:
                scores[index] += 1.25
            for keyword in chunk["keywords"]:
                if keyword.lower() in query_lower:
                    scores[index] += 0.55
            source_id = chunk["source_id"]
            if source_id == "astg" and "astg" in query_lower:
                scores[index] += 0.2
            if source_id == "oecd" and "oecd" in query_lower:
                scores[index] += 0.12
            if source_id == "ao" and ("transaktionsmatrix" in query_lower or "§ 90" in query_lower or "ao" in query_lower):
                scores[index] += 0.25
            if source_id == "vwg" and "verwaltungsgrund" in query_lower:
                scores[index] += 0.35
            for needles, note_id, boost in INTENT_BOOSTS:
                if chunk["id"] == note_id and all(needle in query_lower for needle in needles):
                    scores[index] += boost
        order = scores.argsort()[::-1][:k]
        hits = []
        for index in order:
            if scores[index] <= 0:
                continue
            chunk = self.chunks[index]
            hits.append(
                {
                    "id": chunk["id"],
                    "source": chunk["source"],
                    "source_id": chunk["source_id"],
                    "paragraph": chunk["paragraph"],
                    "title": chunk["title"],
                    "text_en": chunk["text_en"],
                    "text_de": chunk["text_de"],
                    "score": round(float(scores[index]), 4),
                    "collection": COLLECTION,
                }
            )
        return hits


_STORE: RegelwerkStore | None = None


def get_store() -> RegelwerkStore:
    global _STORE
    if _STORE is None:
        _STORE = RegelwerkStore()
    return _STORE
