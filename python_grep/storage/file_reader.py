from io import BufferedReader
from pathlib import Path
from typing import Callable, Generator, Optional, Union

from python_grep.storage.base import DEFAULT_ENCODING, IFileReader, InputType


class FileReader(IFileReader):
    """
    A file reader implementation for reading text and binary files.

    :param str encoding: The encoding to use for reading text files.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING) -> None:
        self._encoding = encoding
        self._on_input_change: Optional[Callable[[InputType], None]] = None

    def on_input_change(self, callback: Callable[[InputType], None]) -> None:
        self._on_input_change = callback

    def read_lines(
        self, path: Path
    ) -> Generator[Union[str, bytes], None, None]:
        try:
            yield from self._read_lines(path)
        except UnicodeDecodeError:
            with path.open("rb") as file:
                print(
                    f"grep: unicode decode error. "
                    f"Trying to read {path} as binary"
                )
                yield from self._read_as_binary(file)

    def _read_lines(
        self, path: Path
    ) -> Generator[Union[str, bytes], None, None]:
        with path.open("rb") as file:
            if self._is_binary_file(file):
                yield from self._read_as_binary(file)
            else:
                yield from self._read_as_text(file)

    @staticmethod
    def _is_binary_file(file: BufferedReader) -> bool:
        try:
            data = file.peek(1024)
            if b"\x00" in data:
                return True
        except Exception as e:
            print(f"Error checking file {file.name}: {e}")
        return False

    def _read_as_text(self, file) -> Generator[str, None, None]:
        file.seek(0)
        self._notify_on_input_change(InputType.TEXT)
        for line in file:
            yield line.decode(self._encoding).rstrip("\n")

    def _read_as_binary(self, file) -> Generator[bytes, None, None]:
        file.seek(0)
        self._notify_on_input_change(InputType.BINARY)
        for line in file:
            yield line

    def _notify_on_input_change(self, file_type: InputType) -> None:
        if self._on_input_change:
            self._on_input_change(file_type)
