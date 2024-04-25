from typing import Callable, List, Union, Optional
from pathlib import Path

from command.grep.color import Color
from match import MatchPosition

DEFAULT_COLOR = Color.GREEN

OutputPrinter = Callable[[Path, Union[str, int], Optional[List[MatchPosition]]], None]


def print_output_with_path(path: Path, processed_data: Union[str, int],
                           match_positions: List[MatchPosition] = None) -> None:
    print(
        f"{path}: {processed_data}"
    )


def print_output_without_path(path: Path, processed_data: Union[str, int],
                              match_positions: List[MatchPosition] = None) -> None:
    print(
        f"{processed_data}"
    )


def print_output_with_path_colorized(path, processed_data: Union[str, int],
                                     match_positions: List[MatchPosition]) -> None:
    print(
        f"{path}: {_colorize_output_string_for_matches(processed_data, match_positions)}"
    )


def _colorize_output_string_for_matches(string: str, match_positions: List[MatchPosition]):
    def _format_recursive(string: str, match_positions: List[MatchPosition], index: int) -> str:
        if not match_positions:
            return string[index:]

        match_position = match_positions[0]
        formatted_string = (
                string[index:match_position.start] +
                _colorize_text(string[match_position.start:match_position.end], DEFAULT_COLOR)
        )
        return formatted_string + _format_recursive(string, match_positions[1:], match_position.end)

    return _format_recursive(string, match_positions, 0)


def _colorize_text(text, color):
    return f"{color.value}{text}{Color.END.value}"
