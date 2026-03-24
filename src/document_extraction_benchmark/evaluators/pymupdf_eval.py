from __future__ import annotations

import pymupdf

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


def _normalize_table(rows: list | None) -> list[list[str]]:
    if not rows:
        return []
    out: list[list[str]] = []
    for row in rows:
        if row is None:
            continue
        out.append(["" if c is None else str(c) for c in row])
    return out


class PyMuPDFEvaluator(BaseEvaluator):
    distribution_name = "pymupdf"
    lib_label = "pymupdf"
    supports_tables = True
    supports_layout = True

    def extract(self) -> ExtractionResult:
        doc = pymupdf.open(self.file_path)
        notes: list[str] = []
        text_parts: list[str] = []
        layout_blocks: list[dict] = []
        tables: list[list[list[str]]] = []

        try:
            for page_index in range(len(doc)):
                page = doc[page_index]
                text_parts.append(page.get_text() or "")
                d = page.get_text("dict")
                for block in d.get("blocks", []):
                    if block.get("type") != 0:
                        continue
                    bbox = block.get("bbox")
                    for line in block.get("lines", []):
                        spans_text = "".join(
                            s.get("text", "") for s in line.get("spans", [])
                        ).strip()
                        if not spans_text:
                            continue
                        lb = line.get("bbox")
                        layout_blocks.append(
                            {
                                "type": "line",
                                "page": page_index,
                                "text": spans_text,
                                "bbox": tuple(float(x) for x in lb) if lb else None,
                                "block_bbox": tuple(float(x) for x in bbox) if bbox else None,
                            }
                        )
                try:
                    tf = page.find_tables()
                    tab_list = getattr(tf, "tables", None)
                    if tab_list is None:
                        tab_list = list(tf) if hasattr(tf, "__iter__") else []
                    for tab in tab_list:
                        extract_fn = getattr(tab, "extract", None)
                        raw = extract_fn() if callable(extract_fn) else None
                        tnorm = _normalize_table(raw)
                        if tnorm:
                            tables.append(tnorm)
                except Exception as exc:  # pragma: no cover - version/API differences
                    notes.append(f"find_tables_failed_page_{page_index}: {exc!s}")
        finally:
            doc.close()

        text = "\n".join(text_parts)
        return ExtractionResult(
            text=text,
            tables=tables,
            layout_blocks=layout_blocks,
            metadata={"page_count": len(text_parts)},
            output_notes=notes,
        )
