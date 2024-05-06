from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

from _pytest.capture import CaptureFixture

from python_grep.main import main

FILE_CONTENT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n
Sed at mauris euismod, ultricies ex at, venenatis ligula. bibendum mauris. Ut
eu arcu vitae odio varius\n ullamcorper. example1@example.com ac pellentesque
nibh.\n Curabitur sodales lobortis diam, quis vestibulum lacus faucibus eget.
Nam at ex vitae orci consequat varius.\nexample2@example.com id consectetur
lectus volutpat.\n Vestibulum ante ipsum primis in faucibus orci
example3@example.com\n Nulla vel pulvinar velit. Nam euismod justo sit amet
nunc"""


def test_e2e(
    tmp_text_file: Callable[[str], Path],
    cli_parser: ArgumentParser,
    capsys: CaptureFixture[str],
):
    file = tmp_text_file(FILE_CONTENT)
    file_path = str(file)
    main([r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", file_path])
    captured_out = capsys.readouterr().out
    expected_output = (
        f"{file_path}: ullamcorper. example1@example.com ac pellentesque"
        f"\n{file_path}:example2@example.com id consectetur"
        f"\n{file_path}:example3@example.com\n"
    )
    assert captured_out == expected_output


def test_e2e_count(
    tmp_text_file: Callable[[str], Path],
    cli_parser: ArgumentParser,
    capsys: CaptureFixture[str],
):
    file = tmp_text_file(FILE_CONTENT)
    file_path = str(file)
    main(
        [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            file_path,
            "-c",
        ]
    )
    captured_out = capsys.readouterr().out
    expected_output = f"{file_path}:3\n"
    assert captured_out == expected_output
