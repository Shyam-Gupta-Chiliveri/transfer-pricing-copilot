"""Retrieve study notes and compose a cited answer without an external LLM."""

from __future__ import annotations

from tp_copilot.retrieval.store import RegelwerkStore, get_store

_GERMAN = (
    " und ", " der ", " die ", " das ", " ist ", " wie ", " welche ", " warum ",
    " wann ", " nicht ", " nach ", " bei ", " eine ", " einem ", "§",
)


def is_german(question: str) -> bool:
    padded = f" {question.lower()} "
    hits = sum(1 for token in _GERMAN if token in padded)
    return hits >= 2


def _cite(hit: dict) -> str:
    return f"{hit['source']} {hit['paragraph']}"


def answer_question(
    question: str,
    k: int = 4,
    lang: str | None = None,
    extra_chunks: list[dict] | None = None,
) -> dict:
    if extra_chunks:
        store = RegelwerkStore(get_store().chunks + list(extra_chunks))
    else:
        store = get_store()
    hits = store.search(question, k=k)
    if lang in ("de", "en"):
        german = lang == "de"
    else:
        german = is_german(question)
    if not hits:
        empty = "Keine passende Stelle gefunden." if german else "No matching passage found."
        return {"answer": empty, "citations": [], "hits": [], "language": "de" if german else "en"}

    primary = hits[0]
    body = primary["text_de"] if german else primary["text_en"]
    lines = [body.strip(), "", ("Belege:" if german else "Sources:")]
    citations = []
    for hit in hits:
        citations.append(
            {
                "source": hit["source"],
                "paragraph": hit["paragraph"],
                "title": hit["title"],
                "score": hit["score"],
            }
        )
        lines.append(f"- {_cite(hit)} — {hit['title']}")

    other = [hit for hit in hits[1:] if hit["source_id"] != primary["source_id"]]
    if other:
        extra = other[0]
        label = "Abgrenzung zu einer anderen Quelle:" if german else "Contrast with another source:"
        extra_body = extra["text_de"] if german else extra["text_en"]
        lines.extend(["", label, extra_body.strip()])

    lines.extend(
        [
            "",
            (
                "Dies ist eine Studienantwort für ein Portfolio, keine steuerliche Beratung."
                if german
                else "This is a portfolio study answer, not tax advice."
            ),
        ]
    )
    return {
        "answer": "\n".join(lines),
        "citations": citations,
        "hits": hits,
        "language": "de" if german else "en",
    }
