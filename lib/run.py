import time
from argparse import ArgumentParser
from collections.abc import Callable
from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import field

from ._helpers import DayPart
from ._helpers import get_all_dayparts


def time_it[**P](
    solution: Callable[P, object],
    *args: P.args,
    **kwargs: P.kwargs,
) -> int:
    start = time.monotonic_ns()
    try:
        result = solution(*args, **kwargs)
    except KeyboardInterrupt:
        end = time.monotonic_ns()
        duration = _format_duration(end - start)
        print(f"solution cancelled after {duration}")
        return 1

    end = time.monotonic_ns()
    duration = _format_duration(end - start)

    print(f"{result = }, duration = {duration}")
    return 0


def _format_duration(duration_ns: int) -> str:
    power = len(str(duration_ns)) - 1
    unit = power // 3
    duration = duration_ns / (10 ** (unit * 3))

    match unit:
        case 0:
            unit_str = "ns"
        case 1:
            unit_str = "μs"
        case 2:
            unit_str = "ms"
        case _:
            duration = duration_ns / (10**9)
            unit_str = "s"

            if duration >= 60:
                duration = duration / 60
                unit_str = "min"

    return f"{duration:.1f} {unit_str}"


@dataclass
class Args:
    all: bool = False
    days: list[int] = field(default_factory=list)
    parts: list[int] = field(default_factory=list)


def _get_selections(dayparts: list[DayPart], args: Args) -> list[DayPart]:
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(
        description=(
            "Execute specified solutions, by default the most recent solution"
            " is executed"
        ),
    )
    parser.add_argument("--all", default=False, action="store_true")
    parser.add_argument("--days", type=int, action="append")
    parser.add_argument("--parts", type=int, action="append")

    args = parser.parse_args(argv, namespace=Args())
    dayparts = get_all_dayparts()
    selections = _get_selections(dayparts, args)

    rtc = 0
    for dp in selections:
        input = dp.inputfile.read_text()
        solution = dp.load_solution()
        print(f"{dp.emoji} ({dp.day:02}/{dp.part}) ➡️ ", end="")
        rtc |= time_it(solution, input)

    return rtc

if __name__ == "__main__":
    raise SystemExit(main())
