import os
from pathlib import Path
from typing import Iterator


def traverse_directories(path: Path) -> Iterator[Path]:
    for root, dirs, files in os.walk(str(path)):
        for file in files:
            yield Path(root, file)


def get_absolute_path(path: str) -> Path:
    pathlib_path = Path(path)

    return (
        pathlib_path
        if pathlib_path.is_absolute()
        else pathlib_path.resolve()
    )


def resolve_patterns(path: Path) -> Iterator[Path]:
    return path.parent.glob(path.name)
