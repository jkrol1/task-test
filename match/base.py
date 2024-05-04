from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AnyStr, Generic, List, Optional


class IPatternMatcher(ABC, Generic[AnyStr]):

    @abstractmethod
    def match(self, input_val: AnyStr) -> Optional[List[MatchPosition]]:
        pass

    @abstractmethod
    def search(self, input_val: AnyStr) -> Optional[MatchPosition]:
        pass


@dataclass(frozen=True)
class MatchPosition:
    start: int
    end: int
