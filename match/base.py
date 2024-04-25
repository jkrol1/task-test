from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class IPatternMatcher(ABC):

    @abstractmethod
    def match_string(self, string: str) -> List[MatchPosition]:
        pass

    @abstractmethod
    def match_bytes(self, bt: bytes) -> bool:
        pass


@dataclass(frozen=True)
class MatchPosition:
    start: int
    end: int
