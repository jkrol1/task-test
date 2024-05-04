from typing import List, Optional

from cli import (
    add_file_path_for_recursive,
    create_cli_parser,
    merge_pattern_related_args,
)
from command.grep.factory import create_grep_from_cli_args


def main(args: Optional[List[str]] = None) -> None:
    cli_parser = create_cli_parser()
    parsed_args = add_file_path_for_recursive(
        merge_pattern_related_args(cli_parser.parse_args(args))
    )
    grep = create_grep_from_cli_args(parsed_args)
    grep.execute()


if __name__ == "__main__":
    main()
