from __future__ import annotations

import pdfplumber

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


def _normalize_table(table: list[list[str | None]] | None) -> list[list[str]]:
    if not table:
        return []
    return [[("" if c is None else str(c)) for c in row] for row in table]


class PDFPlumberEvaluator(BaseEvaluator):
    distribution_name = "pdfplumber"
    lib_label = "pdfplumber"
    supports_tables = True
    supports_layout = True

    def extract(self) -> ExtractionResult:
        text_parts: list[str] = []
        layout_blocks: list[dict] = []
        tables: list[list[list[str]]] = []

        with pdfplumber.open(self.file_path) as pdf:
            page_count = len(pdf.pages)
            for page_index, page in enumerate(pdf.pages):
                text_parts.append(page.extract_text() or "")
                for table in page.extract_tables() or []:
                    tnorm = _normalize_table(table)
                    if tnorm:
                        tables.append(tnorm)
                for word in page.extract_words() or []:
                    layout_blocks.append(
                        {
                            "type": "word",
                            "page": page_index,
                            "text": word.get("text", ""),
                            "bbox": (
                                float(word["x0"]),
                                float(word["top"]),
                                float(word["x1"]),
                                float(word["bottom"]),
                            ),
                        }
                    )

        return ExtractionResult(
            text="\n".join(text_parts),
            tables=tables,
            layout_blocks=layout_blocks,
            metadata={"page_count": page_count},
            output_notes=[],
        )
