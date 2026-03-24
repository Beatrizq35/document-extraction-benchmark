from __future__ import annotations

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


class DoclingEvaluator(BaseEvaluator):
    distribution_name = "docling"
    lib_label = "docling"
    supports_tables = True
    supports_layout = True

    def extract(self) -> ExtractionResult:
        # Lazy imports: avoid loading docling/torch when using other backends.
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractOcrOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.ocr_options = TesseractOcrOptions()
        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )
        conv = converter.convert(self.file_path)
        doc = conv.document

        text = doc.export_to_text() or ""
        markdown = doc.export_to_markdown() or ""
        structured = doc.export_to_dict()
        layout_blocks: list[dict] = []
        tables: list[list[list[str]]] = []

        def walk(node: object, depth: int = 0) -> None:
            if isinstance(node, list):
                for item in node:
                    walk(item, depth)
                return
            if not isinstance(node, dict):
                return
            label = node.get("label") or node.get("type") or "node"
            text_content = node.get("text")
            prov = node.get("prov") or []
            bbox = None
            if prov and isinstance(prov, list) and prov and isinstance(prov[0], dict):
                b = prov[0].get("bbox")
                if b is not None:
                    bbox = b
            if text_content and isinstance(text_content, str) and text_content.strip():
                layout_blocks.append(
                    {
                        "type": str(label),
                        "text": text_content.strip()[:5000],
                        "depth": depth,
                        "bbox": bbox,
                    }
                )
            if str(label).lower() == "table" and isinstance(text_content, str):
                row_lines = [ln.strip() for ln in text_content.splitlines() if ln.strip()]
                if row_lines:
                    split_rows = [r.split("|") if "|" in r else r.split() for r in row_lines]
                    if split_rows:
                        tables.append([[c.strip() for c in row] for row in split_rows])
            for child in node.get("children") or []:
                walk(child, depth + 1)

        walk(structured)

        notes: list[str] = [
            "Docling tables in ExtractionResult are best-effort from document tree / text; "
            "use structured_dict for full structure."
        ]
        return ExtractionResult(
            text=text,
            tables=tables,
            layout_blocks=layout_blocks,
            metadata={
                "page_count": getattr(doc, "num_pages", None),
                "export_formats": ["text", "markdown", "dict"],
            },
            output_notes=notes,
            markdown=markdown,
            structured_dict=structured,
        )
