from __future__ import annotations

from document_extraction_benchmark.models import ExtractionResult


def evaluate_output(result: ExtractionResult) -> dict:
    """Describe primary outputs (text, optional markdown / structured dict)."""
    structured = result.structured_dict
    structured_keys: list[str] | None = None
    structured_size: int | None = None
    if structured is not None:
        structured_keys = list(structured.keys()) if isinstance(structured, dict) else None
        structured_size = len(str(structured))

    return {
        "text_type": type(result.text).__name__,
        "text_char_count": len(result.text or ""),
        "text_line_count": len((result.text or "").splitlines()),
        "has_markdown_export": result.markdown is not None,
        "markdown_char_count": len(result.markdown or ""),
        "has_structured_dict": result.structured_dict is not None,
        "structured_top_level_keys": structured_keys,
        "structured_serialized_length": structured_size,
        "output_notes": list(result.output_notes),
    }
