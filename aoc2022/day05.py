from collections import defaultdict
from dataclasses import dataclass
from itertools import accumulate
from pathlib import Path
from queue import deque
import re
from typing import Deque, Dict, List, Tuple


@dataclass(frozen=True)
class Move:
    n: int
    start: int
    to: int


def parse_line(
    state: Tuple[Dict[int, Deque], List[Move]], line: str
) -> Tuple[Dict[int, Deque], List[Move]]:
    stacks, moves = state
    if move := re.match(r"^move ([0-9]+) from ([0-9]+) to ([0-9]+)$", line):
        # move 1 from 2 to 1
        moves.append(Move(*(int(g) for g in move.groups())))
    elif crates := re.findall(r"(?:\[([A-Z])\]+|   ) ?", line):
        # "        [M] [N] [L] [T] [Q]"
        # "[G]     [P] [C] [F] [G] [T]"
        for i, item in enumerate(crates):
            # Moves count from 1
            if item:
                stacks[i + 1].insert(0, item)
    elif re.match(r"\ [0-9]", line):
        # Skip the line assigning a number to each stack
        pass
    elif not line:
        # Skip the empty line
        pass
    else:
        raise ValueError(f"Unhandled line type: f{line}")

    return stacks, moves


def update_stack_9000(stacks: Dict[int, Deque], move: Move) -> Dict[int, Deque]:
    for _ in range(move.n):
        crate = stacks[move.start].pop()
        stacks[move.to].append(crate)
    return stacks


def update_stack_9001(stacks: Dict[int, Deque], move: Move) -> Dict[int, Deque]:
    to_stack = stacks[move.to]
    after = len(to_stack)
    for _ in range(move.n):
        crate = stacks[move.start].pop()
        to_stack.insert(after, crate)
    return stacks


def top_of_stacks(stacks: Dict[int, Deque]) -> str:
    tops = []
    for i in range(len(stacks)):
        tops.append(stacks[i + 1].pop())

    return "".join(tops)


def part1(file: Path):
    stacks, moves = list(
        accumulate(
            file.read_text().splitlines(),
            parse_line,
            initial=(defaultdict(deque), []),
        )
    )[-1]
    final_state = list(
        accumulate(
            moves,
            update_stack_9000,
            initial=stacks,
        )
    )[-1]
    return top_of_stacks(final_state)


def part2(file: Path):
    stacks, moves = list(
        accumulate(
            file.read_text().splitlines(),
            parse_line,
            initial=(defaultdict(deque), []),
        )
    )[-1]
    final_state = list(
        accumulate(
            moves,
            update_stack_9001,
            initial=stacks,
        )
    )[-1]
    return top_of_stacks(final_state)
