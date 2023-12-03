from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Sequence
from enum import Enum

from . import next
from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_cookie_headers
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
    if dp.part == 1:
        # time for the next part!
        return next.main([])

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
            print(f"\033[41m{error_match[0]}\033[m")
            return 1

    if RIGHT in contents:
        print(f"\033[42m{RIGHT}\033[m")
        return 0
    else:
        print(f"\033[41m{"unexpected output"}\033[m:\n{contents}")
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


if __name__ == "__main__":
    raise SystemExit(main())
