"""Knowledge-graph specialist."""

from __future__ import annotations

from tp_copilot.knowledge.graph import query_graph


def run_kg(question: str, max_edges: int = 8) -> dict:
    return query_graph(question, max_edges=max_edges)
