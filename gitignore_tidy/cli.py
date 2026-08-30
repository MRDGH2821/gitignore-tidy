import enum
import pathlib
import typing

import typer

from gitignore_tidy.core import tidy_file

app = typer.Typer()


class NegationsLast(str, enum.Enum):
    group = "group"
    eof = "eof"


@app.command()
def tidy_files(
    files: typing.Optional[list[pathlib.Path]] = typer.Argument(
        None,
        help="""\
        Paths to one or more gitignore files.
        If not supplied, the .gitignore in the current
        working directory will be assumed.
        """,
    ),
    allow_leading_whitespace: bool = typer.Option(
        False,
        help="Whether or not to allow trailing whitespaces in file names",
    ),
    negations_last: typing.Optional[NegationsLast] = typer.Option(
        None,
        "--negations-last",
        help="""\
        Move negating entries (leading '!') to the end when sorting.
        'group' puts them at the end of their section, 'eof' collects all of
        them into a single block at the end of the file. CAUTION: unlike the
        default, this can change which paths your .gitignore matches.
        """,
    ),
):
    """
    Tidy .gitignore files
    """
    if files is None or len(files) < 1:
        files = [pathlib.Path(".gitignore")]
    mode = negations_last.value if negations_last is not None else None
    [
        tidy_file(
            file,
            allow_leading_whitespace=allow_leading_whitespace,
            negations_last=mode,
        )
        for file in files
    ]
