from __future__ import annotations

from abc import ABC, abstractmethod


class ICommand(ABC):
    """Interface for command objects."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""

        pass
