from __future__ import annotations

from typing import Callable, List

from command.grep.color import Color
from command.grep.input_processor import ProcessingOutput
from command.grep.context import Context
from command.grep.exceptions import SuppressBinaryOutputError
from match import MatchPosition
from storage.base import DEFAULT_ENCODING

DEFAULT_COLOR = Color.GREEN

CreateOutputMessage = Callable[[ProcessingOutput, Context], str]


def create_output_message(
        processing_output: ProcessingOutput, context: Context
) -> str:
    """
    Create an output message based on processing output and context.

    :param ProcessingOutput processing_output: The processing output.
    :param Context context: The context for processing.
    :return: The formatted output message.
    :rtype: str.
    """

    return (
            add_file_name(processing_output, context)
            + add_line_num(processing_output, context)
            + add_line(processing_output, context)
    )


def add_file_name(
        processing_result: ProcessingOutput, context: Context
) -> str:
    """
    Add file name to the output message.

    :param ProcessingOutput processing_result: The processing result.
    :param Context context: The context for processing.
    :return: The formatted file name string.
    :rtype: str.
    """

    return f"{processing_result.path}:"


def add_line_num(processing_result: ProcessingOutput, context: Context) -> str:
    """
    Add line number to the output message if specified in the context.

    :param ProcessingOutput processing_result: The processing result.
    :param Context context: The context for processing.
    :return: The formatted line number string.
    :rtype: str.
    """

    if context.output_control_options.line_number:
        return f"{processing_result.line_number}:"
    return ""


def add_line(processing_result: ProcessingOutput, context: Context) -> str:
    """
    Add line content to the output message.

    :param ProcessingOutput processing_result: The processing result.
    :param Context context: The context for processing.
    :return: The formatted line content string.
    :rtype: str.
    :raises SuppressBinaryOutputError: If binary output is not allowed
    and the line is binary.
    """

    if isinstance(processing_result.line, bytes):
        if context.output_control_options.treat_binary_as_text:
            return processing_result.line.decode(DEFAULT_ENCODING, "replace")
        else:
            raise SuppressBinaryOutputError

    elif (
            processing_result.matches
            and context.output_control_options.color
            and not context.pattern_matching_options.invert_match
    ):
        return colorize(processing_result.line, processing_result.matches)
    elif context.output_control_options.count:
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
        formatted_string = line[index: match_position.start] + _colorize_text(
            line[match_position.start: match_position.end], DEFAULT_COLOR
        )
        return formatted_string + _format_recursive(
            line, match_positions[1:], match_position.end
        )

    return _format_recursive(line, match_positions, 0)


def _colorize_text(text, color) -> str:
    return f"{color.value}{text}{Color.END.value}"
