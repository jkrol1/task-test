from __future__ import annotations

from abc import abstractmethod, ABC
from queue import Full, Queue
from pathlib import Path
from typing import Dict, Generator, Union

from command.base import IInputProcessor, ProcessingOutput
from match import IPatternMatcher
from storage.base import InputType
from storage.file_reader import IFileReader

InputTypeToPatternMatcherMapping = Dict[InputType, IPatternMatcher]


class InputProcessorTemplate(IInputProcessor):
    def __init__(self, file_reader: IFileReader, pattern_matcher_map: Dict) -> None:
        self._pattern_matcher_map = pattern_matcher_map
        self._input_type = InputType.TEXT
        self._pattern_matcher = self._pattern_matcher_map[InputType.TEXT]
        self._file_reader = file_reader
        self._file_reader.on_input_type_change(self._switch_input_type)

    def process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        try:
            yield from self._process(path)
        except PermissionError:
            print(f"grep: {path}: Permission denied")
        except FileNotFoundError:
            print(f"grep: {path}: No such file or directory")

    @abstractmethod
    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        pass

    def _switch_input_type(self, file_type: InputType):
        if file_type != self._input_type:
            self._pattern_matcher = self._pattern_matcher_map[file_type]
            self._input_type = file_type


class LineMatchProcessor(InputProcessorTemplate):
    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        for line_num, line in enumerate(self._file_reader.read_lines(path)):
            if matched_positions := self._pattern_matcher.match(line):
                yield ProcessingOutput(
                    matches=matched_positions,
                    path=path,
                    line=line,
                    line_number=line_num + 1,
                    input_type=self._input_type,
                )


class LineMatchCounterProcessor(InputProcessorTemplate):
    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        match_count = 0
        for line in self._file_reader.read_lines(path):
            if self._pattern_matcher.search(line):
                match_count += 1
        yield ProcessingOutput(
            matches=None,
            path=path,
            input_type=self._input_type,
            line="",
            line_number=0,
            match_count=match_count,
        )


class ContextualLineMatchProcessor(InputProcessorTemplate, ABC):
    def __init__(
        self, file_reader: IFileReader, pattern_matcher_map: Dict, context_size: int
    ):
        super().__init__(file_reader, pattern_matcher_map)
        self._context_size = context_size


class AfterContextLineMatchProcessor(ContextualLineMatchProcessor):

    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        current_lines_to_print = 0
        for line_num, line in enumerate(self._file_reader.read_lines(path)):
            if matched_positions := self._pattern_matcher.match(line):
                yield ProcessingOutput(
                    matches=matched_positions,
                    path=path,
                    line=line,
                    input_type=self._input_type,
                    line_number=line_num + 1,
                )
                current_lines_to_print = self._context_size
            elif current_lines_to_print:
                yield ProcessingOutput(
                    matches=None,
                    path=path,
                    line=line,
                    input_type=self._input_type,
                    line_number=line_num + 1,
                )
                current_lines_to_print -= 1


class BeforeContextLineMatchProcessor(ContextualLineMatchProcessor):
    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        queue: Queue = Queue(maxsize=self._context_size)
        for line_num, line in enumerate(self._file_reader.read_lines(path)):
            if matched_positions := self._pattern_matcher.match(line):
                while not queue.empty():
                    yield ProcessingOutput(
                        matches=None,
                        path=path,
                        line=queue.get(),
                        line_number=line_num - queue.qsize() + 1,
                        input_type=self._input_type,
                    )
                yield ProcessingOutput(
                    matches=matched_positions,
                    path=path,
                    line=line,
                    line_number=line_num + 1,
                    input_type=self._input_type,
                )
            else:
                self._add_line_to_queue(line, queue)

    @staticmethod
    def _add_line_to_queue(line: str, queue: Queue[Union[str, bytes]]) -> None:
        try:
            queue.put(line, block=False)
        except Full:
            queue.get()
            queue.put(line, block=False)
