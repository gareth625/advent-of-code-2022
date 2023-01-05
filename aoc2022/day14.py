from dataclasses import dataclass, field
from functools import reduce
from itertools import repeat
from operator import or_
from pathlib import Path
from typing import Set, Tuple

from aoc2022.helpers import partition
from loguru import logger


Coordinate = Tuple[int, int]
Rocks = Set[Coordinate]
Beach = Set[Coordinate]

SAND_ENTRY: Coordinate = (500, 0)


@dataclass(init=False)
class Cave:
    max_rock_left: Coordinate = (0, 0)
    max_rock_right: Coordinate = (0, 0)
    floor: Coordinate = (0, 0)

    rocks: Rocks = field(default_factory=set)
    beach: Beach = field(default_factory=set)

    def __init__(self, rocks: Rocks):
        self.rocks = rocks

        min_x = min(rocks, key=lambda coord: coord[0])[0]
        max_x = max(rocks, key=lambda coord: coord[0])[0]
        # min_y = min(rocks, key=lambda coord: coord[1])
        max_y = max(rocks, key=lambda coord: coord[1])[1]
        self.max_rock_left = min_x, max_y
        self.max_rock_right = max_x, max_y

        # The floor is an infinite plane, store lower corner for convenience.
        self.floor = (max_x, max_y + 2)
        logger.info(f"left: {self.max_rock_left}, right: {self.max_rock_right}")

        self.beach = set()


def get_rock_line(start: Coordinate, end: Coordinate) -> Rocks:
    x_start, y_start = start
    x_end, y_end = end
    if x_start > x_end:
        x_end, x_start = x_start, x_end
    if y_start > y_end:
        y_end, y_start = y_start, y_end
    return set(
        (x, y) for x in range(x_start, x_end + 1) for y in range(y_start, y_end + 1)
    )


def get_rock_lines(rocks: Rocks, input: str) -> Rocks:
    coords_s = (tuple(coord.split(",")) for coord in input.split(" -> "))
    # Partition will return the last element as it's own 'pair'. Might fix this one day.
    coords = (
        coord
        for coord in partition(2, [(int(x), int(y)) for x, y in coords_s])
        if len(coord) == 2
    )
    return reduce(
        or_,
        ((get_rock_line(start, end)) for start, end in coords),
        rocks,
    )


def collision(cave: Cave, grain: Coordinate) -> bool:
    return grain in cave.rocks or grain in cave.beach


def descend(cave: Cave, incoming: Coordinate) -> Coordinate:
    entry_x, entry_y = incoming
    descend_one_y = entry_y + 1
    descend_one = entry_x, descend_one_y
    descend_one_left = entry_x - 1, descend_one_y
    descend_one_right = entry_x + 1, descend_one_y

    return next(
        filter(
            lambda g: not collision(cave, g),
            [descend_one, descend_one_left, descend_one_right, incoming],
        )
    )


def within_rock_lines(cave: Cave, grain: Coordinate) -> bool:
    return (grain[0] >= cave.max_rock_left[0] and grain[1] <= cave.max_rock_left[1]) or (
        grain[0] <= cave.max_rock_right[0] and grain[1] <= cave.max_rock_right[1]
    )


def settle_sand(cave: Cave, incoming: Coordinate) -> Cave:
    new_location = descend(cave, incoming)
    logger.info(f"Fell to: {new_location}")

    if within_rock_lines(cave, new_location):
        if incoming == new_location:
            cave.beach.add(new_location)
        else:
            cave = settle_sand(cave, new_location)
    else:
        raise StopIteration("Falling to infinity")

    return cave


def part1(file: Path):
    empty_rocks: Rocks = set()
    rocks = reduce(get_rock_lines, file.read_text().splitlines(), empty_rocks)
    logger.info(rocks)

    cave = Cave(rocks)
    try:
        cave = reduce(settle_sand, repeat(SAND_ENTRY), cave)
    except StopIteration:
        pass

    logger.info(cave)
    logger.info(len(cave.beach))
    return len(cave.beach)


def part2(file: Path):
    pass
