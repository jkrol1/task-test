from pathlib import Path
from typing import Callable, List

import pytest
from pytest_mock import MockFixture

from storage.file_reader import FileReader


@pytest.fixture
def file_reader() -> FileReader:
    return FileReader()


@pytest.fixture
def open_mock_with_set_read_data(mocker: MockFixture) -> Callable[[bytes, Callable[[int], bytes]], None]:
    def wrapper(file_content: bytes, peek_callable: Callable[[int], bytes]) -> None:
        mocked_read_data = mocker.mock_open(read_data=file_content)
        mocked_read_data.return_value.peek = peek_callable
        mocker.patch.object(Path, "open", mocked_read_data)

    return wrapper


@pytest.fixture
def mock_pathlib_path_glob(mocker: MockFixture) -> Callable[[List[Path]], None]:
    def wrapper(paths: List[Path]):
        mock_glob = mocker.patch("pathlib.Path.glob")
        mock_glob.return_value = paths

    return wrapper


@pytest.fixture
def tmp_txt_file(tmp_path: Path) -> Callable[[str], Path]:
    def wrapper(file_content: str) -> Path:
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "temp_file.txt"
        p.write_text(file_content)
        return p

    return wrapper
