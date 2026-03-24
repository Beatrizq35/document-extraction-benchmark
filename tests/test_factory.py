from __future__ import annotations

import pytest

from document_extraction_benchmark.evaluators.factory import (
    get_evaluator,
    list_supported_libs,
    normalize_lib,
)


def test_normalize_pdfminer_alias() -> None:
    assert normalize_lib("pdfminer.six") == "pdfminer"
    assert normalize_lib("PDFMINER.SIX") == "pdfminer"


def test_list_supported_libs_sorted() -> None:
    libs = list_supported_libs()
    assert libs == sorted(libs)
    assert "pypdf" in libs


def test_factory_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unsupported"):
        get_evaluator("not-a-real-lib", "dummy.pdf")
