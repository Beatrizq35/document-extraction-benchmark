from __future__ import annotations

from document_extraction_benchmark.metrics.accuracy import evaluate_accuracy
from document_extraction_benchmark.models import ExtractionResult


def test_accuracy_skipped_without_ground_truth() -> None:
    r = evaluate_accuracy(ExtractionResult(text="x"), None)
    assert r["status"] == "skipped"


def test_accuracy_with_ground_truth(tmp_path) -> None:
    gt = tmp_path / "expected.txt"
    gt.write_text("hello world\n", encoding="utf-8")
    r = evaluate_accuracy(ExtractionResult(text="hello world"), str(gt))
    assert r["status"] == "ok"
    assert r["similarity_ratio_rough"] == 1.0
