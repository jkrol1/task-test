from pathlib import Path

import pytest

from python_grep.grep.base import ProcessingOutput
from python_grep.grep.context import (
    OutputControlOptions,
)
from python_grep.grep.output import OutputMessageBuilder
from python_grep.match import MatchPosition
from python_grep.storage import InputType

OUTPUT_MESSAGE_BUILD_TEST_INPUT = [
    (
        ProcessingOutput(
            matches=[MatchPosition(start=5, end=7)],
            path=Path("file.txt"),
            input_type=InputType.TEXT,
            line_number=10,
            line="Test line",
            match_count=1,
        ),
        OutputControlOptions(
            line_number=True,
            recursive=False,
            color=True,
            count=False,
            treat_binary_as_text=False,
        ),
        "file.txt:10:Test \x1b[92mli\x1b[0mne",
    ),
    (
        ProcessingOutput(
            matches=None,
            path=Path("file.txt"),
            input_type=InputType.TEXT,
            line_number=10,
            line="",
            match_count=15,
        ),
        OutputControlOptions(
            line_number=True,
            recursive=False,
            color=True,
            count=True,
            treat_binary_as_text=False,
        ),
        "file.txt:10:15",
    ),
]


@pytest.mark.parametrize(
    "processing_output, output_control_options, expected_output_str",
    OUTPUT_MESSAGE_BUILD_TEST_INPUT,
)
def test_output_message_builder_create(
    processing_output: ProcessingOutput,
    output_control_options: OutputControlOptions,
    expected_output_str: str,
) -> None:
    message = OutputMessageBuilder(output_control_options).create(
        processing_output
    )
    assert message == expected_output_str
