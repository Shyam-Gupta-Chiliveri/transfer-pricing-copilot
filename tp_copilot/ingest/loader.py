"""Load study notes plus any local files in data/regelwerke/."""

from __future__ import annotations

from pathlib import Path

from tp_copilot.ingest.chunker import chunk_file
from tp_copilot.knowledge.notes import NOTES

ROOT = Path(__file__).resolve().parents[2]
REGELWERKE = ROOT / "data" / "regelwerke"
SKIP_NAMES = {"PLACE_OFFICIAL_FILES_HERE.txt"}


def load_chunks() -> list[dict]:
    chunks = [dict(note) for note in NOTES]
    if not REGELWERKE.exists():
        return chunks
    for path in sorted(REGELWERKE.iterdir()):
        if not path.is_file() or path.name in SKIP_NAMES or path.name.startswith("."):
            continue
        if path.suffix.lower() not in {".pdf", ".txt", ".xml", ".md"}:
            continue
        try:
            chunks.extend(chunk_file(path))
        except Exception:
            continue
    return chunks
