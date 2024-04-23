from __future__ import annotations

from typing import List

from command.base import ICommand
from command.grep.input_processor import LineMatchProcessor
from command.grep.output import print_output_without_path
from match import PatternMatcher
from storage.text_format_reader import TextFormatReader
from storage.path_resolver import PathResolver


class Grep(ICommand):
    def __init__(self, pattern: str, file_paths: List[str], recursive: bool = False, invert_match=False, count=True):
        self._pattern = pattern
        self._file_paths = file_paths
        self._recursive = recursive
        self._invert_match = invert_match
        self._count = count

    def execute(self) -> None:
        reader = TextFormatReader()
        pattern_matcher = PatternMatcher([self._pattern], exact_word_match=False, invert_match=self._invert_match)
        path_resolver = PathResolver(file_paths=self._file_paths, recursive=self._recursive)
        input_processor = LineMatchProcessor(reader, pattern_matcher, print_output_without_path)

        for path in path_resolver.get_resolved_file_paths():
            input_processor.process(path)
