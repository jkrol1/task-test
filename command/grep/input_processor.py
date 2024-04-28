from abc import abstractmethod
from queue import Full, Queue
from pathlib import Path
from typing import Callable, Union

from command.base import IInputProcessor
from match import PatternMatcher
from storage.file_reader import FileReader


class AbstractInputProcessor(IInputProcessor):
    def __init__(self, reader: FileReader, pattern_matcher: PatternMatcher, output_printer: Callable) -> None:
        self._reader = reader
        self._pattern_matcher = pattern_matcher
        self._output_printer = output_printer

    @abstractmethod
    def process(self, path: Path) -> None:
        pass


class LineMatchProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        for line in self._reader.read_lines(path):
            if isinstance(line, str):
                if matched_positions := self._pattern_matcher.match_string(line):
                    self._output_printer(path, line, matched_positions)
            else:
                if self._pattern_matcher.match_bytes(line):
                    self._output_printer(path, line)


class LineMatchCounterProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        # It counts just the lines and not each match
        match_count = 0
        for line in self._reader.read_lines(path):
            if isinstance(line, str):
                if self._pattern_matcher.match_string(line):
                    match_count += 1
            else:
                if self._pattern_matcher.match_bytes(line):
                    match_count += 1

        self._output_printer(path, match_count)


class BeforeContextLineMatchProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        desired_size = 3
        queue = Queue(maxsize=desired_size)  # Need to pass it from the cli
        for line in self._reader.read_lines(path):
            if isinstance(line, str):
                if matched_positions := self._pattern_matcher.match_string(line):
                    while not queue.empty():
                        self._output_printer(path, queue.get())
                    self._output_printer(path, line, matched_positions)
                else:
                    self._add_line_to_queue(line, queue)
            else:
                if self._pattern_matcher.match_bytes(line):
                    while not queue.empty():
                        self._output_printer(path, queue.get())
                    self._output_printer(path, line)
                else:
                    self._add_line_to_queue(line, queue)

    @staticmethod
    def _add_line_to_queue(line: str, queue: Queue[Union[str, bytes]]):
        try:
            queue.put(line, block=False)
        except Full:
            queue.get()
            queue.put(line, block=False)


class AfterContextLineMatchProcessor(AbstractInputProcessor):
    def process(self, path: Path) -> None:
        lines_to_print = 3
        current_lines_to_print = 0
        for line in self._reader.read_lines(path):
            if isinstance(line, str):
                if matched_positions := self._pattern_matcher.match_string(line):
                    self._output_printer(path, line, matched_positions)
                    current_lines_to_print = lines_to_print
                elif current_lines_to_print:
                    self._output_printer(path, line)
                    current_lines_to_print -= 1
            else:
                if self._pattern_matcher.match_bytes(line):
                    self._output_printer(path, line)
                    current_lines_to_print = lines_to_print
                elif current_lines_to_print:
                    self._output_printer(path, line)
                    current_lines_to_print -= 1
