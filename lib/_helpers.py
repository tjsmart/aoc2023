from __future__ import annotations

import importlib
import logging
import os
import re
import subprocess
import warnings
from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
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
        return self.outdir / "input.txt"

    @property
    def solutionfile(self) -> Path:
        return self.outdir / f"solution{self.part}.txt"

    @property
    def promptfile(self) -> Path:
        return self.outdir / "prompt.md"

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

    def is_solved(self) -> bool:
        return os.access(self.solutionfile, os.W_OK)

    def mark_solved(self) -> None:
        self.solutionfile.chmod(0o444)

    @property
    def guessfile(self) -> Path:
        return self.outdir / f"guesses{self.part}.txt"

    def add_guess(self, value: str) -> bool:
        """
        Add to set of locally saved previous guesses.
        Returns True/False if guess is new/old.
        """
        try:
            guessfile_contents = self.guessfile.read_text()
        except FileNotFoundError:
            guessfile_contents = ""
        prev_guesses = set(guessfile_contents.splitlines())
        if value in prev_guesses:
            return False
        else:
            self.guessfile.write_text(f"{guessfile_contents}\n{value}")
            return True


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


@dataclass
class SelectionArgs:
    all: bool = False
    days: list[int] = field(default_factory=list)
    parts: list[int] = field(default_factory=list)


def get_selections(dayparts: list[DayPart], args: SelectionArgs) -> list[DayPart]:
    dayparts = dayparts[:]
    if not dayparts:
        return []

    match (args.all, args.days, args.parts):
        case (False, [], []):
            return dayparts[-1:]

        case (False, [], parts):
            days = [dayparts[-1].day]

        case (_, days, parts):
            days = days or [dp.day for dp in dayparts]

        case _:
            raise AssertionError("Should never happen")

    parts = parts or [1, 2]
    return [dp for dp in dayparts if dp.day in days and dp.part in parts]


def get_cookie_headers() -> dict[str, str]:
    session_file = get_rootdir() / ".session"
    return {"Cookie": f"session={session_file.read_text().strip()}"}


class Color(Enum):
    RedText = 31
    GreenText = 32
    YellowText = 33
    BlueText = 34

    RedBack = 41
    GreenBack = 42
    YellowBack = 43
    BlueBack = 44

    def format(self, text: str) -> str:
        return f"\033[{self.value}m{text}\033[0m"
