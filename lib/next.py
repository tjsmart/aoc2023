from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from argparse import ArgumentParser
from collections.abc import Sequence
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import NoReturn

from ._calendar_html_parser import parse_calendar_stars_html_to_star_count
from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_cookie_headers
from ._helpers import get_rootdir
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

    _check_if_ready(year, next)

    create_next_files(year, next, prev)
    _open(next)


def _check_if_ready(year: int, next: DayPart) -> None:
    released_at = datetime(year=year, month=12, day=next.day, hour=0)
    while True:
        estnow = datetime.utcnow() - timedelta(hours=5)
        time_to_wait = released_at - estnow
        if time_to_wait.total_seconds() < 5:
            return

        if time_to_wait >= timedelta(hours=1):
            hours_to_wait = time_to_wait.total_seconds() / (60 * 60)
            raise HandledError(
                f"Still have a long time to wait: {hours_to_wait:.1f} hours"
            )

        wait_str = _format_timedelta(time_to_wait)
        print(f"waiting for the next input to go live! {wait_str}", end="\r")
        time.sleep(1)


def _format_timedelta(td: timedelta) -> str:
    seconds = int(td.total_seconds())
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def _open(next: DayPart) -> NoReturn:
    _configure_harpoon_files(next)

    lines = next.promptfile.read_text().splitlines()
    for startline, line in reversed(list(enumerate(lines, 1))):
        if line.startswith("## "):
            break
    else:
        startline = 1

    sys.stdout.flush()
    os.execlp(
        "bash",
        "bash",
        "-c",
        (
            f"{sys.executable} -m pip install -e . -qqq"
            f" & nvim -c '{startline}' {next.promptfile}"
        ),
    )


def _configure_harpoon_files(next: DayPart) -> None:
    harpoon_json_file = Path().home() / ".local" / "share" / "nvim" / "harpoon.json"
    try:
        data = json.loads(harpoon_json_file.read_text())
        repodir = str(get_rootdir())

        data['projects'][repodir]['mark']['marks'] = [
            {'col': 0, 'row': 0, 'filename': str(next.promptfile.relative_to(repodir))},
            {'col': 0, 'row': 0, 'filename': str(next.pyfile.relative_to(repodir))},
            {'col': 0, 'row': 0, 'filename': str(next.inputfile.relative_to(repodir))},
        ]

        harpoon_json_file.write_text(json.dumps(data))

    except Exception as ex:
        print(f"... bummer, couldn't find the harpoon configuration file: {ex}")


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
    _download_calendar(year)

    print(f"All finished, AOC day {next.day} part {next.part} is ready! 🎉")


def _download_input(year: int, dp: DayPart) -> None:
    dp.outdir.mkdir(exist_ok=True, parents=True)

    while True:
        try:
            input = _get_input(year, dp.day)
        except urllib.error.URLError:
            print("... waiting 😴 for input to be ready ...")
            time.sleep(1)
            continue
        else:
            break

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


def _download_calendar(year: int) -> None:
    readme_md = get_rootdir() / "README.md"

    html = _get_home_html(year)
    stars = parse_calendar_stars_html_to_star_count(html)
    _update_readme_stars(readme_md, stars)

    print(f"... {readme_md} written ✅")


def _get_home_html(year: int) -> str:
    url = f"https://adventofcode.com/{year}"
    req = urllib.request.Request(url, headers=get_cookie_headers())
    output = urllib.request.urlopen(req).read().decode().strip()
    print(f"... {url} fetched ✅")
    return output


def _update_readme_stars(readme_md: Path, stars: list[int]) -> None:
    if readme_md.exists():
        lines = readme_md.read_text().splitlines()
    else:
        lines = []

    starting_lines, ending_lines = _partition_md_on_table(lines)
    new_table = _star_count_to_md_table(stars)

    new_lines = starting_lines + new_table + ending_lines
    readme_md.write_text("\n".join(new_lines))


def _partition_md_on_table(lines: list[str]) -> tuple[list[str], list[str]]:
    try:
        starting_idx = lines.index("|  day  | stars |")
    except ValueError:
        return lines, []

    for ending_idx, line in enumerate(lines):
        if ending_idx <= starting_idx:
            continue
        if not line.startswith("| "):
            break
    else:
        assert False, f"Failed to parse readme table?: {"\n".join(lines)}"

    return lines[:starting_idx], lines[ending_idx:]


def _star_count_to_md_table(stars: list[int]) -> list[str]:
    header = "|  day  | stars |\n| ----- | ----- | "
    row = "|   {day:02d}  |{stars}|"
    lines = [header]
    count_to_str = ["   --  ", "  ⭐-  ", "  ⭐⭐ "]
    lines.extend(
        row.format(day=day, stars=count_to_str[count])
        for day, count in enumerate(stars, 1)
    )
    return lines


def _get_prev_and_next() -> tuple[DayPart | None, DayPart]:
    dps = get_all_dayparts()
    prev = dps[-1] if dps else None
    next = prev.next() if prev else DayPart.first()
    return prev, next


if __name__ == "__main__":
    raise SystemExit(main())
