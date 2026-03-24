from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractionResult:
    """Normalized output from any PDF adapter for metric functions."""

    text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    layout_blocks: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    output_notes: list[str] = field(default_factory=list)
    markdown: str | None = None
    structured_dict: dict[str, Any] | None = None
