from __future__ import annotations

from argparse import Namespace

from command.grep.input_processor import InputTypeToPatternMatcherMapping
from command.grep import (
    Grep,
    LineMatchGrep,
    LineMatchCounterGrep,
    BeforeContextLineMatchGrep,
    AfterContextLineMatchGrep,
)

from command.grep.output import create_output_message
from command.grep.context import Context
from match import BinaryPatternMatcher, TextPatternMatcher
from storage.base import InputType
from storage.path_resolver import PathResolver
from storage.file_reader import FileReader


def create_grep_from_cli_args(parsed_cli_args: Namespace) -> Grep:
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
