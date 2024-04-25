from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class IInputProcessor(ABC):
    @abstractmethod
    def process(self, path: Path) -> None:
        pass
