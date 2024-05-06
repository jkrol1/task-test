from __future__ import annotations

from argparse import Namespace
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Context:
    patterns: List[str]
    file_paths: List[str]
    pattern_matching_options: PatternMatchingOptions
    output_control_options: OutputControlOptions
    context_control_options: ContextControlOptions

    @classmethod
    def from_parsed_cli_args(cls, parsed_args: Namespace) -> Context:
        """
        Creates Context from parsed CLI Arguments.

        :param Namespace parsed_args: Parsed CLI arguments
        :return: Application context
        :rtype: Context
        """

        return cls(
            patterns=parsed_args.patterns,
            file_paths=parsed_args.files,
            pattern_matching_options=PatternMatchingOptions(
                invert_match=parsed_args.invert_match,
                word_regexp=parsed_args.word_regexp,
                ignore_case=parsed_args.ignore_case,
            ),
            output_control_options=OutputControlOptions(
                count=parsed_args.count,
                recursive=parsed_args.recursive,
                line_number=parsed_args.line_number,
                treat_binary_as_text=parsed_args.text,
                color=parsed_args.color,
            ),
            context_control_options=ContextControlOptions(
                before_context=parsed_args.before_context,
                after_context=parsed_args.after_context,
            ),
        )


@dataclass(frozen=True)
class PatternMatchingOptions:
    invert_match: bool
    word_regexp: bool
    ignore_case: bool


@dataclass(frozen=True)
class OutputControlOptions:
    count: bool
    recursive: bool
    line_number: bool
    treat_binary_as_text: bool
    color: bool


@dataclass(frozen=True)
class ContextControlOptions:
    before_context: bool
    after_context: bool
