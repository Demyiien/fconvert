"""Base class every converter inherits from."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class ConversionError(Exception):
    pass


class BaseConverter(ABC):
    name = ""
    input_formats: set = set()
    output_formats: set = set()
    quality_hint = ""

    def can_convert(self, src_ext: str, target: str) -> bool:
        return src_ext in self.input_formats and target in self.output_formats and src_ext != target

    def output_folder_name(self, target: str) -> str:
        """Sub-folder inside output/ where results go."""
        return target

    @abstractmethod
    def convert(self, src: Path, dest: Path, target: str, quality: Optional[int]) -> None:
        ...
