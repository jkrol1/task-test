from pathlib import Path

import pytest

from python_grep.grep.base import ProcessingOutput
from python_grep.grep.context import (
    OutputControlOptions,
)
from python_grep.grep.output import (
    add_file_name,
    add_line,
    add_line_num,
    colorize,
    create_output_message,
)
from python_grep.match import MatchPosition
from python_grep.storage import InputType


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
def output_control_options():
    return OutputControlOptions(
        line_number=True,
        recursive=False,
        color=True,
        count=False,
        treat_binary_as_text=False,
    )


def test_create_output_message(
    processing_output: ProcessingOutput, output_control_options
) -> None:
    message = create_output_message(processing_output, output_control_options)
    expected_message = "file.txt:10:Test \x1b[92mli\x1b[0mne"
    assert message == expected_message


def test_add_file_name(
    processing_output: ProcessingOutput, output_control_options
) -> None:
    file_name = add_file_name(processing_output, output_control_options)
    expected_file_name = "file.txt:"
    assert file_name == expected_file_name


def test_add_line_num(
    processing_output: ProcessingOutput, output_control_options
) -> None:
    line_num = add_line_num(processing_output, output_control_options)
    expected_line_num = "10:"
    assert line_num == expected_line_num


def test_add_line(
    processing_output: ProcessingOutput, output_control_options
) -> None:
    line = add_line(processing_output, output_control_options)
    expected_line = "Test \x1b[92mli\x1b[0mne"
    assert line == expected_line


def test_colorize() -> None:
    line = "Test line"
    matches = [MatchPosition(start=5, end=7)]
    colored_line = colorize(line, matches)
    expected_colored_line = "Test \x1b[92mli\x1b[0mne"
    assert colored_line == expected_colored_line
