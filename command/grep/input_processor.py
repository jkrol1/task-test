from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

from match import PatternMatcher
from storage.text_format_reader import TextFormatReader


class AbstractInputProcessor(ABC):
    def __init__(self, reader: TextFormatReader, pattern_matcher: PatternMatcher, output_printer: Callable) -> None:
        self._reader = reader
        self._pattern_matcher = pattern_matcher
        self._output_printer = output_printer

    @abstractmethod
    def process(self, path: Path) -> None:
        pass


class LineMatchProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        for line in self._reader.read_lines(path):
            if matched_positions := self._pattern_matcher.match(line):
                self._output_printer(path, line, matched_positions)


class LineMatchCounterProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        match_count = 0
        for line in self._reader.read_lines(path):
            match_count += len(self._pattern_matcher.match(line))
        self._output_printer(path, match_count)
