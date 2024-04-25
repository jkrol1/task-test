from abc import ABC, abstractmethod
from pathlib import Path
import sys

from typing import Generator, Generic, TypeVar

DEFAULT_ENCODING = sys.getdefaultencoding()

IOType = TypeVar("IOType", str, bytes)


class IFileReader(ABC, Generic[IOType]):
    """FileReader Interface."""

    @abstractmethod
    def read_lines(self, path: Path) -> Generator[IOType, None, None]:
        pass


class IPathResolver(ABC):

    @abstractmethod
    def get_resolved_file_paths(self) -> Generator[Path, None, None]:
        pass
