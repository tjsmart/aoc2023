from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Self


@dataclass
class Range:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1

    @classmethod
    def empty(cls) -> Self:
        return Range(0, -1)

    @classmethod
    def full(cls) -> Self:
        return Range(1, 4000)

    @property
    def is_empty(self) -> bool:
        return self.end < self.start

    def __bool__(self) -> bool:
        return not self.is_empty


@dataclass
class RatingRange:
    x: Range
    m: Range
    a: Range
    s: Range

    @classmethod
    def empty(cls) -> Self:
        return cls(Range.empty(), Range.empty(), Range.empty(), Range.empty())

    @classmethod
    def full(cls) -> Self:
        return cls(Range.full(), Range.full(), Range.full(), Range.full())

    def combinations(self) -> int:
        return self.x.length * self.m.length * self.a.length * self.s.length


@dataclass
class Rule:
    target: str
    condition: Callable[[RatingRange], tuple[RatingRange, RatingRange]] = lambda rr: (
        rr,
        RatingRange.empty(),
    )


@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[Rule]


def solution(s: str) -> int:
    w_s, _ = s.split("\n\n")
    workflows = parse_workflows(w_s)

    queue: list[tuple[str, RatingRange]] = [("in", RatingRange.full())]
    accepted_ranges: list[RatingRange] = []
    while queue:
        w, rr = queue.pop()
        if w == "A":
            accepted_ranges.append(rr)
            continue

        if w == "R":
            continue

        for rule in workflows[w].rules:
            trr, rr = rule.condition(rr)
            if trr:
                queue.append((rule.target, trr))
            if not rr:
                break

    return sum(rr.combinations() for rr in accepted_ranges)


def parse_workflows(s: str) -> dict[str, Workflow]:
    return {w.name: w for w in map(parse_workflow, s.splitlines())}


def parse_workflow(s: str) -> Workflow:
    name, rest = s.split("{")
    rules_s = rest.strip("}")
    rules = [parse_rule(s) for s in rules_s.split(",")]
    return Workflow(name, rules)


def parse_rule(s: str) -> Rule:
    cond_or_target, colon, target = s.partition(":")
    if not colon:
        return Rule(cond_or_target)

    cond = cond_or_target
    if ">" in cond:
        key, _, value_s = cond.partition(">")
        value = int(value_s)
        return Rule(target, partial(split_range_gt, key=key, value=value))
    if "<" in cond:
        key, _, value_s = cond.partition("<")
        value = int(value_s)
        return Rule(target, partial(split_range_lt, key=key, value=value))
    else:
        raise ValueError(f"Unexpected rule string: {s}")


def split_range_lt(
    rr: RatingRange, key: str, value: int
) -> tuple[RatingRange, RatingRange]:
    rrd = {k: getattr(rr, k) for k in ("x", "m", "a", "s")}
    kr = rrd[key]
    if kr.end < value:
        return rr, RatingRange.empty()
    if kr.start > value:
        return RatingRange.empty(), rr

    return (
        RatingRange(**(rrd | {key: Range(kr.start, value - 1)})),
        RatingRange(**(rrd | {key: Range(value, kr.end)})),
    )


def split_range_gt(
    rr: RatingRange, key: str, value: int
) -> tuple[RatingRange, RatingRange]:
    rrd = {k: getattr(rr, k) for k in ("x", "m", "a", "s")}
    kr = rrd[key]
    if kr.end < value:
        return RatingRange.empty(), rr
    if kr.start > value:
        return rr, RatingRange.empty()

    return (
        RatingRange(**(rrd | {key: Range(value + 1, kr.end)})),
        RatingRange(**(rrd | {key: Range(kr.start, value)})),
    )


class Test:
    import pytest

    EXAMPLE_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
    EXPECTED_RESULT = 167409079868000

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
