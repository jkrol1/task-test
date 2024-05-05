from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AnyStr, Generic, List, Optional


class IPatternMatcher(ABC, Generic[AnyStr]):
    """Interface for pattern matchers."""

    @abstractmethod
    def match(self, input_val: AnyStr) -> Optional[List[MatchPosition]]:
        """
          Perform a full match operation.

          Attempts to match the entire input string with the pattern and
          returns match position of every single match.

          :param AnyStr input_val: The input value to match against.
          :return: A list of MatchPosition objects representing the matches,
                   or None if no matches are found.
          :rtype: Optional[List[MatchPosition]],
          """

    @abstractmethod
    def search(self, input_val: AnyStr) -> Optional[MatchPosition]:
        """
        Perform a search operation.

        Searches for the pattern within the input string.
        Returns first found MatchPosition.


        :param AnyStr input_val: The input value to search within.
        :return: A MatchPosition object representing the first match found,
                 or None if no matches are found.
        :rtype: Optional[MatchPosition]
        """
        pass


@dataclass(frozen=True)
class MatchPosition:
    start: int
    end: int
