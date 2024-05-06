from __future__ import annotations

from argparse import Namespace

from python_grep.grep.context import Context
from python_grep.grep.grep import (
    AfterContextLineMatchGrep,
    BeforeContextLineMatchGrep,
    Grep,
    LineMatchCounterGrep,
    LineMatchGrep,
)
from python_grep.grep.input_processor import InputTypeToPatternMatcherMapping
from python_grep.grep.output import create_output_message
from python_grep.match import BinaryPatternMatcher, TextPatternMatcher
from python_grep.storage.base import InputType
from python_grep.storage.file_reader import FileReader
from python_grep.storage.path_resolver import PathResolver


def create_grep_from_cli_args(parsed_cli_args: Namespace) -> Grep:
    """
    Create a Grep instance based on the parsed command-line arguments.

    :param Namespace parsed_cli_args: Parsed command-line arguments
    as a Namespace object.
    :return: A Grep instance based on the provided command-line arguments.
    :rtype: Grep.
    """

    context = Context.from_parsed_cli_args(parsed_cli_args)
    file_reader = FileReader()
    path_resolver = PathResolver(
        context.file_paths,
        context.output_control_options.recursive,
    )

    text_pattern_matcher = TextPatternMatcher(
        context.patterns, context.pattern_matching_options
    )
    binary_pattern_matcher = BinaryPatternMatcher(
        context.patterns, context.pattern_matching_options
    )
    file_type_to_pattern_matcher_map: InputTypeToPatternMatcherMapping = {
        InputType.TEXT: text_pattern_matcher,
        InputType.BINARY: binary_pattern_matcher,
    }

    if context.output_control_options.count:
        return LineMatchCounterGrep(
            file_reader,
            path_resolver,
            create_output_message,
            file_type_to_pattern_matcher_map,
            context,
        )
    elif context.context_control_options.before_context:
        return BeforeContextLineMatchGrep(
            file_reader,
            path_resolver,
            create_output_message,
            file_type_to_pattern_matcher_map,
            context,
        )
    elif context.context_control_options.after_context:
        return AfterContextLineMatchGrep(
            file_reader,
            path_resolver,
            create_output_message,
            file_type_to_pattern_matcher_map,
            context,
        )
    else:
        return LineMatchGrep(
            file_reader,
            path_resolver,
            create_output_message,
            file_type_to_pattern_matcher_map,
            context,
        )
