from __future__ import annotations

import re
from pathlib import Path

from document_extraction_benchmark.models import ExtractionResult


def _normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins, delete, sub = cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)
            cur.append(min(ins, delete, sub))
        prev = cur
    return prev[-1]


def evaluate_accuracy(
    result: ExtractionResult,
    ground_truth_path: str | None,
) -> dict:
    """
    Compare extracted text to an optional UTF-8 ground-truth file.

    When ``ground_truth_path`` is omitted, returns a skipped placeholder for future BLEU etc.
    """
    if not ground_truth_path:
        return {
            "status": "skipped",
            "reason": "no_ground_truth_provided",
            "note": "Pass --ground-truth path/to/expected.txt for text metrics.",
        }
    path = Path(ground_truth_path)
    if not path.is_file():
        return {
            "status": "error",
            "reason": "ground_truth_not_found",
            "path": ground_truth_path,
        }
    expected = path.read_text(encoding="utf-8", errors="replace")
    actual = result.text or ""
    ne, na = _normalize(expected), _normalize(actual)
    lev = _levenshtein(ne, na)
    max_len = max(len(ne), len(na), 1)
    ratio = 1.0 - lev / max_len
    return {
        "status": "ok",
        "normalized_levenshtein_distance": lev,
        "similarity_ratio_rough": round(ratio, 6),
        "expected_char_count": len(expected),
        "actual_char_count": len(actual),
    }
