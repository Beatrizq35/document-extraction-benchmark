from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from document_extraction_benchmark.evaluators.factory import get_evaluator, list_supported_libs
from document_extraction_benchmark.metrics.accuracy import evaluate_accuracy
from document_extraction_benchmark.metrics.complexity import evaluate_complexity
from document_extraction_benchmark.metrics.dependencies import evaluate_dependencies
from document_extraction_benchmark.metrics.engineering import evaluate_engineering
from document_extraction_benchmark.metrics.layout import evaluate_layout
from document_extraction_benchmark.metrics.output import evaluate_output
from document_extraction_benchmark.metrics.speed import evaluate_speed
from document_extraction_benchmark.metrics.tables import evaluate_tables
from document_extraction_benchmark.reporting import group_by_category


def run_evaluation(
    lib: str,
    file_path: str,
    *,
    repeat: int = 1,
    warmup: int = 0,
    ground_truth: str | None = None,
) -> dict[str, Any]:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    evaluator = get_evaluator(lib, str(path.resolve()))
    for _ in range(max(0, warmup)):
        evaluator.extract()

    timings: list[float] = []
    result = None
    runs = max(1, repeat)
    for _ in range(runs):
        t0 = time.perf_counter()
        result = evaluator.extract()
        timings.append(time.perf_counter() - t0)

    assert result is not None
    page_count = result.metadata.get("page_count")
    if page_count is not None:
        if callable(page_count):
            page_count = page_count()  # Executa o método para pegar o número
        page_count = int(page_count)

    criteria: dict[str, Any] = {
        "speed": evaluate_speed(timings, page_count),
        "layout": evaluate_layout(result, evaluator),
        "tables": evaluate_tables(result, evaluator),
        "output": evaluate_output(result),
        "complexity": evaluate_complexity(evaluator.lib_label),
        "dependencies": evaluate_dependencies(evaluator.distribution_name),
        "engineering": evaluate_engineering(evaluator.lib_label),
        "accuracy": evaluate_accuracy(result, ground_truth),
    }

    return {
        "lib": evaluator.lib_label,
        "distribution": evaluator.distribution_name,
        "file": str(path.resolve()),
        "criteria": criteria,
        "categories": group_by_category(criteria),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate a PDF extraction library on a single file (benchmark harness).",
    )
    parser.add_argument(
        "--lib",
        required=True,
        help=f"Library name. Supported: {', '.join(list_supported_libs())}. "
        "Aliases: pdfminer.six → pdfminer.",
    )
    parser.add_argument("--file", required=True, help="Path to input PDF.")
    parser.add_argument(
        "--output",
        "-o",
        default="",
        help="Write JSON report to this path (stdout if omitted).",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of timed extract() runs after warmup (default: 1).",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=0,
        help="Number of untimed extract() runs before measurement (default: 0).",
    )
    parser.add_argument(
        "--ground-truth",
        default="",
        help="Optional UTF-8 text file to compare against extracted text (accuracy metric).",
    )

    args = parser.parse_args(argv)
    gt = args.ground_truth.strip() or None

    try:
        report = run_evaluation(
            args.lib,
            args.file,
            repeat=args.repeat,
            warmup=args.warmup,
            ground_truth=gt,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(exc, file=sys.stderr)
        return 1

    text = json.dumps(report, indent=2, ensure_ascii=False, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
