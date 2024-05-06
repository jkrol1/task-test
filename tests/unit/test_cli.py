from argparse import Namespace, ArgumentTypeError

import pytest

from cli import merge_pattern_related_args, add_file_path_for_recursive


def test_merge_pattern_related_args_only_pattern() -> None:
    args = merge_pattern_related_args(Namespace(pattern="test", patterns=None))
    assert args.patterns == ["test"]


def test_merge_pattern_related_args_only_option_e() -> None:
    args = merge_pattern_related_args(
        Namespace(
            pattern=None, patterns=["pattern1", "pattern2"], files=["test.txt"]
        )
    )
    assert args.patterns == ["pattern1", "pattern2"]


def test_merge_pattern_related_args_no_pattern_or_option_e() -> None:
    with pytest.raises(ArgumentTypeError):
        merge_pattern_related_args(Namespace(pattern=None, patterns=None))


def test_add_file_path_for_recursive_no_files_not_recursive() -> None:
    with pytest.raises(ArgumentTypeError):
        add_file_path_for_recursive(Namespace(files=[], recursive=False))


def test_add_file_path_for_recursive_no_files_but_recursive() -> None:
    args = add_file_path_for_recursive(Namespace(files=[], recursive=True))
    assert args.files == ["*"]
