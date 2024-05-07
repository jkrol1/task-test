from __future__ import annotations

from abc import ABC, abstractmethod

from python_grep.grep.base import (
    ICommand,
    IInputProcessor,
    IOutputMessageBuilder,
)
from python_grep.grep.context import Context
from python_grep.grep.exceptions import SuppressBinaryOutputError
from python_grep.grep.input_processor import (
    AfterContextLineMatchProcessor,
    BeforeContextLineMatchProcessor,
    InputTypeToPatternMatcherMapping,
    LineMatchCounterProcessor,
    LineMatchProcessor,
)
from python_grep.storage.base import IFileReader, IPathResolver


class Grep(ICommand, ABC):
    """
    Grep implementation.

    :param IFileReader file_reader: An instance of the file reader.
    :param IPlathResolver path_resolver: An instance of the path resolver.
    :param IOutputMessageBuilder output_message_builder: An instance
    of concrete output message builder.
    :param InputTypeToPatternMatcherMapping file_type_to_pattern_matcher_map:
    Mapping of input types to pattern matchers.
    :param Context context: The context object containing options and
    controls for grep.
    """

    def __init__(
        self,
        file_reader: IFileReader,
        path_resolver: IPathResolver,
        output_message_builder: IOutputMessageBuilder,
        file_type_to_pattern_matcher_map: InputTypeToPatternMatcherMapping,
        context: Context,
    ) -> None:
        self._file_reader = file_reader
        self._path_resolver = path_resolver
        self._output_message_builder = output_message_builder
        self._file_type_to_pattern_matcher_map = (
            file_type_to_pattern_matcher_map
        )
        self._context = context

    def execute(self) -> None:
        input_processor = self.create_input_processor()
        for path in self._path_resolver.get_resolved_file_paths():
            try:
                for result in input_processor.process(path):
                    output_message = self._output_message_builder.create(
                        result
                    )
                    print(output_message)
            except SuppressBinaryOutputError:
                print(f"Binary file {path} matches")

    @abstractmethod
    def create_input_processor(self) -> IInputProcessor:
        """
        Create an input processor for the grep command.

        :return: An instance of the input processor.
        :rtype: IInputProcessor.
        """
        pass


class LineMatchGrep(Grep):
    """A grep for line matching"""

    def create_input_processor(self) -> IInputProcessor:
        return LineMatchProcessor(
            self._file_reader, self._file_type_to_pattern_matcher_map
        )


class LineMatchCounterGrep(Grep):
    """A grep command for line match counting."""

    def create_input_processor(self) -> IInputProcessor:
        return LineMatchCounterProcessor(
            self._file_reader, self._file_type_to_pattern_matcher_map
        )


class BeforeContextLineMatchGrep(Grep):
    """A grep command for before context line matching."""

    def create_input_processor(self) -> IInputProcessor:
        return BeforeContextLineMatchProcessor(
            self._file_reader,
            self._file_type_to_pattern_matcher_map,
            self._context.context_control_options,
        )


class AfterContextLineMatchGrep(Grep):
    """A grep command for after context line matching."""

    def create_input_processor(self) -> IInputProcessor:
        return AfterContextLineMatchProcessor(
            self._file_reader,
            self._file_type_to_pattern_matcher_map,
            self._context.context_control_options,
        )
