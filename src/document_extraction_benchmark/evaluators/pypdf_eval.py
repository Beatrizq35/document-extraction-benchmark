from __future__ import annotations

from pypdf import PdfReader

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


class PypdfEvaluator(BaseEvaluator):
    distribution_name = "pypdf"
    lib_label = "pypdf"
    supports_tables = False
    supports_layout = False

    def extract(self) -> ExtractionResult:
        reader = PdfReader(self.file_path)
        parts: list[str] = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text() or ""
            parts.append(t)
        text = "\n".join(parts)
        meta: dict = {"page_count": len(reader.pages)}
        if reader.metadata:
            meta["document_metadata_keys"] = [k for k in reader.metadata.keys() if k is not None]
        notes: list[str] = [
            "pypdf: no table detection or per-block geometry in the high-level API used here."
        ]
        return ExtractionResult(
            text=text,
            tables=[],
            layout_blocks=[],
            metadata=meta,
            output_notes=notes,
        )
