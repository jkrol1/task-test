from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional, List, Union

from match import MatchPosition
from storage.base import InputType


class IInputProcessor(ABC):
    """Interface for input processors. Input processors
    are responsible for orchestrating pattern matching and
    applying specific logic on read file lines.
    """

    @abstractmethod
    def process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        """
        Process data from a file at a given path.

        :param path: The path to the input.
        :type path: pathlib.Path
        :yield: Generator yielding ProcessingOutput objects.
        :rtype: Generator[ProcessingOutput, None, None]
        """


@dataclass(frozen=True)
class ProcessingOutput:
    matches: Optional[List[MatchPosition]]
    path: Path
    input_type: InputType
    line: Union[bytes, str]
    line_number: int
    match_count: int = 0
