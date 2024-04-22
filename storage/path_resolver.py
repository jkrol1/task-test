import os
from pathlib import Path
from typing import Generator, List


class PathResolver:
    def __init__(self, file_paths: List[str], include_hidden: bool = False, recursive: bool = False) -> None:
        self._file_paths = file_paths
        self._include_hidden = include_hidden
        self._recursive = recursive

    def get_resolved_file_paths(self) -> Generator[Path, None, None]:
        for path in self._file_paths:
            abs_path = get_absolute_path(path)
            yield from self._get_resolved_path_from_absolute_path(abs_path)

    def _get_resolved_path_from_absolute_path(self, absolute_path: Path) -> Generator[Path, None, None]:
        for resolved_path in resolve_patterns(absolute_path):
            yield from self._process_resolved_path(resolved_path)

    def _process_resolved_path(self, resolved_path: Path) -> Generator[Path, None, None]:
        if resolved_path.name.startswith(".") and not self._include_hidden:
            return
        elif resolved_path.is_dir():
            if self._recursive:
                yield from get_paths_from_dirs_recursively(resolved_path)
            else:
                print(f"grep: {resolved_path.name} is a directory")
        else:
            yield resolved_path


def get_paths_from_dirs_recursively(dir_path: Path) -> Generator[Path, None, None]:
    for root, dirs, files in os.walk(str(dir_path)):
        for file in files:
            yield Path(root, file)


def get_absolute_path(path: str) -> Path:
    pathlib_path = Path(path)

    return (
        pathlib_path
        if pathlib_path.is_absolute()
        else pathlib_path.resolve()
    )


def resolve_patterns(path: Path) -> Generator[Path, None, None]:
    return path.parent.glob(path.name)
