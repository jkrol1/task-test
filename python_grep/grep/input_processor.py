from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from queue import Full, Queue
from typing import Dict, Generator, Union

from python_grep.grep.base import IInputProcessor, ProcessingOutput
from python_grep.match import IPatternMatcher
from python_grep.storage import IFileReader, InputType

InputTypeToPatternMatcherMapping = Dict[InputType, IPatternMatcher]


class InputProcessorTemplate(IInputProcessor):
    """
    A template for input processors.

    :param IFileReader file_reader: An instance of IFileReader
     for reading files.
    :param InputTypeToPatternMatcherMapping pattern_matcher_map:
     A dictionary mapping
    InputType to IPatternMatcher.
    """

    def __init__(
        self, file_reader: IFileReader, pattern_matcher_map: Dict
    ) -> None:
        self._pattern_matcher_map = pattern_matcher_map
        self._input_type = InputType.TEXT
        self._pattern_matcher = self._pattern_matcher_map[InputType.TEXT]
        self._file_reader = file_reader
        self._file_reader.on_input_change(self._switch_input_type)

    def process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        try:
            yield from self._process(path)
        except PermissionError:
            print(f"grep: {path}: Permission denied")
        except FileNotFoundError:
            print(f"grep: {path}: No such file or directory")

    @abstractmethod
    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        """
        Internal method for actual processing of the input data.

        :param Path path: The path to the input data file.
        :yield: A generator of ProcessingOutput objects.
        :rtype: Generator[ProcessingOutput, None, None].
        """

    def _switch_input_type(self, input_type: InputType) -> None:
        """
        Switch the object's input type and pattern matcher
        for the newly read input type.

        :param InputType input_type: The new input type.
        """
        if input_type != self._input_type:
            self._pattern_matcher = self._pattern_matcher_map[input_type]
            self._input_type = input_type


class LineMatchProcessor(InputProcessorTemplate):
    """Processor for finding matching lines."""

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
    """Processor for finding and counting matching lines."""

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
    """Processor for finding matching lines with specified context."""

    def __init__(
        self,
        file_reader: IFileReader,
        pattern_matcher_map: Dict,
        context_size: int,
    ) -> None:
        super().__init__(file_reader, pattern_matcher_map)
        self._context_size = context_size


class AfterContextLineMatchProcessor(ContextualLineMatchProcessor):
    """Processor for finding matching lines with "after" context."""

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
    """Processor for finding matching lines with "before" context."""

    def _process(self, path: Path) -> Generator[ProcessingOutput, None, None]:
        queue: Queue = Queue(maxsize=self._context_size)
        for line_num, line in enumerate(self._file_reader.read_lines(path)):
            if matched_positions := self._pattern_matcher.match(line):
                while not queue.empty():
                    output_line_number = line_num - queue.qsize() + 1
                    output_line = queue.get()
                    yield ProcessingOutput(
                        matches=None,
                        path=path,
                        line_number=output_line_number,
                        line=output_line,
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
