from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import sys

from typing import AnyStr, Generator, Generic, TypeVar

DEFAULT_ENCODING = sys.getdefaultencoding()


class IFileReader(ABC, Generic[AnyStr]):
    """FileReader Interface."""

    @abstractmethod
    def read_lines(self, path: Path) -> Generator[AnyStr, None, None]:
        pass

    @abstractmethod
    def on_input_type_change(self, callback) -> None:
        pass


class IPathResolver(ABC):

    @abstractmethod
    def get_resolved_file_paths(self) -> Generator[Path, None, None]:
        pass


class InputType(Enum):
    TEXT = "TEXT"
    BINARY = "BINARY"
