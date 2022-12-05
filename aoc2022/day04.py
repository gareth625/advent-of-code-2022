from pathlib import Path
from typing import Tuple


def get_assignment_range(s: str) -> Tuple[int, int]:
    lower, upper = s.split("-")
    return int(lower), int(upper)


def get_assignment_ranges(s: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    a, b = s.split(",")
    return get_assignment_range(a), get_assignment_range(b)


def within(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    a_min, a_max = a
    b_min, b_max = b
    return (a_min <= b_min and a_max >= b_max) or (b_min <= a_min and b_max >= a_max)


def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    a_min, a_max = a
    b_min, b_max = b
    return (a_min <= b_min and b_min <= a_max) or (b_min <= a_min and a_min <= b_max)


def part1(file: Path):
    n_within = (
        1 for s in file.read_text().splitlines() if within(*get_assignment_ranges(s))
    )
    return sum(n_within)


def part2(file: Path):
    n_overlap = (
        1 for s in file.read_text().splitlines() if overlaps(*get_assignment_ranges(s))
    )
    return sum(n_overlap)
