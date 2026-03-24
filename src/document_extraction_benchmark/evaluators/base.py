from __future__ import annotations

from abc import ABC, abstractmethod

from document_extraction_benchmark.models import ExtractionResult


class BaseEvaluator(ABC):
    """Adapter from a specific PDF library to :class:`ExtractionResult`."""

    #: PyPI distribution name for ``importlib.metadata.requires``
    distribution_name: str
    #: Short label used in reports (matches CLI ``--lib`` canonical name)
    lib_label: str
    supports_tables: bool = False
    supports_layout: bool = False

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @abstractmethod
    def extract(self) -> ExtractionResult:
        """Run extraction and return normalized data."""
