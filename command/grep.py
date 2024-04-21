from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from typing import Iterator, List

from command.base import ICommand
from storage.text_format_reader import TextFormatReader
from storage.file_finder import get_absolute_path, resolve_patterns, traverse_directories


class Grep(ICommand):
    def __init__(self, pattern: str, file_paths: List[str], recursive: bool = False):
        self._pattern = pattern
        self._file_paths = file_paths
        self._recursive = recursive

    def execute(self) -> None:
        reader = TextFormatReader()
        pattern_matcher = PatternMatcher([self._pattern])

        abs_paths = []
        for path in self._file_paths:
            abs_path = get_absolute_path(path)
            abs_paths.append(abs_path)

        resolved_paths = []
        for abs_path in abs_paths:
            for resolved_path in resolve_patterns(abs_path):
                if not resolved_path.name.startswith("."):
                    if resolved_path.is_dir() and not self._recursive:
                        print(f"grep: {resolved_path.name} is a directory")
                    else:
                        resolved_paths.append(resolved_path)

        all_searched_paths = []
        if self._recursive:
            for resolved_path in resolved_paths:
                if resolved_path.is_dir():
                    for found_path in traverse_directories(resolved_path):
                        if not found_path.name.startswith("."):
                            all_searched_paths.append(found_path)
                else:
                    all_searched_paths.append(resolved_path)
        else:
            all_searched_paths.extend(resolved_paths)

        for path in all_searched_paths:
            for line in reader.read_lines(path):
                matched_positions = pattern_matcher.match(line)
                if matched_positions:
                    print_output(path, format_output(line, matched_positions))


class PatternMatcher:
    def __init__(self, patterns: List[str]) -> None:
        self._patterns = patterns

    def match(self, string: str) -> List[MatchPosition]:
        positions = []
        for pattern in self._patterns:
            for matched_position in self._match(string, pattern):
                positions.append(matched_position)
        return positions

    @staticmethod
    def _match(string: str, pattern: str) -> Iterator[MatchPosition]:
        regex = re.compile(pattern)
        for match in regex.finditer(string):
            start_pos = match.start()
            end_pos = match.end()
            yield MatchPosition(start_pos, end_pos)


@dataclass
class MatchPosition:
    start: int
    end: int


def print_output(path: Path, formatted_output: str, *args, **kwargs) -> None:
    print(
        f"{path}: {formatted_output}", *args, **kwargs
    )


def get_relative_from_file_path(file_path: Path) -> Path:
    script_dir = Path.cwd().resolve()
    relative_path = file_path.relative_to(script_dir)
    if relative_path.parts[0] == '..':
        relative_path = relative_path.relative_to(relative_path.parts[0])

    return relative_path


def format_output(string: str, match_positions: List[MatchPosition]) -> str:
    def _format_recursive(string: str, match_positions: List[MatchPosition], index: int) -> str:
        if not match_positions:
            return string[index:]

        match_position = match_positions[0]
        formatted_string = (
                string[index:match_position.start] +
                colorize_text(string[match_position.start:match_position.end], Color.GREEN)
        )
        return formatted_string + _format_recursive(string, match_positions[1:], match_position.end)

    return _format_recursive(string, match_positions, 0).replace("\n", "")


def colorize_text(text, color):
    return f"{color.value}{text}{Color.END.value}"


class Color(Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    END = "\033[0m"
