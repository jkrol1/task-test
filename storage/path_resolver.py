import os
from pathlib import Path
from typing import Generator, List

from storage.base import IPathResolver


class PathResolver(IPathResolver):
    """
    A path resolver implementation for resolving file paths.

    :param List[str] file_paths: A list of file path patterns.
    :param bool include_hidden: Flag indicating whether to include hidden files (default is True).
    :param bool recursive: Flag indicating whether to recursively search for files in directories (default is False).
    """

    def __init__(
            self,
            file_paths: List[str],
            recursive: bool = False,
            include_hidden: bool = True,
    ) -> None:
        self._file_paths = file_paths
        self._recursive = recursive
        self._include_hidden = include_hidden

    def get_resolved_file_paths(self) -> Generator[Path, None, None]:
        for path_str in self._file_paths:
            yield from self._get_resolved_path(Path(path_str))

    def _get_resolved_path(self, absolute_path: Path) -> Generator[Path, None, None]:
        for resolved_path in self._resolve_patterns(absolute_path):
            yield from self._process_resolved_path(resolved_path)

    def _process_resolved_path(
            self, resolved_path: Path
    ) -> Generator[Path, None, None]:
        if resolved_path.name.startswith(".") and not self._include_hidden:
            return
        elif resolved_path.is_dir():
            if self._recursive:
                yield from self._get_paths_from_dirs_recursively(resolved_path)
            else:
                print(f"grep: {resolved_path.name} is a directory")
        else:
            yield resolved_path

    @staticmethod
    def _get_paths_from_dirs_recursively(dir_path: Path) -> Generator[Path, None, None]:
        for root, dirs, files in os.walk(str(dir_path)):
            for file in files:
                yield Path(root, file)

    @staticmethod
    def _resolve_patterns(path: Path) -> Generator[Path, None, None]:
        return path.parent.glob(path.name)
