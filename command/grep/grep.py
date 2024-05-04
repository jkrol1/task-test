from __future__ import annotations

from abc import ABC, abstractmethod

from command.base import ICommand, IInputProcessor
from command.grep.exceptions import SuppressBinaryOutputError
from command.grep.input_processor import (
    InputTypeToPatternMatcherMapping,
    LineMatchProcessor,
    LineMatchCounterProcessor,
    BeforeContextLineMatchProcessor,
    AfterContextLineMatchProcessor,
)
from command.grep.output import CreateOutputMessage
from storage.base import IPathResolver, IFileReader


class Grep(ICommand, ABC):
    def __init__(
        self,
        file_reader: IFileReader,
        path_resolver: IPathResolver,
        create_output_message: CreateOutputMessage,
        file_type_to_pattern_matcher_map: InputTypeToPatternMatcherMapping,
        context,
    ) -> None:
        self._file_reader = file_reader
        self._path_resolver = path_resolver
        self._create_output_message = create_output_message
        self._file_type_to_pattern_matcher_map = file_type_to_pattern_matcher_map
        self._context = context

    def execute(self) -> None:
        input_processor = self.create_input_processor()
        for path in self._path_resolver.get_resolved_file_paths():
            try:
                for result in input_processor.process(path):
                    output_message = self._create_output_message(result, self._context)
                    print(output_message)
            except SuppressBinaryOutputError:
                print(f"Binary file {path} matches")

    @abstractmethod
    def create_input_processor(self) -> IInputProcessor:
        pass


class LineMatchGrep(Grep):
    def create_input_processor(self) -> IInputProcessor:
        return LineMatchProcessor(
            self._file_reader, self._file_type_to_pattern_matcher_map
        )


class LineMatchCounterGrep(Grep):
    def create_input_processor(self) -> IInputProcessor:
        return LineMatchCounterProcessor(
            self._file_reader, self._file_type_to_pattern_matcher_map
        )


class BeforeContextLineMatchGrep(Grep):
    def create_input_processor(self) -> IInputProcessor:
        return BeforeContextLineMatchProcessor(
            self._file_reader,
            self._file_type_to_pattern_matcher_map,
            self._context.context_control_options.before_context,
        )


class AfterContextLineMatchGrep(Grep):
    def create_input_processor(self) -> IInputProcessor:
        return AfterContextLineMatchProcessor(
            self._file_reader,
            self._file_type_to_pattern_matcher_map,
            self._context.context_control_options.after_context,
        )
