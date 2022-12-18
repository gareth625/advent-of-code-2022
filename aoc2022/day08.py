from functools import reduce
from pathlib import Path
from operator import mul
from typing import List, Tuple

from loguru import logger


# logger.disable(__name__)


def build_grid(grid: List[List[int]], row: str) -> List[List[int]]:
    grid.append([int(s) for s in row])
    return grid


def select_row(
    grid: List[List[int]], row_idx: int, col_idx: int
) -> Tuple[List[int], List[int]]:
    return grid[row_idx][0:col_idx], grid[row_idx][col_idx + 1 :]


def select_col(
    grid: List[List[int]], row_idx: int, col_idx: int
) -> Tuple[List[int], List[int]]:
    return (
        [grid[i][col_idx] for i in range(len(grid)) if i < row_idx],
        [grid[i][col_idx] for i in range(len(grid)) if i > row_idx],
    )


def is_visible(trees: List[int], candidate: int) -> int:
    return 1 if all(candidate > tree for tree in trees) else 0


def is_edge(index: int, max_index: int) -> int:
    return 1 if (index == 0 or index == max_index - 1) else 0


def check_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return []

    nrows = len(grid)
    ncols = len(grid[0])
    logger.info(f"(nrows, ncols) = ({nrows},{ncols})")
    visible_trees: List[List[int]] = [[0 for _ in range(ncols)] for _ in range(nrows)]
    for row_idx in range(nrows):
        # logger.info("----")
        for col_idx in range(ncols):
            #            logger.info("--")
            row_before, row_after = select_row(grid, row_idx, col_idx)
            col_before, col_after = select_col(grid, row_idx, col_idx)
            #            logger.info(f"{row_before}, {row_after}")
            #            logger.info(f"{col_before}, {col_after}")
            candidate = grid[row_idx][col_idx]
            visible_in_row = (
                is_visible(row_before, candidate) or is_visible(row_after, candidate)
                if not is_edge(row_idx, nrows)
                else 1
            )
            visible_in_col = (
                is_visible(col_before, candidate) or is_visible(col_after, candidate)
                if not is_edge(col_idx, ncols)
                else 1
            )

            # logger.info(
            #     f"({row_idx}, {col_idx})={grid[row_idx][col_idx]}: {visible_in_row}, {visible_in_col}"
            # )
            visible_trees[row_idx][col_idx] = visible_in_row or visible_in_col

    return visible_trees


def scenic_score_line_of_sight(trees: List[int], candidate: int) -> int:
    if not trees:
        return 0

    score = 0
    for tree in trees:
        score += 1
        if tree >= candidate:
            break

    return score


def scenic_score_total(sight_scores: List[int]) -> int:
    return reduce(mul, sight_scores)


def how_scenic(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return []

    nrows = len(grid)
    ncols = len(grid[0])
    # logger.info(f"(nrows, ncols) = ({nrows},{ncols})")
    scenery: List[List[int]] = [[0 for _ in range(ncols)] for _ in range(nrows)]
    for row_idx in range(nrows):
        # logger.info("----")
        for col_idx in range(ncols):
            # logger.info("--")
            row_before, row_after = select_row(grid, row_idx, col_idx)
            col_before, col_after = select_col(grid, row_idx, col_idx)
            candidate = grid[row_idx][col_idx]
            # logger.info(f"Candidate: {candidate}")
            # logger.info(f"Row: {row_before}, {row_after}")
            # logger.info(f"Col: {col_before}, {col_after}")
            scenery[row_idx][col_idx] = scenic_score_total(
                [
                    scenic_score_line_of_sight(reversed(row_before), candidate),
                    scenic_score_line_of_sight(row_after, candidate),
                    scenic_score_line_of_sight(reversed(col_before), candidate),
                    scenic_score_line_of_sight(col_after, candidate),
                ]
            )
            # logger.info(f"Score: {scenery[row_idx][col_idx]}")
    return scenery


def part1(file: Path):
    initial: List[List[int]] = []
    grid = reduce(
        build_grid,
        file.read_text().splitlines(),
        initial,
    )
    logger.info(grid)

    visible_trees = check_grid(grid)
    # logger.info(visible_trees)
    return sum(tree_visible for row in visible_trees for tree_visible in row)


def part2(file: Path):
    initial: List[List[int]] = []
    grid = reduce(
        build_grid,
        file.read_text().splitlines(),
        initial,
    )
    logger.info(grid)

    scenery = how_scenic(grid)
    logger.info(scenery)
    return max(score for trees in scenery for score in trees)
