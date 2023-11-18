from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from argparse import ArgumentParser
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple


THIS_DIR = Path(__file__).resolve().parent
PARTFILE = re.compile(r".*/day(\d\d)/part\d\.py")


class DayPart(NamedTuple):
    day: int
    part: int


class HandledError(RuntimeError):
    ...


@lru_cache(maxsize=1)
def _get_rootdir() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout)


def _get_year() -> int:
    rootdir = _get_rootdir()
    *_, year = rootdir.name.partition("aoc")
    try:
        return int(year)
    except ValueError:
        raise HandledError(
            f"failed to parse year from rootdir name: {rootdir.name}, expected"
            " name to be of the form 'aoc[year]', e.g., 'aoc2023'"
        )


def _get_prev_daypart() -> DayPart | None:
    root_dir = _get_rootdir()
    prev = (0, 2)
    for dd in root_dir.glob("day*/part*.py"):
        m = PARTFILE.search(str(dd))
        if not m:
            continue

        other = tuple(map(int, m.groups()))
        prev = max(prev, other)

    if prev == (0, 2):
        return None

    return DayPart(*prev)


def _get_next_daypart(prev: DayPart | None) -> DayPart:
    if prev == (25, 2):
        raise HandledError("It's over, go home!")

    if prev is None:
        return DayPart(1, 1)

    if prev[1] == 1:
        next = prev[0], prev[1] + 1
    elif prev[1] == 2:
        next = prev[0] + 1, 1
    else:
        raise HandledError(f"Last day/part was invalid: {prev[0]}/{prev[1]}")

    return DayPart(*next)


def create_next_files(year: int, next: DayPart, prev: DayPart | None) -> None:
    print(f"Generating files for day {next.day} part {next.part}...")

    outdir = _get_outdir(next.day)
    outdir.mkdir(exist_ok=True, parents=True)
    print(f"...{outdir} created ✅")

    nextfile = _get_pyfile(next)
    assert not nextfile.exists(), f"Whoops, {nextfile} already exists!"

    if not prev:
        prevfile = THIS_DIR / "template_part.py"
    else:
        prevfile = _get_pyfile(next)

    nextfile.write_text(prevfile.read_text())
    print(f"...{nextfile} written ✅")

    (outdir / "__init__.py").touch(exist_ok=True)

    if next.part == 1:
        _download_input(year, next.day)

    print(f"All finished, AOC day {next.day} part {next.part} is ready!")


def _get_pyfile(dp: DayPart) -> Path:
    return _get_outdir(dp.day) / f"part{dp.part}.py"


def _download_input(year: int, day: int) -> None:
    outdir = _get_outdir(day)
    outdir.mkdir(exist_ok=True, parents=True)

    input = _get_input(year, day)
    inputfile = outdir / "input.txt"
    inputfile.write_text(input)
    print(f"...{inputfile} written ✅")


def _get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {"Cookie": _get_cookie()}
    req = urllib.request.Request(url, headers=headers)
    output = urllib.request.urlopen(req).read().decode()
    print(f"...{url} fetched ✅")
    return output


def _get_cookie() -> str:
    session_file = _get_rootdir() / ".session"
    return f"session={session_file.read_text().strip()}"


def _get_outdir(day: int) -> Path:
    return _get_rootdir() / f"day{day:02}"


def _main() -> None:
    year = _get_year()
    prev = _get_prev_daypart()
    next = _get_next_daypart(prev)

    create_next_files(year, next, prev)

    nextfile = _get_pyfile(next)
    inputfile = _get_outdir(next.day) / "input.txt"

    os.execlp("nvim", f"-O {nextfile} {inputfile}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(description="Generate files for next day/part.")
    _ = parser.parse_args(argv)

    try:
        _main()
    except (HandledError, subprocess.CalledProcessError) as ex:
        print("error:", ex, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
