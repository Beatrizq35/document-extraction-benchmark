from __future__ import annotations

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams, LTTextBox

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


class PdfminerEvaluator(BaseEvaluator):
    distribution_name = "pdfminer.six"
    lib_label = "pdfminer"
    supports_tables = False
    supports_layout = True

    def extract(self) -> ExtractionResult:
        text = extract_text(self.file_path) or ""
        layout_blocks: list[dict] = []
        notes: list[str] = []
        laparams = LAParams()
        page_index = 0
        try:
            for page_layout in extract_pages(self.file_path, laparams=laparams):
                for element in page_layout:
                    if isinstance(element, LTTextBox):
                        layout_blocks.append(
                            {
                                "type": "textbox",
                                "page": page_index,
                                "text": element.get_text().strip(),
                                "bbox": (
                                    float(element.x0),
                                    float(element.y0),
                                    float(element.x1),
                                    float(element.y1),
                                ),
                            }
                        )
                page_index += 1
        except Exception as exc:
            notes.append(f"layout_extraction_partial: {exc!s}")

        return ExtractionResult(
            text=text,
            tables=[],
            layout_blocks=layout_blocks,
            metadata={"page_count": page_index},
            output_notes=notes
            + [
                "pdfminer.six has no dedicated table API; "
                "tables metric reflects heuristics only."
            ],
        )
