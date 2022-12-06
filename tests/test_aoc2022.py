import importlib
import pathlib
import pytest

solutions = [
    (1, [24_000, 45000]),
    (2, [15, 12]),
    (3, [157, 70]),
    (4, [2, 4]),
    (5, ["CMZ", "MCD"]),
    (6, [(7, 5, 6, 10, 11), (19, 23, 23, 29, 26)]),
    (7, [None, None]),
    (8, [None, None]),
    (9, [None, None]),
]

# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("day,expected", solutions)
def test_all(day, expected):
    module = importlib.import_module(f"aoc2022.day{day:02d}")
    file = pathlib.Path(f"tests/inputs/day{day:02d}.txt")
    assert getattr(module, "part1")(file) == expected[0]
    assert getattr(module, "part2")(file) == expected[1]
