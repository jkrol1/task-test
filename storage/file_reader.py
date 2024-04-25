from pathlib import Path
from typing import Generator, BinaryIO

from storage.base import DEFAULT_ENCODING, IFileReader, IOType


class FileReader(IFileReader):

    def __init__(self, encoding: str = DEFAULT_ENCODING):
        self._encoding = encoding

    def read_lines(self, path: Path) -> Generator[IOType, None, None]:
        try:
            return self._read_lines(path)
        except PermissionError:
            print(f"grep: {path}: Permission denied")
        except FileNotFoundError:
            print(f"grep: {path}: No such file or directory")

    def _read_lines(self, path: Path) -> Generator[IOType, None, None]:
        try:
            with path.open("rb") as file:
                if self._is_binary_file(file):
                    yield from self._read_as_binary(file)
                else:
                    yield from self._read_as_text(file)
        except UnicodeDecodeError:
            yield from self._read_as_binary(file)

    @staticmethod
    def _is_binary_file(file: BinaryIO) -> bool:
        try:
            data = file.peek(1024)  # Peek at the first 1024 bytes
            if b'\x00' in data:
                return True
        except Exception as e:
            print(f"Error checking file: {e}")
        return False

    def _read_as_text(self, file) -> Generator[str, None, None]:
        file.seek(0)
        with file:
            for line in file:
                yield line.decode(self._encoding).rstrip('\n')

    @staticmethod
    def _read_as_binary(file) -> Generator[bytes, None, None]:
        file.seek(0)
        with file:
            for line in file:
                yield line
