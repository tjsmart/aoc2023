from collections import deque
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import NamedTuple

from lib import collect_lines


@dataclass
class FlipFlopModule:
    name: str
    destinations: list[str]
    state: bool = False


@dataclass
class ConjuctionModule:
    name: str
    destinations: list[str]
    memory: dict[str, bool] = field(default_factory=dict)


@dataclass
class BroadcastModule:
    name: ClassVar[str] = "broadcaster"
    destinations: list[str]


type Module = FlipFlopModule | BroadcastModule | ConjuctionModule


class Signal(NamedTuple):
    src: str
    dest: str
    state: bool


type PulseCount = dict[bool, int]


def solution(s: str) -> int:
    modules = collect_lines(s, parse, container=dict)
    populate_conjuction_memory(modules)
    pulse_counts: list[PulseCount] = []

    for _ in range(1000):
        pulse_counts.append(push_button(modules))

    return sum(pc[False] for pc in pulse_counts) * sum(pc[True] for pc in pulse_counts)


def push_button(modules: dict[str, Module]) -> PulseCount:
    broadcaster = modules["broadcaster"]
    queue: deque[Signal] = deque(
        Signal("broadcaster", d, False) for d in broadcaster.destinations
    )
    pulse_count = {False: 1, True: 0}
    while queue:
        src, dest, state = queue.popleft()
        pulse_count[state] += 1

        m = modules.get(dest)
        match m:
            case None:
                continue

            case FlipFlopModule():
                if not state:
                    m.state = not m.state
                    for d in m.destinations:
                        queue.append(Signal(m.name, d, m.state))

            case ConjuctionModule():
                m.memory[src] = state
                output = not all(m.memory.values())
                for d in m.destinations:
                    queue.append(Signal(m.name, d, output))

            case _:
                raise TypeError(f"Unexpected module type: {type(m).__name__!r}")

    return pulse_count


def get_system_state(modules: dict[str, Module]) -> dict[str, bool]:
    return {
        name: m.state for name, m in modules.items() if isinstance(m, FlipFlopModule)
    }


def populate_conjuction_memory(modules: dict[str, Module]) -> None:
    for name, m in modules.items():
        if not isinstance(m, FlipFlopModule):
            continue
        for d in m.destinations:
            dm = modules[d]
            if isinstance(dm, ConjuctionModule):
                dm.memory[name] = False


def parse(s: str) -> tuple[str, Module]:
    m_s, d_s = s.split(" -> ")
    destinations = d_s.split(", ")

    if m_s == "broadcaster":
        return (m_s, BroadcastModule(destinations))

    op, m_s = m_s[0], m_s[1:]
    match op:
        case "%":
            return (m_s, FlipFlopModule(m_s, destinations))
        case "&":
            return (m_s, ConjuctionModule(m_s, destinations))
        case _:
            raise ValueError(f"Invalid module string: {s}")


class Test:
    import pytest

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (
                """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""",
                32000000,
            ),
            (
                """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""",
                11687500,
            ),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
