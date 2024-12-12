#!/usr/bin/env python3

import sys
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------

char = str

GridType = list[list[char]]


class Point(NamedTuple):
    row: int
    col: int
    value: int


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]

    def get_cell_value(self, i: int, j: int, default=".") -> char:
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def start(self) -> None:
        pass

    def show(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                sys.stdout.write(c)
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    fname = "example1.txt"
    # fname = "example2.txt"
    # fname = "example3.txt"

    # fname = "input.txt"

    g = Grid(fname)
    g.start()

    g.show()


##############################################################################

if __name__ == "__main__":
    main()
