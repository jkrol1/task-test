from __future__ import annotations

from abc import abstractmethod
import re
from typing import AnyStr, List, Optional, Pattern

from command.grep.context import PatternMatchingOptions
from match.base import IPatternMatcher, MatchPosition


class PatternMatcherTemplate(IPatternMatcher[AnyStr]):
    """
    A template for pattern matchers.

    Provides a template for implementing pattern matching operations.

    :param List[str] patterns: A list of patterns to match against.
    :param PatternMatchingOptions pattern_matching_options: Options for pattern matching.
    """

    def __init__(
            self, patterns: List[str], pattern_matching_options: PatternMatchingOptions
    ) -> None:
        self._patterns = patterns
        self._options = pattern_matching_options
        self._compiled_regex_patterns: List[Pattern[AnyStr]] = (
            self._compile_regex_patterns()
        )

    def search(self, input_val: AnyStr) -> Optional[MatchPosition]:
        for compiled_regex in self._compiled_regex_patterns:
            match = compiled_regex.search(input_val)
            if match and not self._options.invert_match:
                return MatchPosition(match.start(), match.end())
            elif self._options.invert_match:
                return MatchPosition(0, len(input_val))
        return None

    @abstractmethod
    def _compile_regex_patterns(self) -> List[re.Pattern[AnyStr]]:
        pass

    def _get_flags(self) -> int:
        flags = 0
        if self._options.ignore_case:
            flags |= re.IGNORECASE

        return flags


class BinaryPatternMatcher(PatternMatcherTemplate[bytes]):
    """PatternMatcher for bytes input"""

    def match(self, input_val: bytes) -> Optional[List[MatchPosition]]:
        if match_position := self.search(input_val):
            return [match_position]
        return None

    def _compile_regex_patterns(self) -> List[Pattern[bytes]]:
        flags = self._get_flags()
        compiled_patterns = []

        for pattern in self._patterns:
            encoded_pattern = pattern.encode()
            regex_pattern = (
                rb"\b%s\b" % encoded_pattern
                if self._options.word_regexp
                else rb"%s" % encoded_pattern
            )

            compiled_patterns.append(re.compile(regex_pattern, flags=flags))

        return compiled_patterns


class TextPatternMatcher(PatternMatcherTemplate[str]):
    """PatternMatcher for str input"""

    def match(self, input_val: str) -> List[MatchPosition]:
        positions = []
        for compiled_regex in self._compiled_regex_patterns:
            for matched_position in self._get_matched_positions(
                    input_val, compiled_regex
            ):
                positions.append(matched_position)
        return positions

    def _compile_regex_patterns(self) -> List[re.Pattern[str]]:
        flags = self._get_flags()

        return [
            re.compile(
                (
                    rf"\b{re.escape(pattern)}\b"
                    if self._options.word_regexp
                    else pattern
                ),
                flags,
            )
            for pattern in self._patterns
        ]

    def _get_matched_positions(
            self, input_val: str, compiled_regex: re.Pattern[str]
    ) -> List[MatchPosition]:
        if self._options.invert_match and not self._is_match_found(
                input_val, compiled_regex
        ):
            return [MatchPosition(0, len(input_val))]
        return [
            MatchPosition(match.start(), match.end())
            for match in compiled_regex.finditer(input_val)
        ]

    @staticmethod
    def _is_match_found(input_val: AnyStr, compiled_regex: re.Pattern[AnyStr]) -> bool:
        return bool(compiled_regex.search(input_val))
