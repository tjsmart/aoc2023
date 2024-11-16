from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Sequence
from enum import Enum
from pathlib import Path

from . import next
from ._calendar_html_parser import parse_calendar_stars_html_to_star_count
from ._helpers import Color
from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_cookie_headers
from ._helpers import get_rootdir
from ._helpers import get_year


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Submit the specified solutions, by default the most recent solution"
            " is submitted"
        ),
    )
    _ = parser.parse_args(argv)

    dayparts = get_all_dayparts()
    if not dayparts:
        raise SystemExit("error: no files exist yet to submit!")

    most_recent = dayparts.pop()
    return submit_daypart(most_recent)


def submit_daypart(dp: DayPart) -> int:
    year = get_year()
    try:
        solution = dp.solutionfile.read_text().strip()
    except FileNotFoundError:
        raise SystemExit(f"error: no solution exists yet for: {dp}")

    if dp.solutionfile.stat().st_mtime < dp.pyfile.stat().st_mtime:
        print("solution has been modified, executing `run` again ...")
        from .run import run_selections
        if rtc := run_selections([dp]):
            return rtc

    if rtc := submit_solution(year, dp, solution):
        return rtc

    dp.mark_solved()
    _update_calendar(year)

    if dp.day == 25:
        return submit_day25_part2()

    if dp.part == 1:
        # time for the next part!
        return next.main([])

    return 0


def submit_day25_part2() -> int:
    """
    Day 25 part2 isn't a new puzzle, just need
    to push the big red button and get-r-done.
    """
    year = get_year()
    dp = DayPart(25, 2)
    if rtc := submit_solution(year, dp, "0"):
        return rtc

    dp.mark_solved()
    _update_calendar(year)
    return 0


def submit_solution(year: int, dp: DayPart, solution: str) -> int:
    contents = _post_solution(year, dp, solution)
    return _parse_post_contents(contents)


def _post_solution(year: int, dp: DayPart, solution: str) -> str:
    params = urllib.parse.urlencode({"level": dp.part, "answer": solution})
    req = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{dp.day}/answer",
        method="POST",
        data=params.encode(),
        headers=get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req)
    return resp.read().decode()


def _parse_post_contents(contents: str) -> int:
    for error_regex in _ErrorRegex:
        error_match = error_regex.value.search(contents)
        if error_match:
            print(f"{Color.RedBack.format(error_match[0])} 😿")
            return 1

    if RIGHT in contents:
        print(f"{Color.GreenBack.format(RIGHT)} 😸")
        return 0
    else:
        print(f"{Color.RedBack.format("unexpected output")} 🙀:\n{contents}")
        return 1


# That's not the right answer; your answer is too low.
# You gave an answer too recently; you have to wait after submitting an answer before trying again.  You have 25s left to wait.
# You gave an answer too recently; you have to wait after submitting an answer before trying again.  You have 4m 37s left to wait.
# That's not the right answer; your answer is too high.
# That's the right answer!

class _ErrorRegex(Enum):
    TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
    WRONG = re.compile(r"That's not the right answer.*?\.")
    ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


RIGHT = "That's the right answer!"


def _update_calendar(year: int) -> None:
    readme_md = get_rootdir() / "README.md"

    html = _get_home_html(year)
    stars = parse_calendar_stars_html_to_star_count(html)
    _update_readme_stars(readme_md, stars)

    print("updated calendar with more stars ✨✨")


def _get_home_html(year: int) -> str:
    url = f"https://adventofcode.com/{year}"
    req = urllib.request.Request(url, headers=get_cookie_headers())
    output = urllib.request.urlopen(req).read().decode().strip()
    return output


def _update_readme_stars(readme_md: Path, stars: list[int]) -> None:
    if readme_md.exists():
        lines = readme_md.read_text().splitlines()
    else:
        lines = []

    starting_lines, ending_lines = _partition_md_on_table(lines)
    new_table = _star_count_to_md_table(stars)

    new_lines = starting_lines + new_table + ending_lines + [""]
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
        ending_idx = len(lines)

    return lines[:starting_idx], lines[ending_idx:]


def _star_count_to_md_table(stars: list[int]) -> list[str]:
    header = "|  day  | stars |\n| ----- | ----- |"
    row = "|   {day:02d}  |{stars}|"
    lines = [header]
    count_to_str = ["       ", "  ⭐   ", "  ⭐⭐ "]
    lines.extend(
        row.format(day=day, stars=count_to_str[count])
        for day, count in enumerate(stars, 1)
    )
    return lines




if __name__ == "__main__":
    raise SystemExit(main())
