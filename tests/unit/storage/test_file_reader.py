import re
from pathlib import Path
from typing import Callable

import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockFixture

from python_grep.storage import FileReader, InputType


@pytest.mark.parametrize(
    "file_content, peek_callable, expected_result",
    [
        (b"test test \x10", lambda x: b"\x00", b"test test \x10"),
        (b"test test \x10", lambda x: b"", "test test \x10"),
    ],
)
def test_read_file(
    open_mock_with_set_read_data: Callable[
        [bytes, Callable[[int], bytes]], None
    ],
    file_reader: FileReader,
    file_content: bytes,
    peek_callable: Callable[[int], bytes],
    expected_result,
) -> None:
    open_mock_with_set_read_data(file_content, peek_callable)
    first_read_line = file_reader.read_lines(Path("path")).__next__()
    assert first_read_line == expected_result


@pytest.mark.parametrize(
    "file_content, peek_callable, expected_input_type",
    [
        (b"test test \x10", lambda x: b"", InputType.TEXT),
        (b"test test \x10", lambda x: b"\x00", InputType.BINARY),
    ],
)
def test_on_input_change(
    open_mock_with_set_read_data: Callable[
        [bytes, Callable[[int], bytes]], None
    ],
    file_reader: FileReader,
    mocker: MockFixture,
    file_content: bytes,
    peek_callable: Callable[[int], bytes],
    expected_input_type: InputType,
) -> None:
    mock_callback = mocker.Mock()
    file_reader.before_file_traverse_hook(mock_callback)
    open_mock_with_set_read_data(file_content, peek_callable)
    file_reader.read_lines(Path("path")).__next__()

    mock_callback.assert_called_once_with(expected_input_type)


def test_unicode_decode_error_handling(
    open_mock_with_set_read_data: Callable[
        [bytes, Callable[[int], bytes]], None
    ],
    file_reader: FileReader,
    capsys: CaptureFixture[str],
) -> None:
    open_mock_with_set_read_data(b"\xff\xfe\x00\x00", lambda x: b"")
    first_read_line = file_reader.read_lines(Path("path")).__next__()
    captured = capsys.readouterr()
    captured_output = captured.out

    assert isinstance(first_read_line, bytes)
    assert (
        captured_output
        == "grep: unicode decode error. Trying to read path as binary\n"
    )


def test_handling_exception_on_is_binary_file_check(
    open_mock_with_set_read_data: Callable[
        [bytes, Callable[[int], bytes]], None
    ],
    file_reader: FileReader,
    capsys: CaptureFixture[str],
) -> None:
    def _callable_with_generic_exception_raise(_: int) -> bytes:
        raise Exception("error_msg")

    open_mock_with_set_read_data(
        b"test", _callable_with_generic_exception_raise
    )
    file_reader.read_lines(Path("path")).__next__()
    captured = capsys.readouterr()
    captured_output = captured.out

    assert re.match(r"Error checking file .*: error_msg\n", captured_output)
