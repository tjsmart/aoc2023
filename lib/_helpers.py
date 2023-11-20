from __future__ import annotations

import importlib
import logging
import re
import subprocess
import warnings
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple


logger = logging.getLogger("aoc.lib")
THIS_DIR = Path(__file__).resolve().parent
_PARTFILE = re.compile(r".*/day(\d\d)/part(\d)\.py")
type Solution[T] = Callable[[str], T]
_EMOJI_LIST = [
    "🔔", # 1
    "📦", # 2
    "👼", # 3
    "🌟", # 4
    "🎄", # 5
    "🎤", # 6
    "🎶", # 7
    "🔥", # 8
    "❄️", # 9
    "☃️", # 10
    "🍴", # 11
    "🍷", # 12
    "🍺", # 13
    "🦌", # 14
    "🥕", # 15
    "🏂", # 16
    "🧝", # 17
    "🧦", # 18
    "☕", # 19
    "📝", # 20
    "🎁", # 21
    "🍪", # 22
    "🥛", # 23
    "🤶", # 24
    "🎅", # 25
]


class DayPart(NamedTuple):
    day: int
    part: int

    @property
    def outdir(self) -> Path:
        return get_rootdir() / f"day{self.day:02}"

    @property
    def pyfile(self) -> Path:
        return self.outdir / f"part{self.part}.py"

    @property
    def inputfile(self) -> Path:
        return self.outdir / f"input.txt"

    def load_solution(self) -> Solution:
        mod = importlib.import_module(f"day{self.day:02}.part{self.part}")
        return mod.solution

    @classmethod
    def first(cls) -> DayPart:
        return DayPart(1, 1)

    def next(self) -> DayPart:
        if self == (25, 2):
            raise HandledError("It's over, go home!")

        if self.day not in range(1, 26) and self.part in (1, 2):
            raise HandledError(
                f"Unable to determine next from invalid day/part: {self}"
            )

        if self.part == 1:
            return DayPart(self.day, self.part + 1)
        else:
            return DayPart(self.day + 1, 1)

    @property
    def emoji(self) -> str:
        return _EMOJI_LIST[self.day]


class HandledError(RuntimeError):
    ...


@lru_cache(maxsize=1)
def get_rootdir() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


@lru_cache(maxsize=1)
def get_year() -> int:
    rootdir = get_rootdir()
    *_, year = rootdir.name.partition("aoc")
    try:
        return int(year)
    except ValueError:
        raise HandledError(
            f"failed to parse year from rootdir name: {rootdir.name}, expected"
            " name to be of the form 'aoc[year]', e.g., 'aoc2023'"
        )

def get_all_dayparts() -> list[DayPart]:
    """
    Returns a list of all previous day/part solutions in ascending order
    """
    rootdir = get_rootdir()
    dayparts = []
    for dd in rootdir.glob("day*/part*.py"):
        m = _PARTFILE.search(str(dd))
        if not m:
            warnings.warn(f"skipping invalid day/part file: {dd}")
            continue

        dp = DayPart(*map(int, m.groups()))
        dayparts.append(dp)

    dayparts.sort()
    return dayparts
