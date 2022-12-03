from enum import IntEnum
from typing import Generator, List, Tuple

from loguru import logger
from pathlib import Path


class Move(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Score(IntEnum):
    L = 0
    D = 3
    W = 6


def play(a: Move, b: Move) -> int:
    score = None

    if a == b:
        score = Score.D
    elif a == Move.ROCK:
        if b == Move.PAPER:
            score = Score.L
        elif b == Move.SCISSORS:
            score = Score.W
    elif a == Move.PAPER:
        if b == Move.ROCK:
            score = Score.W
        elif b == Move.SCISSORS:
            score = Score.L
    elif a == Move.SCISSORS:
        if b == Move.ROCK:
            score = Score.L
        elif b == Move.PAPER:
            score = Score.W

    if score is not None:
        return score + a
    else:
        raise ValueError(f"Unknown score from game: {a.name} vs {b.name}")


to_move = {
    "A": Move.ROCK,
    "X": Move.ROCK,
    "B": Move.PAPER,
    "Y": Move.PAPER,
    "C": Move.SCISSORS,
    "Z": Move.SCISSORS,
}


def get_moves_p1(file: Path) -> Generator[List[Move], None, None]:
    return ([to_move[m] for m in g.split()] for g in file.read_text().splitlines())


def part1(file: Path):
    moves = get_moves_p1(file)
    total_score = sum([play(b, a) for a, b in moves])
    return total_score


to_their_move = {
    "A": Move.ROCK,
    "B": Move.PAPER,
    "C": Move.SCISSORS,
}


def to_my_move(t: Move, m: str) -> Move:
    move = None

    if m == "Y":  # Draw
        move = t
    elif m == "X":  # Lose
        if t == Move.ROCK:
            move = Move.SCISSORS
        elif t == Move.PAPER:
            move = Move.ROCK
        elif t == Move.SCISSORS:
            move = Move.PAPER
    elif m == "Z":  # Win
        if t == Move.ROCK:
            move = Move.PAPER
        elif t == Move.PAPER:
            move = Move.SCISSORS
        elif t == Move.SCISSORS:
            move = Move.ROCK

    if move is not None:
        return move
    else:
        raise ValueError(f"Unknown move for {t} given {m}")


def parse_moves_p2(t: str, m: str) -> Tuple[Move, Move]:
    their_move = to_their_move[t]
    return their_move, to_my_move(their_move, m)


def get_moves_p2(file: Path) -> Generator[Tuple[Move, Move], None, None]:
    return (parse_moves_p2(*g.split()) for g in file.read_text().splitlines())


def part2(file: Path):
    moves = get_moves_p2(file)
    total_score = sum([play(b, a) for a, b in moves])
    return total_score
