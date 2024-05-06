from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockFixture

from python_grep.grep.base import ProcessingOutput
from python_grep.grep.context import OutputControlOptions
from python_grep.grep.grep import LineMatchGrep
from python_grep.grep.output import SuppressBinaryOutputError
from python_grep.match import MatchPosition
from python_grep.storage import InputType


@pytest.fixture
def mocked_line_match_grep(mocker: MockFixture) -> LineMatchGrep:
    context = mocker.Mock()
    reader = mocker.Mock()
    path_resolver = mocker.Mock()
    path_resolver.get_resolved_file_paths.return_value = ["file.txt"]
    create_output_message = mocker.Mock()
    create_output_message.return_value = "file.txt:line match 1"
    input_processor = mocker.Mock()
    input_processor.process.side_effect = [
        [
            ProcessingOutput(
                matches=[MatchPosition(start=5, end=7)],
                path=Path("file.txt"),
                input_type=InputType.TEXT,
                line_number=10,
                line="Test line",
                match_count=1,
            )
        ]
    ]
    file_type_to_pattern_matcher_map = mocker.Mock()
    grep = LineMatchGrep(
        reader,
        path_resolver,
        create_output_message,
        file_type_to_pattern_matcher_map,
        context,
    )

    mocker.patch.object(
        grep, "create_input_processor", return_value=input_processor
    )

    return grep


def test_grep_execute(
    mocked_line_match_grep: LineMatchGrep, capsys: CaptureFixture[str]
) -> None:
    mocked_line_match_grep.execute()
    captured = capsys.readouterr()
    captured_output = captured.out

    assert captured_output == "file.txt:line match 1\n"


def test_suppress_binary_output_error_handling(
    mocked_line_match_grep: LineMatchGrep, capsys: CaptureFixture[str]
) -> None:
    def _raise_suppress_binary_output_exception(
        _: ProcessingOutput, _2: OutputControlOptions
    ) -> str:
        raise SuppressBinaryOutputError

    mocked_line_match_grep._create_output_message = (
        _raise_suppress_binary_output_exception
    )
    mocked_line_match_grep.execute()
    captured_output = capsys.readouterr().out

    assert captured_output == "Binary file file.txt matches\n"
