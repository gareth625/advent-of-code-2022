from pathlib import Path

from typing import Collection, List, Set, Tuple


def as_prioritises(items: str) -> List[int]:
    prioritises = []
    for item in items:
        i = ord(item)
        prioritises.append(i - 96 if i > 96 else i - 38)
    return prioritises


def compartmentalise(items: List[int]) -> Tuple[Set[int], Set[int]]:
    nitems = len(items)
    if nitems % 2 != 0:
        raise ValueError(f"Uneven number of items in sack, found {nitems} in '{items}'")

    split = int(nitems / 2)
    return set(items[:split]), set(items[split:])


def part1(file: Path):
    sacks = (compartmentalise(as_prioritises(r)) for r in file.read_text().splitlines())
    shared_items = (a.intersection(b).pop() for a, b in sacks)
    return sum(shared_items)


def part2(file: Path):
    sacks = [as_prioritises(s) for s in file.read_text().splitlines()]
    n = 3
    groups = ([set(j) for j in sacks[i:i + n]] for i in range(0, len(sacks), n))
    badges = (a.intersection(b).intersection(c).pop() for a, b, c in groups)
    return sum(badges)
