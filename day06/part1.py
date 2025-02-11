#!/usr/bin/env python3


import copy
from enum import Enum
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------

char = str

GridType = list[list[char]]


class Dir(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Point(NamedTuple):
    row: int
    col: int


TURN_RIGHT = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT, Dir.UP]


# ----------------------------------------------------------------------------


class Guard:
    """A guard's head has a position (row, col) and a direction."""

    def __init__(self, parent: "Grid") -> None:
        self.parent: Grid = parent
        self.row, self.col = self.find_guard()
        self.direction = Dir.UP

    def find_guard(self) -> Point:
        for i, row in enumerate(self.parent.matrix):
            for j, c in enumerate(row):
                if c == "^":
                    return Point(row=i, col=j)
                #
            #
        #
        assert False, "cannot get here"

    def turn_right(self) -> None:
        idx = TURN_RIGHT.index(self.direction)
        self.direction = TURN_RIGHT[idx + 1]

    def is_inside(self) -> bool:
        return (0 <= self.row < self.parent.no_of_rows) and (0 <= self.col < self.parent.no_of_cols)

    def get_position_in_front(self) -> Point:
        if self.direction == Dir.UP:
            return Point(row=self.row - 1, col=self.col)
        elif self.direction == Dir.RIGHT:
            return Point(row=self.row, col=self.col + 1)
        elif self.direction == Dir.DOWN:
            return Point(row=self.row + 1, col=self.col)
        else:  # Dir.LEFT
            return Point(row=self.row, col=self.col - 1)

    def move(self) -> None:
        in_front: Point = self.get_position_in_front()
        value = self.parent.get_cell_value(in_front.row, in_front.col)
        if value == "#":
            self.turn_right()
        else:  # value == '.'
            self.row, self.col = in_front


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.guard = Guard(self)
        self.visited: set[Point] = set()
        self.visited.add(Point(row=self.guard.row, col=self.guard.col))
        self.no_of_rows: int = len(self.matrix)
        self.no_of_cols: int = len(self.matrix[0])

    def get_cell_value(self, i: int, j: int, default=".") -> char:
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def start(self) -> None:
        while True:
            self.guard.move()
            if not self.guard.is_inside():
                break
            # else, if inside
            self.visited.add(Point(row=self.guard.row, col=self.guard.col))
            #
            # self.show()
            # input("Press ENTER to continue...")
        #

    def get_result(self) -> int:
        return len(self.visited)

    def show(self) -> None:
        lines = copy.deepcopy(self.matrix)
        #
        for v in self.visited:
            lines[v.row][v.col] = "X"
        #
        for line in lines:
            print("".join(line))


# ----------------------------------------------------------------------------


def main():
    # fname = "example.txt"
    fname = "input.txt"

    g = Grid(fname)
    g.start()

    result = g.get_result()
    print(result)

    # g.show()


##############################################################################

if __name__ == "__main__":
    main()
