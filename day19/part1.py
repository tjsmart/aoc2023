from collections.abc import Callable
from dataclasses import dataclass


type Rating = dict[str, int]


@dataclass
class Rule:
    target: str
    condition: Callable[[Rating], bool] = lambda _: True


@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[Rule]


def solution(s: str) -> int:
    w_s, r_s = s.split("\n\n")
    workflows = parse_workflows(w_s)
    ratings = parse_ratings(r_s)
    total = 0
    for rating in ratings:
        if is_accepted(rating, workflows):
            total += sum(rating.values())
    return total


def is_accepted(rating: Rating, workflows: dict[str, Workflow]) -> bool:
    w = "in"
    while True:
        if w == "A":
            return True
        elif w == "R":
            return False

        for rule in workflows[w].rules:
            if rule.condition(rating):
                w = rule.target
                break


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
        return Rule(target, lambda rating: rating[key] > value)
    if "<" in cond:
        key, _, value_s = cond.partition("<")
        value = int(value_s)
        return Rule(target, lambda rating: rating[key] < value)
    else:
        raise ValueError(f"Unexpected rule string: {s}")


def parse_ratings(s: str) -> list[Rating]:
    return [eval(f"dict({l[1:-1]})") for l in s.splitlines()]


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
    EXPECTED_RESULT = 19114

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
