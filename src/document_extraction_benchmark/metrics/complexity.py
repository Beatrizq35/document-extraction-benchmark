from __future__ import annotations

from pathlib import Path


def _package_evaluators_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "evaluators"


_ADAPTER_FILES = {
    "docling": "docling.py",
    "pymupdf": "pymupdf_eval.py",
    "pdfplumber": "pdfplumber_eval.py",
    "pdfminer": "pdfminer_eval.py",
    "pypdf": "pypdf_eval.py",
}


def evaluate_complexity(lib_label: str) -> dict:
    """
    Lines of non-empty, non-comment source in this repo's adapter for ``lib_label``.

    Measures maintenance cost of *your* integration code, not the upstream library.
    """
    fname = _ADAPTER_FILES.get(lib_label)
    if not fname:
        return {"error": f"unknown lib_label {lib_label!r}", "adapter_loc": None}
    path = _package_evaluators_dir() / fname
    if not path.is_file():
        return {"error": f"missing adapter file {path}", "adapter_loc": None}
    lines = path.read_text(encoding="utf-8").splitlines()
    logical = 0
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        logical += 1
    return {
        "adapter_file": str(path.relative_to(path.parents[2])),
        "adapter_loc_non_empty_non_comment": logical,
        "adapter_total_lines": len(lines),
    }
