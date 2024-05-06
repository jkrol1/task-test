from argparse import ArgumentParser
from typing import List, Type

import pytest

from python_grep.cli import get_parsed_args
from python_grep.grep.factory import create_grep_from_cli_args
from python_grep.grep.grep import (
    AfterContextLineMatchGrep,
    BeforeContextLineMatchGrep,
    Grep,
    LineMatchCounterGrep,
    LineMatchGrep,
)


@pytest.mark.parametrize(
    "grep_type_selection_option, grep_type",
    [
        ([], LineMatchGrep),
        (["-c"], LineMatchCounterGrep),
        (["-A", "4"], AfterContextLineMatchGrep),
        (["-B", "1"], BeforeContextLineMatchGrep),
    ],
)
def test_create_grep_from_cli_args(
    cli_parser: ArgumentParser,
    grep_type_selection_option: List[str],
    grep_type: Type[Grep],
) -> None:
    parsed_args = get_parsed_args(
        cli_parser,
        ["test_pattern", "test_file.txt"] + grep_type_selection_option,
    )
    grep = create_grep_from_cli_args(parsed_args)
    assert isinstance(grep, grep_type)
