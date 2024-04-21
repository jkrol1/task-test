from pathlib import Path
from typing import Iterator

from storage.base.reader import IFileReader


class TextFormatReader(IFileReader):
    def read_lines(self, path: Path) -> Iterator[str]:
        try:
            with path.open("r") as file:
                for line in file:
                    yield line
        except UnicodeDecodeError:
            pass
