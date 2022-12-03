import importlib
from pathlib import Path
from typing import List
import re
import typer
from loguru import logger

app = typer.Typer()

@app.command("solve")
def solve(files: List[Path]):
    """Solve a challenges based on filename"""
    for path in files:
        if path.is_file():
            day = int(re.findall(r"\d+", path.name)[0])
            logger.info(f"--- Day {day} ---", day)
            module = importlib.import_module(f"aoc2022.day{day:02d}")
            logger.info(f"Part 1: {getattr(module, 'part1')(path)}")
            try:
                logger.info(f"Part 2: {getattr(module, 'part2')(path)}")
            except AttributeError:
                logger.warning("No part 2")
            logger.info(f"--- Day {day} ---")


def main():
    app()


if __name__ == "__main__":
    main()
