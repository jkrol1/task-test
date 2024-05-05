from pathlib import Path

import pytest

from command.grep.base import ProcessingOutput
from command.grep.context import Context, PatternMatchingOptions, OutputControlOptions, ContextControlOptions
from command.grep.output import create_output_message, add_file_name, add_line_num, add_line, colorize
from match import MatchPosition
from storage.base import InputType


@pytest.fixture
def processing_output():
    return ProcessingOutput(
        matches=[MatchPosition(start=5, end=7)],
        path=Path("file.txt"),
        input_type=InputType.TEXT,
        line_number=10,
        line="Test line",
        match_count=1,
    )


@pytest.fixture
def context():
    return Context(
        patterns=[""],
        file_paths=[""],
        output_control_options=OutputControlOptions(line_number=True,
                                                    recursive=False,
                                                    color=True,
                                                    count=False,
                                                    treat_binary_as_text=False),
        pattern_matching_options=PatternMatchingOptions(invert_match=False, word_regexp=False, ignore_case=False),
        context_control_options=ContextControlOptions(before_context=False, after_context=False)
    )


def test_create_output_message(processing_output: ProcessingOutput, context: Context) -> None:
    message = create_output_message(processing_output, context)
    expected_message = "file.txt:10:Test \x1b[92mli\x1b[0mne"
    assert message == expected_message


def test_add_file_name(processing_output: ProcessingOutput, context: Context) -> None:
    file_name = add_file_name(processing_output, context)
    expected_file_name = "file.txt:"
    assert file_name == expected_file_name


def test_add_line_num(processing_output: ProcessingOutput, context: Context) -> None:
    line_num = add_line_num(processing_output, context)
    expected_line_num = "10:"
    assert line_num == expected_line_num


def test_add_line(processing_output: ProcessingOutput, context: Context) -> None:
    line = add_line(processing_output, context)
    expected_line = "Test \x1b[92mli\x1b[0mne"
    assert line == expected_line


def test_colorize() -> None:
    line = "Test line"
    matches = [MatchPosition(start=5, end=7)]
    colored_line = colorize(line, matches)
    expected_colored_line = "Test \x1b[92mli\x1b[0mne"
    assert colored_line == expected_colored_line
