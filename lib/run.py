import time
from argparse import ArgumentParser
from collections.abc import Callable
from collections.abc import Sequence
from dataclasses import dataclass

from . import submit
from ._helpers import Color
from ._helpers import DayPart
from ._helpers import get_all_dayparts
from ._helpers import get_selections
from ._helpers import SelectionArgs


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
    parser.add_argument("--test", default=False, action="store_true")

    args, other_args = parser.parse_known_args(argv, namespace=_Args())
    dayparts = get_all_dayparts()
    selections = get_selections(dayparts, args)

    if args.test:
        return _test_selections(selections, other_args)
    else:
        return run_selections(selections)


def run_selections(selections: list[DayPart]) -> int:
    rtc = 0
    for dp in selections:
        input = dp.inputfile.read_text()
        solution = dp.load_solution()
        print(f"{dp.emoji} ({dp.day:02}/{dp.part}) ➡️ ", end="")
        result = time_it(solution, input)

        match result:
            case Cancelled(duration):
                print(f"{Color.YellowText.format(f"solution cancelled after {duration}")} 🛑")
                rtc |= 1

            case Finished(None, _):
                print(f"{Color.YellowText.format("no answer provided?!")} 👻")
                rtc |= 1

            case Finished(result, duration):
                if dp.is_solved():
                    correct = str(result) == dp.solutionfile.read_text()
                    if correct:
                        print(f"{Color.GreenText.format(f"{result = }, duration = {duration}")} ✅")
                    else:
                        print(f"{Color.RedText.format(f"{result = }, duration = {duration}")} ❌")
                        rtc |= 1
                else:
                    if dp.add_guess(str(result)):
                        dp.solutionfile.write_text(str(result))
                        print(f"{Color.BlueText.format(f"{result = }, duration = {duration}")} 🚀")
                        rtc |= submit.submit_daypart(dp)
                    else:
                        print(f"{Color.RedText.format(f"{result = }, duration = {duration}")} ❌")
                        rtc |= 1

    return rtc


def _test_selections(
    selections: list[DayPart],
    pytest_args: list[str] | None = None,
) -> int:
    import pytest

    args = [*pytest_args, "--"] if pytest_args else ["--"]
    args.extend(str(dp.pyfile) for dp in selections)
    return pytest.main(args)


@dataclass
class Finished[R]:
    result: R | None
    duration: str

@dataclass
class Cancelled:
    duration: str

type SolutionResult[R] = Finished[R] | Cancelled

def time_it[R, **P](
    solution: Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> SolutionResult[R]:
    start = time.monotonic_ns()
    try:
        result = solution(*args, **kwargs)
    except KeyboardInterrupt:
        end = time.monotonic_ns()
        duration = _format_duration(end - start)
        return Cancelled(duration)

    end = time.monotonic_ns()
    duration = _format_duration(end - start)
    return Finished(result, duration)


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
class _Args(SelectionArgs):
    test: bool = False


if __name__ == "__main__":
    raise SystemExit(main())
