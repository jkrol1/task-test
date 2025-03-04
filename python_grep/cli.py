from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import List, Optional


def create_cli_parser() -> ArgumentParser:
    """
    Create a command-line interface (CLI) parser.

    :return:The CLI parser.
    :rtype: ArgumentParser.
    """

    parser = ArgumentParser(
        description="Python implementation of grep command"
    )
    parser.add_argument(
        "pattern", help="Pattern to search for in the file(s)."
    )
    parser.add_argument("files", nargs="*", help="Files to search in")
    parser.add_argument(
        "-e",
        "--pattern",
        action="append",
        dest="patterns",
        help="Additional pattern(s) to search for",
    )
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="prints only a count of selected lines per file",
    )
    parser.add_argument(
        "-a",
        "--text",
        action="store_true",
        help="assume binary files are of type text",
    )
    parser.add_argument(
        "--color", action="store_true", help="Enable colored output"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="prints the searched pattern in the given directory "
        "recursively in all the files",
    )
    parser.add_argument(
        "-v",
        "--invert-match",
        action="store_true",
        help="select non-matching lines",
    )
    parser.add_argument(
        "-w",
        "--word-regexp",
        action="store_true",
        help="match only whole words",
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="ignore case distinctions in patterns and data",
    )
    parser.add_argument(
        "-n",
        "--line-number",
        action="store_true",
        help="print line number with output lines",
    )
    parser.add_argument(
        "-B",
        "--before-context",
        type=int,
        help="print NUM lines of leading context",
    )
    parser.add_argument(
        "-A",
        "--after-context",
        type=int,
        help="print NUM lines of trailing context",
    )

    return parser


def merge_pattern_related_args(args: Namespace) -> Namespace:
    """
    Merge pattern-related arguments into a single list.

    :param Namespace args: The namespace containing parsed arguments.
    :return: The modified namespace.
    :rtype: Namespace
    :raises ArgumentTypeError: Raises exception if no patterns are provided.
    """

    if not args.pattern and not args.patterns:
        raise ArgumentTypeError(
            "Either -e option or pattern argument is required."
        )
    elif not args.patterns:
        args.patterns = [rf"{args.pattern}"]
    elif args.patterns and args.pattern:
        if not args.files:
            args.files.insert(0, rf"{args.pattern}")
        else:
            args.patterns.append(args.pattern)

    return args


def add_file_path_for_recursive(args: Namespace) -> Namespace:
    """
    Add file path "*" for recursive search if no path was given.

    :param args: Namespace, The namespace containing parsed arguments.
    :return: Namespace, The modified namespace.
    :raises ArgumentTypeError: raises exception if is not recursive
     and no file names given
    """
    if not args.files and not args.recursive:
        raise ArgumentTypeError("Files argument is required")
    if not args.files and args.recursive:
        args.files.append("*")

    return args


def get_parsed_args(
    cli_parser: ArgumentParser, args: Optional[List[str]]
) -> Namespace:
    """
    Parses the command-line arguments using the provided
    `ArgumentParser` instance and returns a `Namespace` object
    containing the parsed arguments. Additionally,
    merges pattern-related arguments and adds file paths for
    recursive operations.

    :param ArgumentParser cli_parser: An instance of `ArgumentParser`
    configured with the desired command-line arguments and options.
    :param Optional[List[str]] args: A list of strings representing
    the command-line arguments. If None, sys.argv is used.
    :return: A `Namespace` object containing the parsed arguments,
     with pattern-related arguments merged and file paths added for
     recursive operations.
    :rtype: Namespace
    """

    return add_file_path_for_recursive(
        merge_pattern_related_args(cli_parser.parse_args(args))
    )
