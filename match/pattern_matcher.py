from __future__ import annotations

import re
from typing import AnyStr, List, Pattern

from match.base import IPatternMatcher, MatchPosition


class PatternMatcher(IPatternMatcher):
    def __init__(self, patterns: List[str],
                 whole_word_match: bool = False,
                 invert_match: bool = False,
                 ignore_case: bool = False) -> None:
        self._patterns = patterns
        self._whole_word_match = whole_word_match
        self._invert_match = invert_match
        self._ignore_case = ignore_case

    def match_string(self, string: str) -> List[MatchPosition]:
        positions = []
        for pattern in self._patterns:
            compiled_regex = self._compile_regex(pattern)
            for matched_position in self._get_matched_positions(string, compiled_regex):
                positions.append(matched_position)
        return positions

    def match_bytes(self, bt: bytes) -> bool:
        for pattern in self._patterns:
            compiled_regex = self._compile_bytes_regex(pattern)
            match = compiled_regex.search(bt)

            return match is not None

    def _get_matched_positions(self, string: str, compiled_regex: re.Pattern[str]) -> List[MatchPosition]:
        if self._invert_match:
            if not self._is_match_found(string, compiled_regex):
                return [MatchPosition(0, len(string))]
        else:
            return [MatchPosition(match.start(), match.end()) for match in compiled_regex.finditer(string)]

    def _compile_bytes_regex(self, pattern: str) -> Pattern[AnyStr]:
        flags = self._get_flags()
        encoded_pattern = pattern.encode()
        regex_pattern = rb'\b%s\b' % encoded_pattern if self._whole_word_match else rb'%s' % encoded_pattern

        return re.compile(regex_pattern, flags=flags)

    def _compile_regex(self, pattern: str):
        flags = self._get_flags()

        return re.compile((rf'\b{re.escape(pattern)}\b' if self._whole_word_match else pattern), flags)

    def _get_flags(self) -> int:
        flags = 0
        if self._ignore_case:
            flags |= re.IGNORECASE

        return flags

    @staticmethod
    def _is_match_found(string: str, compiled_regex: re.Pattern[str]) -> bool:
        return bool(compiled_regex.search(string))
