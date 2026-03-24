from __future__ import annotations

from document_extraction_benchmark.evaluators.base import BaseEvaluator

_REGISTRY_KEYS = ("docling", "pymupdf", "pdfplumber", "pdfminer", "pypdf")


def normalize_lib(name: str) -> str:
    n = name.strip().lower()
    if n in ("pdfminer.six", "pdfminer_six"):
        return "pdfminer"
    return n


def list_supported_libs() -> list[str]:
    return sorted(_REGISTRY_KEYS)


def get_evaluator(lib_name: str, file_path: str) -> BaseEvaluator:
    key = normalize_lib(lib_name)
    if key == "docling":
        from document_extraction_benchmark.evaluators.docling import DoclingEvaluator

        return DoclingEvaluator(file_path)
    if key == "pymupdf":
        from document_extraction_benchmark.evaluators.pymupdf_eval import PyMuPDFEvaluator

        return PyMuPDFEvaluator(file_path)
    if key == "pdfplumber":
        from document_extraction_benchmark.evaluators.pdfplumber_eval import PDFPlumberEvaluator

        return PDFPlumberEvaluator(file_path)
    if key == "pdfminer":
        from document_extraction_benchmark.evaluators.pdfminer_eval import PdfminerEvaluator

        return PdfminerEvaluator(file_path)
    if key == "pypdf":
        from document_extraction_benchmark.evaluators.pypdf_eval import PypdfEvaluator

        return PypdfEvaluator(file_path)

    supported = ", ".join(list_supported_libs())
    raise ValueError(f"Unsupported lib {lib_name!r}. Choose one of: {supported}")
