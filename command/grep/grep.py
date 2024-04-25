from __future__ import annotations

from command.base import ICommand
from command.grep.input_processor import IInputProcessor
from storage.base import IPathResolver


class Grep(ICommand):
    def __init__(self, path_resolver: IPathResolver, input_processor: IInputProcessor):
        self._path_resolver = path_resolver
        self._input_processor = input_processor

    def execute(self) -> None:
        for path in self._path_resolver.get_resolved_file_paths():
            # Return result object from input processor and pass it to specific printing function
            self._input_processor.process(path)
