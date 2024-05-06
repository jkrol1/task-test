from pathlib import Path
from typing import Callable, List

from _pytest.capture import CaptureFixture
from pytest_mock import MockFixture

from storage.path_resolver import PathResolver


def test_get_resolved_file_paths(
    mock_pathlib_path_glob: Callable[[List[Path]], None]
) -> None:
    mock_pathlib_path_glob([Path("test1.txt"), Path("test2.txt")])
    path_resolver = PathResolver(["*.txt"])
    resolved_paths = list(path_resolver.get_resolved_file_paths())
    expected_files = [
        Path("test1.txt"),
        Path("test2.txt"),
    ]

    assert all(path in resolved_paths for path in expected_files)


def test_is_dir_message_on_path_resolving(
    mock_pathlib_path_glob: Callable[[List[Path]], None],
    mocker: MockFixture,
    capsys: CaptureFixture[str],
):
    mock_pathlib_path_glob([Path("test1")])
    path_resolver = PathResolver(["test1"])
    mock = mocker.patch("pathlib.Path.is_dir")
    mock.return_value = True
    list(path_resolver.get_resolved_file_paths())
    captured = capsys.readouterr()
    captured_output = captured.out

    assert captured_output == "grep: test1 is a directory\n"
