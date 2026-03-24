from __future__ import annotations

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


def evaluate_tables(result: ExtractionResult, evaluator: BaseEvaluator) -> dict:
    """
    Table-related stats from normalized ``result.tables``.

    Without ground truth, ``quality_vs_truth`` stays ``null`` (see ``metrics.accuracy``).
    """
    tables = result.tables
    total_cells = 0
    empty_cells = 0
    max_cols = 0
    for table in tables:
        for row in table:
            max_cols = max(max_cols, len(row))
            for cell in row:
                total_cells += 1
                if not str(cell).strip():
                    empty_cells += 1

    return {
        "table_count": len(tables),
        "supports_tables_flag": evaluator.supports_tables,
        "total_cells": total_cells,
        "empty_cell_ratio": (empty_cells / total_cells) if total_cells else None,
        "max_columns_seen": max_cols,
        "quality_vs_truth": None,
        "note": (
            "Ground-truth table accuracy not computed; "
            "use accuracy metric with future table ground truth."
        ),
    }
