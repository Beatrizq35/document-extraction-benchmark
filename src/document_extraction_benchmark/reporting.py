from __future__ import annotations

from typing import Any


def group_by_category(flat_criteria: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map flat criterion keys to A–F-style report sections."""
    return {
        "A_architecture_capability": {
            "engineering_rubric": flat_criteria.get("engineering"),
            "layout": flat_criteria.get("layout"),
            "tables": flat_criteria.get("tables"),
        },
        "B_engineering_integration": {
            "dependencies": flat_criteria.get("dependencies"),
            "complexity_adapter_loc": flat_criteria.get("complexity"),
        },
        "C_performance": {
            "speed": flat_criteria.get("speed"),
        },
        "D_output_data_quality": {
            "output": flat_criteria.get("output"),
            "accuracy": flat_criteria.get("accuracy"),
        },
        "E_experimental": {
            "accuracy": flat_criteria.get("accuracy"),
            "tables": flat_criteria.get("tables"),
            "layout": flat_criteria.get("layout"),
        },
        "F_developer_experience": {
            "complexity": flat_criteria.get("complexity"),
            "engineering": flat_criteria.get("engineering"),
        },
    }
