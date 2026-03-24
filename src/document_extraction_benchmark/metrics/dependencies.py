from __future__ import annotations

from importlib.metadata import PackageNotFoundError, requires


def evaluate_dependencies(distribution_name: str) -> dict:
    """
    List declared dependencies for the installed distribution (PyPI name), e.g. ``pdfminer.six``.
    """
    try:
        req_list = requires(distribution_name)
    except PackageNotFoundError:
        return {
            "distribution": distribution_name,
            "requires": None,
            "error": "package_not_found",
        }
    if req_list is None:
        return {"distribution": distribution_name, "requires": [], "requirement_count": 0}
    sorted_req = sorted(req_list)
    return {
        "distribution": distribution_name,
        "requires": sorted_req,
        "requirement_count": len(sorted_req),
    }
