from loguru import logger
from pathlib import Path
from typing import List


def chunk_stream(message: str, chunk_size: int) -> List[str]:
    return [message[i : i + chunk_size] for i in range(len(message))]


def chunk_is_unique(chunk: str) -> bool:
    return len(chunk) == len(set(chunk))


def section_start(chunks: List[str], chunk_size: int) -> int:
    return next(
        i + chunk_size for i, chunk in enumerate(chunks) if chunk_is_unique(chunk)
    )


def part1(file: Path):
    chunk_size = 4
    messages = file.read_text().splitlines()
    return tuple(
        section_start(chunk_stream(message, chunk_size), chunk_size)
        for message in messages
    )


def part2(file: Path):
    chunk_size = 14
    messages = file.read_text().splitlines()
    return tuple(
        section_start(chunk_stream(message, chunk_size), chunk_size)
        for message in messages
    )
