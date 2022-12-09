import abc
from enum import Enum
import functools
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple, Union


class CommandType(Enum):
    cd = "cd"
    ls = "ls"


class Command(abc.ABC):
    @property
    @abc.abstractmethod
    def command_type(self) -> CommandType:
        ...

    @property
    @abc.abstractmethod
    def action(self) -> Union[List[Tuple[str, int]], str]:
        return ""

    @abc.abstractmethod
    def act(
        self, state: Dict[str, Tuple[int, bool]], current_dir: List[str]
    ) -> Tuple[Dict[str, Tuple[int, bool]], List[str]]:
        ...


class Cd(Command):
    _command_type: CommandType = CommandType.cd
    _action: str = ""

    def __init__(self, action: str):
        self._action = action

    def __repr__(self):
        return f"cd: {self.action}"

    def __str__(self):
        return self.__repr__()

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @property
    def action(self) -> str:
        return self._action

    def act(
        self, state: Dict[str, Tuple[int, bool]], current_dir: List[str]
    ) -> Tuple[Dict[str, Tuple[int, bool]], List[str]]:
        if self.action == "/":
            current_dir = ["root"]
        elif self.action == "..":
            current_dir = current_dir[:-1]
        else:
            current_dir.append(self.action)

        return state, current_dir


class Ls(Command):
    _command_type: CommandType = CommandType.ls
    _action: List[Tuple[str, int]]

    def __init__(self) -> None:
        self._action = []

    def __repr__(self):
        return f"ls: {', '.join(f'{file}:{size}' for file, size in self.action)}"
        # return f"ls: {len(self.action)}"

    def __str__(self):
        return self.__repr__()

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @property
    def action(self) -> List[Tuple[str, int]]:
        return self._action

    @action.setter
    def action(self, listing: str):
        file = ""
        size = 0
        if match := re.match("(?P<size>[0-9]+) (?P<file>[a-z.]+)", listing):
            file = match.group("file")
            size = int(match.group("size"))
            self._action.append((file, size))
        elif listing.startswith("dir"):
            # Skip directories
            pass
        else:
            raise ValueError(f"Unrecognised ls listing {listing}")

    def act(
        self, state: Dict[str, Tuple[int, bool]], current_dir: List[str]
    ) -> Tuple[Dict[str, Tuple[int, bool]], List[str]]:
        for file, size in self.action:
            dir = current_dir.copy()
            for i in range(len(dir)):
                parent = "/".join(dir[: i + 1])
                parent_size, _ = state.get(parent, (0, True))
                state[parent] = (parent_size + size, True)
            dir.append(file)
            sdir = "/".join(dir)
            current_size, _ = state.get(sdir, (0, False))
            state[sdir] = (current_size + size, False)

        return state, current_dir


def parse(commands: List[Command], line: str) -> List[Command]:
    command = commands[-1] if commands else None
    if line.startswith("$"):
        if match := re.search("(?P<command>cd|ls) ?(?P<action>.+)?", line):
            cmd_type = CommandType(match.group("command"))
            if CommandType.cd == cmd_type:
                command = Cd(match.group("action"))
            elif CommandType.ls == cmd_type:
                command = Ls()
        else:
            raise ValueError(f"Unrecognised command type: {line}")
    else:
        if isinstance(command, Ls):
            command.action = line
        else:
            raise ValueError(
                f"Command ({command}) isn't an 'ls' however, the next line isn't another command"
            )

    if not command:
        raise ValueError(f"Failed to parse a command from line: {line}")

    if not commands or command != commands[-1]:
        commands.append(command)

    return commands


def part1(file: Path):
    terminal = file.read_text().splitlines()
    initial: List[Command] = []
    commands = functools.reduce(parse, terminal, initial)

    state: Dict[str, Tuple[int, bool]] = {}
    current_dir: List[str] = ["root"]
    for command in commands:
        state, current_dir = command.act(state, current_dir)
    print(state)

    return sum(size for _, (size, isdir) in state.items() if isdir and size <= 100_000)


def part2(file: Path):
    terminal = file.read_text().splitlines()
    initial: List[Command] = []
    commands = functools.reduce(parse, terminal, initial)

    state: Dict[str, Tuple[int, bool]] = {}
    current_dir: List[str] = ["root"]
    for command in commands:
        state, current_dir = command.act(state, current_dir)
    print(state)

    total_space = 70_000_000
    min_unused = 30_000_000
    unused = total_space - state["root"][0]
    return sorted([
        (dir, size)
        for dir, (size, isdir) in state.items()
        if isdir and (unused + size) >= min_unused
    ], key=lambda t: t[1])[0][1]
