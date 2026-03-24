from __future__ import annotations

import re

from document_extraction_benchmark.evaluators.base import BaseEvaluator
from document_extraction_benchmark.models import ExtractionResult


def _bbox_present(blocks: list[dict]) -> int:
    return sum(1 for b in blocks if b.get("bbox") is not None)


def evaluate_layout(result: ExtractionResult, evaluator: BaseEvaluator) -> dict:
    """
    Heuristic layout score (0–5) from geometry coverage and coarse text structure.

    This is **not** ground-truth fidelity; it encodes whether the pipeline exposes
    structure useful for downstream layout-aware tasks.
    """
    blocks = result.layout_blocks
    text = result.text or ""
    score = 0
    details: dict = {
        "layout_block_count": len(blocks),
        "blocks_with_bbox": _bbox_present(blocks),
        "supports_layout_flag": evaluator.supports_layout,
    }

    if evaluator.supports_layout:
        score += 1
    if blocks:
        score += 1
    if blocks and _bbox_present(blocks) >= max(1, len(blocks) // 10):
        score += 1
    if len(re.findall(r"\n{2,}", text)) >= 2:
        score += 1
    if any(b.get("type") for b in blocks):
        score += 1

    score = min(score, 5)
    details["layout_heuristic_score_0_5"] = score
    details["note"] = (
        "Heuristic only: pair with human or dataset-based layout fidelity for publication."
    )
    return details
