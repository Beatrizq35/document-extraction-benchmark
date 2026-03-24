from __future__ import annotations

import os
from pathlib import Path

import pytest

from document_extraction_benchmark.main import run_evaluation

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PDF = ROOT / "dataset" / "sample.pdf"


@pytest.fixture
def sample_pdf() -> Path:
    if not SAMPLE_PDF.is_file():
        pytest.skip(f"Missing {SAMPLE_PDF}")
    return SAMPLE_PDF


def test_pypdf_run_evaluation(sample_pdf: Path) -> None:
    report = run_evaluation("pypdf", str(sample_pdf), repeat=1, warmup=0)
    assert report["lib"] == "pypdf"
    assert report["criteria"]["output"]["text_char_count"] > 0
    assert report["criteria"]["speed"]["runs"] == 1


def test_pdfminer_run_evaluation(sample_pdf: Path) -> None:
    pytest.importorskip("pdfminer")
    report = run_evaluation("pdfminer", str(sample_pdf))
    assert report["lib"] == "pdfminer"
    assert report["criteria"]["output"]["text_char_count"] > 0


@pytest.mark.skipif(
    os.environ.get("RUN_DOCLING_SMOKE") != "1",
    reason="Docling downloads layout models on first run; set RUN_DOCLING_SMOKE=1 to enable.",
)
def test_docling_run_evaluation(sample_pdf: Path) -> None:
    pytest.importorskip("docling")
    report = run_evaluation("docling", str(sample_pdf), repeat=1, warmup=0)
    assert report["lib"] == "docling"
    assert report["criteria"]["output"]["text_char_count"] > 0
