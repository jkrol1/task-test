from __future__ import annotations

from enum import Enum
from typing import Callable, List

from python_grep.grep.base import ProcessingOutput
from python_grep.grep.context import OutputControlOptions
from python_grep.grep.exceptions import SuppressBinaryOutputError
from python_grep.match import MatchPosition
from python_grep.storage import DEFAULT_ENCODING

CreateOutputMessage = Callable[[ProcessingOutput, OutputControlOptions], str]


def create_output_message(
    processing_output: ProcessingOutput,
    output_control_options: OutputControlOptions,
) -> str:
    """
    Create an output message based on processing output and context.

    :param ProcessingOutput processing_output: The processing output.
    :param OutputControlOptions output_control_options: Output control options.
    :return: The formatted output message.
    :rtype: str.
    """

    return (
        add_file_name(processing_output, output_control_options)
        + add_line_num(processing_output, output_control_options)
        + add_line(processing_output, output_control_options)
    )


def add_file_name(
    processing_result: ProcessingOutput,
    output_control_options: OutputControlOptions,
) -> str:
    """
    Add file name to the output message.

    :param ProcessingOutput processing_result: The processing result.
    :param OutputControlOptions output_control_options: Output control options.
    :return: The formatted file name string.
    :rtype: str.
    """

    return f"{processing_result.path}:"


def add_line_num(
    processing_result: ProcessingOutput,
    output_control_options: OutputControlOptions,
) -> str:
    """
    Add line number to the output message if specified in the context.

    :param ProcessingOutput processing_result: The processing result.
    :param Context output_control_options: Output control options.
    :return: The formatted line number string.
    :rtype: str.
    """

    if output_control_options.line_number:
        return f"{processing_result.line_number}:"
    return ""


def add_line(
    processing_result: ProcessingOutput,
    output_control_options: OutputControlOptions,
) -> str:
    """
    Add line content to the output message.

    :param ProcessingOutput processing_result: The processing result.
    :param Context output_control_options: Output control options.
    :return: The formatted line content string.
    :rtype: str.
    :raises SuppressBinaryOutputError: If binary output is not allowed
    and the line is binary.
    """

    if isinstance(processing_result.line, bytes):
        if output_control_options.treat_binary_as_text:
            return processing_result.line.decode(DEFAULT_ENCODING, "replace")
        else:
            raise SuppressBinaryOutputError

    elif processing_result.matches and output_control_options.color:
        return colorize(processing_result.line, processing_result.matches)
    elif output_control_options.count:
        return str(processing_result.match_count)
    else:
        return processing_result.line


def colorize(line: str, match_positions: List[MatchPosition]) -> str:
    """
    Colorize matched text in the line.

    :param str line: The line content.
    :param List[MatchPosition] match_positions: The positions of
     matches in the line.
    :return: The colorized line content.
    :rtype: str.
    """

    def _format_recursive(
        line: str, match_positions: List[MatchPosition], index: int
    ) -> str:
        if not match_positions:
            return line[index:]

        match_position = match_positions[0]
        formatted_string = line[index : match_position.start] + _colorize_text(
            line[match_position.start : match_position.end], Color.GREEN
        )
        return formatted_string + _format_recursive(
            line, match_positions[1:], match_position.end
        )

    return _format_recursive(line, match_positions, 0)


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
