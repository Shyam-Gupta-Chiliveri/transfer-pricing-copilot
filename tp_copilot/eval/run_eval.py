"""Citation accuracy: is an accepted paragraph inside the top 3 hits?"""

from __future__ import annotations

from tp_copilot.eval.questions import QUESTIONS
from tp_copilot.retrieval.store import get_store


def run_eval(k: int = 3) -> dict:
    store = get_store()
    rows = []
    hits = 0
    for item in QUESTIONS:
        found = store.search(item["question"], k=k)
        paragraphs = [hit["paragraph"] for hit in found]
        ok = any(paragraph in paragraphs for paragraph in item["accept"])
        hits += int(ok)
        rows.append(
            {
                "id": item["id"],
                "ok": ok,
                "accept": item["accept"],
                "got": paragraphs,
                "question": item["question"],
            }
        )
    total = len(QUESTIONS)
    return {
        "k": k,
        "hits": hits,
        "total": total,
        "accuracy": hits / total if total else 0.0,
        "rows": rows,
    }
