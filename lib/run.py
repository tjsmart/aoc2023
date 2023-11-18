import time
from collections.abc import Callable


def run_solution[**P](
    compute: Callable[P, object],
    *args: P.args,
    **kwargs: P.kwargs,
) -> int:
    start = time.monotonic_ns()
    try:
        result = compute(*args, **kwargs)
    except KeyboardInterrupt:
        end = time.monotonic_ns()
        duration = _format_duration(end - start)
        print(f"solution cancelled after {duration}")
        return 1

    end = time.monotonic_ns()
    duration = _format_duration(end - start)

    print(f"{result = }, {duration = }")
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
        case 3:
            unit_str = "s"
        case _:
            duration = duration_ns / (10**9) / 60
            unit_str = "min"

    return f"{duration} {unit_str}"
