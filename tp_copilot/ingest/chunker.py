"""Split guideline text on paragraph numbers or statute sections.

Official OECD PDFs are not shipped in this repository. This chunker runs when
a local file is placed in data/regelwerke/.
"""

from __future__ import annotations

import re
from pathlib import Path

OECD_PARA = re.compile(r"(?m)(?:^|\n)\s*(\d{1,2}\.\d{1,3})\.\s+")
SECTION = re.compile(r"(?m)(?:^|\n)\s*§\s*(\d+[a-z]?)")


def chunk_paragraphs(text: str, source: str) -> list[dict]:
    """Split OECD-style '1.33. ...' text. Each chunk keeps its paragraph id."""
    matches = list(OECD_PARA.finditer(text))
    if not matches:
        return []
    chunks: list[dict] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if len(body) < 40:
            continue
        paragraph = match.group(1)
        chunks.append(
            {
                "id": f"file-{source}-{paragraph}",
                "source": source,
                "source_id": "oecd-file",
                "paragraph": paragraph,
                "title": f"{source} para. {paragraph}",
                "keywords": [paragraph, source],
                "text_en": body[:1800],
                "text_de": body[:1800],
            }
        )
    return chunks


def chunk_statute(text: str, source: str) -> list[dict]:
    matches = list(SECTION.finditer(text))
    if not matches:
        return []
    chunks: list[dict] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if len(body) < 40:
            continue
        section = f"§ {match.group(1)}"
        chunks.append(
            {
                "id": f"file-{source}-{match.group(1)}",
                "source": source,
                "source_id": "statute-file",
                "paragraph": section,
                "title": f"{source} {section}",
                "keywords": [section, source],
                "text_en": body[:1800],
                "text_de": body[:1800],
            }
        )
    return chunks


def chunk_file(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _read_pdf(path)
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")
    return chunks_from_text(text, path.stem)


def chunks_from_bytes(filename: str, data: bytes) -> list[dict]:
    """Index an uploaded PDF or text file. Nothing is written to disk."""
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        text = _read_pdf_bytes(data)
    else:
        text = data.decode("utf-8", errors="ignore")
    return chunks_from_text(text, Path(filename).stem or "upload")


def chunks_from_text(text: str, source: str) -> list[dict]:
    paragraphs = chunk_paragraphs(text, source)
    if paragraphs:
        return paragraphs
    sections = chunk_statute(text, source)
    if sections:
        return sections
    if len(text.strip()) < 40:
        return []
    return [
        {
            "id": f"file-{source}",
            "source": source,
            "source_id": "file",
            "paragraph": source,
            "title": source,
            "keywords": [source],
            "text_en": text.strip()[:1800],
            "text_de": text.strip()[:1800],
        }
    ]


def _read_pdf(path: Path) -> str:
    return _read_pdf_bytes(path.read_bytes())


def _read_pdf_bytes(data: bytes) -> str:
    from io import BytesIO

    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    return "\n".join((page.extract_text() or "") for page in reader.pages)
