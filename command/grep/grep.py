from __future__ import annotations

from abc import ABC, abstractmethod

from command.base import ICommand
from command.grep.base import IInputProcessor
from command.grep.context import Context
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
    """
    Grep implementation.

    :param IFileReader file_reader: An instance of the file reader.
    :param IPlathResolver path_resolver: An instance of the path resolver.
    :param CreateOutputMessage create_output_message: A function to
    create output messages.
    :param InputTypeToPatternMatcherMapping file_type_to_pattern_matcher_map:
    Mapping of input types to pattern matchers.
    :param Context context: The context object containing options and
    controls for grep.
    """

    def __init__(
            self,
            file_reader: IFileReader,
            path_resolver: IPathResolver,
            create_output_message: CreateOutputMessage,
            file_type_to_pattern_matcher_map: InputTypeToPatternMatcherMapping,
            context: Context,
    ) -> None:
        self._file_reader = file_reader
        self._path_resolver = path_resolver
        self._create_output_message = create_output_message
        self._file_type_to_pattern_matcher_map = (
            file_type_to_pattern_matcher_map
        )
        self._context = context

    def execute(self) -> None:
        input_processor = self.create_input_processor()
        for path in self._path_resolver.get_resolved_file_paths():
            try:
                for result in input_processor.process(path):
                    output_message = self._create_output_message(
                        result, self._context
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
            self._context.context_control_options.before_context,
        )


class AfterContextLineMatchGrep(Grep):
    """A grep command for after context line matching."""

    def create_input_processor(self) -> IInputProcessor:
        return AfterContextLineMatchProcessor(
            self._file_reader,
            self._file_type_to_pattern_matcher_map,
            self._context.context_control_options.after_context,
        )
