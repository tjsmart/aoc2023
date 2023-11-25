from __future__ import annotations

import os
import subprocess
import sys
import urllib.request
from argparse import ArgumentParser
from collections.abc import Sequence

from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_cookie_headers
from ._helpers import get_year
from ._helpers import HandledError
from ._helpers import THIS_DIR
from ._prompt_html_parser import parse_prompt_html_to_md


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(description="Generate files for next day/part.")
    _ = parser.parse_args(argv)

    try:
        _main()
    except (HandledError, subprocess.CalledProcessError) as ex:
        print("error:", ex)
        return 1

    return 0


def _main() -> None:
    year = get_year()
    prev, next = _get_prev_and_next()

    create_next_files(year, next, prev)

    sys.stdout.flush()
    os.execlp(
        "bash",
        "bash",
        "-c",
        (
            f"{sys.executable} -m pip install -e . -qqq"
            f" & nvim -O {next.pyfile} {next.inputfile}"
        ),
    )


def create_next_files(year: int, next: DayPart, prev: DayPart | None) -> None:
    print(f"Generating files for day {next.day} part {next.part}:")

    next.outdir.mkdir(exist_ok=True, parents=True)
    print(f"... {next.outdir} created ✅")

    assert not next.pyfile.exists(), f"Whoops, {next.pyfile} already exists!"

    if not prev:
        prev_src = (THIS_DIR / "template_part.py").read_text()
    else:
        prev_src = prev.pyfile.read_text()

    next.pyfile.write_text(prev_src)
    print(f"... {next.pyfile} written ✅")

    (next.outdir / "__init__.py").touch(exist_ok=True)

    if next.part == 1:
        _download_input(year, next)

    _download_prompt(year, next)

    print(f"All finished, AOC day {next.day} part {next.part} is ready! 🎉")


def _download_input(year: int, dp: DayPart) -> None:
    dp.outdir.mkdir(exist_ok=True, parents=True)

    input = _get_input(year, dp.day)
    dp.inputfile.write_text(input)
    print(f"... {dp.inputfile} written ✅")


def _get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = urllib.request.Request(url, headers=get_cookie_headers())
    output = urllib.request.urlopen(req).read().decode().strip()
    print(f"... {url} fetched ✅")
    return output


def _download_prompt(year: int, dp: DayPart) -> None:
    dp.outdir.mkdir(exist_ok=True, parents=True)

    prompt = _get_prompt(year, dp.day)
    dp.promptfile.write_text(prompt)
    print(f"... {dp.promptfile} written ✅")


def _get_prompt(year: int, day: int) -> str:
    html = _get_prompt_html(year, day)
    return parse_prompt_html_to_md(html)


def _get_prompt_html(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}"
    req = urllib.request.Request(url, headers=get_cookie_headers())
    output = urllib.request.urlopen(req).read().decode().strip()
    print(f"... {url} fetched ✅")
    return output


def _get_prev_and_next() -> tuple[DayPart | None, DayPart]:
    dps = get_all_dayparts()
    prev = dps[-1] if dps else None
    next = prev.next() if prev else DayPart.first()
    return prev, next


if __name__ == "__main__":
    raise SystemExit(main())
