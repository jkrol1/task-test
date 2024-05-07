from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, List, Optional, Union

from python_grep.match import MatchPosition
from python_grep.storage.base import InputType


class ICommand(ABC):
    """Interface for command objects."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""

        pass


class IOutputMessageBuilder(ABC):
    """Interface for output message builders."""

    @abstractmethod
    def create(self, processing_output: ProcessingOutput) -> str:
        """
        Create an output message based on processing output.

        :param ProcessingOutput processing_output: The processing output.
        :return: Output message.
        :rtype: str.
        """

        pass


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
