from argparse import ArgumentParser
from pathlib import Path

from lib import run_solution

THIS_DIR = Path(__file__).resolve().parent


def compute(s: str) -> int:
    ...


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "inputfile", nargs="?", default=(THIS_DIR / "input.txt"), type=Path
    )
    args = parser.parse_args()

    return run_solution(compute, args.inputfile.read_text())
