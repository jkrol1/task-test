from typing import List, Optional

from cli import create_cli_parser, merge_pattern_related_args
from command.grep.factory import create_grep_from_cli_args


def main(args: Optional[List[str]] = None) -> None:
    cli_parser = create_cli_parser()
    parsed_args = merge_pattern_related_args(cli_parser.parse_args(args))
    grep = create_grep_from_cli_args(parsed_args)
    grep.execute()


if __name__ == "__main__":
    main()
