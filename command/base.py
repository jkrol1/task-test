from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Union, Optional, List

from match import MatchPosition
from storage.base import InputType


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class IInputProcessor(ABC):
    @abstractmethod
    def process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        pass


@dataclass(frozen=True)
class ProcessingOutput:
    matches: Optional[List[MatchPosition]]
    path: Path
    input_type: InputType
    line: Union[bytes, str]
    line_number: int
    match_count: int = 0
