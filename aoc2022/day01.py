from pathlib import Path
from typing import Generator


def sums(data: Path) -> Generator[int, None, None]:
    return (
        sum(int(i) for i in s.split()) for s in data.read_text("utf-8").split("\n\n")
    )


def part1(file: Path):
    return max(sums(file))


def part2(file: Path):
    return sum(sorted(sums(file), reverse=True)[0:3])
