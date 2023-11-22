from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_cookie_headers
from ._helpers import get_selections
from ._helpers import get_year
from ._helpers import SelectionArgs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Submit the specified solutions, by default the most recent solution"
            " is submitted"
        ),
    )
    parser.add_argument("--all", default=False, action="store_true")
    parser.add_argument("--days", type=int, action="append")
    parser.add_argument("--parts", type=int, action="append")

    args = parser.parse_args(argv, namespace=_Args())

    year = get_year()
    dayparts = get_all_dayparts()
    selections = get_selections(dayparts, args)

    rtc = 0
    for dp in selections:
        try:
            solution = dp.solutionfile.read_text().strip()
        except FileNotFoundError:
            print(f"No solution exists yet for: {dp}")
            rtc |= 1
        else:
            rtc |= submit_solution(year, dp, solution)

    return rtc


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


class _ErrorRegex(Enum):
    TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
    WRONG = re.compile(r"That's not the right answer.*?\.")
    ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


RIGHT = "That's the right answer!"


@dataclass
class _Args(SelectionArgs):
    ...


if __name__ == "__main__":
    raise SystemExit(main())
