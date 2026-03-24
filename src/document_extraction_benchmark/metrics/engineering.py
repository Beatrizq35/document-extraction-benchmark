from __future__ import annotations

# Qualitative rubrics for IC reporting. Values are suggestions — revise after hands-on review.
_ENGINEERING_RUBRICS: dict[str, dict[str, str]] = {
    "docling": {
        "extraction_engine": "hybrid_ml_layout",
        "pdf_type_support": "text_native_ocr_optional",
        "installation_complexity": "heavy_ml_stack",
        "api_design": "high_level_converter_exports",
        "extensibility": "pipeline_options_plugins",
    },
    "pymupdf": {
        "extraction_engine": "native_c_text_vector",
        "pdf_type_support": "text_native_ocr_separate",
        "installation_complexity": "easy_wheel",
        "api_design": "low_level_page_objects",
        "extensibility": "good_centric_document_model",
    },
    "pdfplumber": {
        "extraction_engine": "rule_based_pdfminer_wrapped",
        "pdf_type_support": "text_based",
        "installation_complexity": "easy",
        "api_design": "page_centric_pythonic",
        "extensibility": "moderate_hooks",
    },
    "pdfminer": {
        "extraction_engine": "rule_based_parser_layout_analysis",
        "pdf_type_support": "text_based",
        "installation_complexity": "easy",
        "api_design": "verbose_low_level",
        "extensibility": "high_fine_grained",
    },
    "pypdf": {
        "extraction_engine": "rule_based_python_pure",
        "pdf_type_support": "text_based",
        "installation_complexity": "easy",
        "api_design": "simple_reader_writer",
        "extensibility": "moderate",
    },
}


def evaluate_engineering(lib_label: str) -> dict:
    rubric = _ENGINEERING_RUBRICS.get(lib_label)
    if rubric is None:
        return {
            "manual_review_required": True,
            "rubric": None,
            "note": f"No static rubric for {lib_label!r}; extend metrics/engineering.py.",
        }
    return {
        "manual_review_required": False,
        "rubric": rubric,
        "note": "Static labels for reporting; validate against docs and your experiments.",
    }
