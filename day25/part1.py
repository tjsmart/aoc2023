"""
https://en.wikipedia.org/wiki/Karger%27s_algorithm
"""
import math
from collections import defaultdict
from random import Random


rng = Random("aoc2023")


def solution(s: str) -> int:
    edges: set[frozenset[str]] = set()
    graph: dict[str, set[str]] = defaultdict(set)
    for line in s.splitlines():
        key, value_s = line.split(": ")
        for value in value_s.strip().split():
            edges.add(frozenset({key, value}))
            graph[key].add(value)
            graph[value].add(key)

    while True:
        cg = contract(graph)
        cut_size = len(next(iter(cg.values())))
        if cut_size == 3:
            return math.prod(map(lambda s: s.count("-") + 1, cg))


def contract(g: dict[str, set[str]]) -> dict[str, list[str]]:
    graph = {k: list(values) for k, values in g.items()}

    for _ in range(len(graph) - 2):
        n1, n2 = random_edge(graph)
        new = f"{n1}-{n2}"

        new_values = []
        for n in graph.pop(n1):
            if n == n2:
                continue
            new_values.append(n)
            graph[n].remove(n1)
            graph[n].append(new)

        for n in graph.pop(n2):
            if n == n1:
                continue
            new_values.append(n)
            graph[n].remove(n2)
            graph[n].append(new)

        graph[new] = new_values

    return graph


def edges(graph: dict[str, list[str]]) -> list[tuple[str, str]]:
    return [(k, v) for k, vs in graph.items() for v in vs]


def random_edge(graph: dict[str, list[str]]) -> tuple[str, str]:
    return rng.choice(list(edges(graph)))


class Test:
    import pytest

    EXAMPLE_INPUT = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""
    EXPECTED_RESULT = 54

    @pytest.mark.parametrize(
        ("case", "expected"),
        [
            (EXAMPLE_INPUT, EXPECTED_RESULT),
        ],
    )
    def test_examples(self, case, expected):
        assert solution(case) == expected
