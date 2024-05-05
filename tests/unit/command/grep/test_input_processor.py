from pathlib import Path, PosixPath

import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockFixture

from command.grep.base import ProcessingOutput
from command.grep.input_processor import (AfterContextLineMatchProcessor,
                                          BeforeContextLineMatchProcessor,
                                          LineMatchCounterProcessor,
                                          LineMatchProcessor, )
from match import MatchPosition
from storage.base import InputType


def test_line_match_processor(mocker: MockFixture) -> None:
    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines.return_value = (x for x in ["test1 line", "test2 line"])
    mocked_pattern_matcher.match.side_effect = [[MatchPosition(0, 4)], None]
    result = LineMatchProcessor(mocked_file_reader,
                                {InputType.TEXT: mocked_pattern_matcher}).process(Path("path")).__next__()

    expected_result = ProcessingOutput(matches=[MatchPosition(start=0, end=4)], path=PosixPath('path'),
                                       input_type=InputType.TEXT, line='test1 line', line_number=1,
                                       match_count=0)

    assert result == expected_result


def test_line_match_counter_processor(mocker: MockFixture) -> None:
    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines.return_value = (x for x in ["test1 line x", "test2 line x"])
    mocked_pattern_matcher.match.return_value = [[MatchPosition(0, 1)], [MatchPosition(0, 1)]]
    result = LineMatchCounterProcessor(mocked_file_reader,
                                       {InputType.TEXT: mocked_pattern_matcher}).process(
        Path("path")).__next__()
    expected_result = ProcessingOutput(matches=None, path=PosixPath('path'),
                                       input_type=InputType.TEXT, line="", line_number=0,
                                       match_count=2)

    assert result == expected_result


def test_after_context_line_match_processor(mocker: MockFixture) -> None:
    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines.return_value = (x for x in ["test1 line", "test2 line", "test3 line", "test4 line"])
    mocked_pattern_matcher.match.side_effect = [[MatchPosition(0, 4)], None, None, None]

    results = list(AfterContextLineMatchProcessor(mocked_file_reader,
                                                  {InputType.TEXT: mocked_pattern_matcher},
                                                  2).process(Path("path")))

    expected_results = [
        ProcessingOutput(matches=[MatchPosition(start=0, end=4)], path=PosixPath('path'), input_type=InputType.TEXT,
                         line='test1 line', line_number=1, match_count=0),
        ProcessingOutput(matches=None, path=PosixPath('path'), input_type=InputType.TEXT, line='test2 line',
                         line_number=2, match_count=0),
        ProcessingOutput(matches=None, path=PosixPath('path'), input_type=InputType.TEXT, line='test3 line',
                         line_number=3, match_count=0)]

    assert results == expected_results


def test_before_context_line_match_processor(mocker: MockFixture) -> None:
    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines.return_value = (x for x in ["test1 line", "test2 line", "test3 line", "test4 line"])
    mocked_pattern_matcher.match.side_effect = [None, None, [MatchPosition(0, 4)], None]

    results = list(BeforeContextLineMatchProcessor(mocked_file_reader,
                                                   {InputType.TEXT: mocked_pattern_matcher},
                                                   2).process(Path("path")))

    expected_results = [
        ProcessingOutput(matches=None, path=PosixPath('path'), input_type=InputType.TEXT, line='test1 line',
                         line_number=1, match_count=0),
        ProcessingOutput(matches=None, path=PosixPath('path'), input_type=InputType.TEXT, line='test2 line',
                         line_number=2, match_count=0),
        ProcessingOutput(matches=[MatchPosition(start=0, end=4)], path=PosixPath('path'), input_type=InputType.TEXT,
                         line='test3 line', line_number=3, match_count=0),
    ]

    assert results == expected_results


def test_file_permission_error_handling(mocker: MockFixture, capsys: CaptureFixture[str]) -> None:
    def _raise_file_permission_error(path: Path) -> None:
        raise PermissionError

    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines = _raise_file_permission_error

    list(BeforeContextLineMatchProcessor(mocked_file_reader,
                                         {InputType.TEXT: mocked_pattern_matcher},
                                         2).process(Path("path")))

    captured = capsys.readouterr()
    captured_output = captured.out

    assert captured_output == "grep: path: Permission denied\n"


def test_file_not_found_error_handling(mocker: MockFixture, capsys: CaptureFixture[str]) -> None:
    def _raise_file_not_found_error(path: Path) -> None:
        raise FileNotFoundError

    mocked_file_reader = mocker.Mock()
    mocked_pattern_matcher = mocker.Mock()
    mocked_file_reader.read_lines = _raise_file_not_found_error

    list(BeforeContextLineMatchProcessor(mocked_file_reader,
                                         {InputType.TEXT: mocked_pattern_matcher},
                                         2).process(Path("path")))

    captured = capsys.readouterr()
    captured_output = captured.out

    assert captured_output == "grep: path: No such file or directory\n"
