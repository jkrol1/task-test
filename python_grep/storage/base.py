from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import AnyStr, Callable, Generator, Generic

DEFAULT_ENCODING = sys.getdefaultencoding()


class IFileReader(ABC, Generic[AnyStr]):
    """Interface for file readers."""

    @abstractmethod
    def read_lines(self, path: Path) -> Generator[AnyStr, None, None]:
        """
        Read lines from a file.

        :param Path path: The path to the file.
        :return: A generator yielding lines from the file.
        :rtype: Generator[AnyStr, None, None].
        """
        pass

    @abstractmethod
    def on_input_change(self, callback: Callable[[InputType], None]) -> None:
        """
        Register a callback for input changes.

        :param Callable[[InputType], None] callback: The callback function
         to be called when the input changes.
        """


class IPathResolver(ABC):
    """Interface for path resolver objects."""

    @abstractmethod
    def get_resolved_file_paths(self) -> Generator[Path, None, None]:
        """
        Get resolved file paths.

        :return: A generator yielding resolved file paths.
        :rtype: Generator[Path, None, None]
        """


class InputType(Enum):
    TEXT = "TEXT"
    BINARY = "BINARY"
