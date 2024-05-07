from __future__ import annotations

from enum import Enum
from typing import List

from python_grep.grep.base import ProcessingOutput, IOutputMessageBuilder
from python_grep.grep.context import OutputControlOptions
from python_grep.grep.exceptions import SuppressBinaryOutputError
from python_grep.match import MatchPosition
from python_grep.storage import DEFAULT_ENCODING


class OutputMessageBuilder(IOutputMessageBuilder):
    """
    Constructs final output massage based on the
    output control options and processing output.

    :param OutputControlOptions output_control_options:
    Options for output control.
    """

    def __init__(self, output_control_options: OutputControlOptions) -> None:
        self._output_control_options = output_control_options

    def create(self, processing_output: ProcessingOutput) -> str:
        return (
            self._add_file_name(processing_output)
            + self._add_line_num(processing_output)
            + self._add_line(processing_output)
        )

    @staticmethod
    def _add_file_name(
        processing_result: ProcessingOutput,
    ) -> str:
        return f"{processing_result.path}:"

    def _add_line_num(
        self,
        processing_result: ProcessingOutput,
    ) -> str:

        if self._output_control_options.line_number:
            return f"{processing_result.line_number}:"
        return ""

    def _add_line(
        self,
        processing_result: ProcessingOutput,
    ) -> str:
        if isinstance(processing_result.line, bytes):
            if self._output_control_options.treat_binary_as_text:
                return processing_result.line.decode(
                    DEFAULT_ENCODING, "replace"
                )
            else:
                raise SuppressBinaryOutputError

        elif processing_result.matches and self._output_control_options.color:
            return self._colorize(
                processing_result.line, processing_result.matches
            )
        elif self._output_control_options.count:
            return str(processing_result.match_count)
        else:
            return processing_result.line

    def _colorize(
        self, line: str, match_positions: List[MatchPosition]
    ) -> str:

        return self._colorize_tail_recursive(line, match_positions, 0)

    def _colorize_tail_recursive(
        self, line: str, match_positions: List[MatchPosition], index: int
    ) -> str:
        if not match_positions:
            return line[index:]

        match_position = match_positions[0]
        formatted_string = line[
            index : match_position.start
        ] + self._colorize_text(
            line[match_position.start : match_position.end], Color.GREEN
        )
        return formatted_string + self._colorize_tail_recursive(
            line, match_positions[1:], match_position.end
        )

    @staticmethod
    def _colorize_text(text, color) -> str:
        return f"{color.value}{text}{Color.END.value}"


class Color(Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    END = "\033[0m"
