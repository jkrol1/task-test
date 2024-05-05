from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture
def tmp_txt_file(tmp_path: Path) -> Callable[[str], Path]:
    def wrapper(file_content: str) -> Path:
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "temp_file.txt"
        p.write_text(file_content)
        return p

    return wrapper
