from argparse import Namespace

from command.grep import Grep
from command.grep.input_processor import AfterContextLineMatchProcessor, BeforeContextLineMatchProcessor, \
    LineMatchCounterProcessor, LineMatchProcessor
from command.grep.output import print_output_without_path, print_output_with_path
from match import PatternMatcher
from storage.path_resolver import PathResolver
from storage.file_reader import FileReader


def create_grep_from_cli_args(parsed_cli_args: Namespace) -> Grep:
    patterns = parsed_cli_args.patterns
    file_paths = parsed_cli_args.files
    count_lines = parsed_cli_args.count
    before_context = parsed_cli_args.before_context
    after_context = parsed_cli_args.after_context
    recursive = parsed_cli_args.recursive
    invert_match = parsed_cli_args.invert_match
    whole_word_match = parsed_cli_args.word_regexp
    ignore_case = parsed_cli_args.ignore_case
    line_number = parsed_cli_args.line_number

    reader = FileReader()
    pattern_matcher = PatternMatcher(patterns,
                                     whole_word_match=whole_word_match,
                                     invert_match=invert_match,
                                     ignore_case=ignore_case)
    path_resolver = PathResolver(file_paths=file_paths, recursive=recursive)

    if count_lines:
        input_processor = LineMatchCounterProcessor(reader, pattern_matcher, print_output_without_path)
    elif before_context:
        input_processor = BeforeContextLineMatchProcessor(reader, pattern_matcher, print_output_without_path)
    elif after_context:
        input_processor = AfterContextLineMatchProcessor(reader, pattern_matcher, print_output_without_path)
    else:
        input_processor = LineMatchProcessor(reader, pattern_matcher, print_output_with_path)

    return Grep(
        path_resolver=path_resolver,
        input_processor=input_processor
    )
