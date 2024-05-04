from argparse import ArgumentParser, ArgumentTypeError, Namespace


def create_cli_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Python implementation of grep command")
    parser.add_argument("pattern", help="Pattern to search for in the file(s).")
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
        "-a", "--text", action="store_true", help="assume binary files are of type text"
    )
    parser.add_argument("--color", action="store_true", help="Enable colored output")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="prints the searched pattern in the given directory recursively in all the files",
    )
    parser.add_argument(
        "-v", "--invert-match", action="store_true", help="select non-matching lines"
    )
    parser.add_argument(
        "-w", "--word-regexp", action="store_true", help="match only whole words"
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
        "-B", "--before-context", type=int, help="print NUM lines of leading context"
    )
    parser.add_argument(
        "-A", "--after-context", type=int, help="print NUM lines of trailing context"
    )

    return parser


def merge_pattern_related_args(args: Namespace) -> Namespace:
    if args.pattern is None and args.patterns is None:
        raise ArgumentTypeError("Either -e option or pattern argument is required.")
    elif args.patterns is None:
        args.patterns = [args.pattern]
    else:
        args.files.insert(0, args.pattern)

    return args


def add_file_path_for_recursive(args: Namespace) -> Namespace:
    if not args.files and not args.recursive:
        raise ArgumentTypeError("Files argument is required")
    if not args.files and args.recursive:
        args.files.append("*")

    return args
