from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List


class PatternMatcher:
    def __init__(self, patterns: List[str], exact_word_match: bool, invert_match: bool) -> None:
        self._patterns = patterns
        self._exact_word_match = exact_word_match
        self._invert_match = invert_match

    def match(self, string: str) -> List[MatchPosition]:
        positions = []
        for pattern in self._patterns:
            for matched_position in self._match(string, pattern):
                positions.append(matched_position)
        return positions

    def _match(self, string: str, pattern: str) -> List[MatchPosition]:
        regex = self._compile_regex(pattern)

        if self._invert_match:
            if not self._is_match_found(string, regex):
                return [MatchPosition(0, len(string))]
        else:
            return [MatchPosition(match.start(), match.end()) for match in regex.finditer(string)]

    def _compile_regex(self, pattern: str):
        return (
            re.compile(r'\b{}\b'.format(re.escape(pattern)))
            if self._exact_word_match
            else re.compile(pattern)
        )

    @staticmethod
    def _is_match_found(string: str, compiled_regex: re.Pattern[str]) -> bool:
        return bool(compiled_regex.search(string))


@dataclass(frozen=True)
class MatchPosition:
    start: int
    end: int
