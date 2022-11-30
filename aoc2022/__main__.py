import typer
from loguru import logger

app = typer.Typer()


@app.command()
def solve():
    logger.info("Welcome to Advent of Code 2022!")


def main():
    app()


if __name__ == "__main__":
    main()
