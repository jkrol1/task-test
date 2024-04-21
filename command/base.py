from __future__ import annotations

from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
