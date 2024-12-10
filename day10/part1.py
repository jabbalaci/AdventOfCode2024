#!/usr/bin/env python3

import sys
from collections import deque
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


class Hiking:
    def __init__(self, parent: "Grid") -> None:
        self.parent = parent

    def get_neighbors(self, p: Point) -> list[Point]:
        result: list[Point] = []
        i, j = p.row, p.col

        positions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        for i, j in positions:
            value = self.parent.get_cell_value(i, j)
            if value.isdigit():
                result.append(Point(row=i, col=j, value=int(value)))
            #
        #
        return result

    def process(self, zero: Point) -> int:
        """Returns the score of a trailhead."""
        q = deque([zero])
        nines: set[Point] = set()

        while len(q) > 0:
            p: Point = q.popleft()
            if p.value == 9:
                nines.add(p)
            #
            neighbors: list[Point] = self.get_neighbors(p)
            for nb in neighbors:
                if nb.value == p.value + 1:
                    q.append(nb)
                #
            #
        #
        score = len(nines)  # how many different 9s can be reached
        return score


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.zeros: list[Point] = self.find_zeros()

    def find_zeros(self) -> list[Point]:
        result: list[Point] = []
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == "0":
                    result.append(Point(row=i, col=j, value=0))
                #
            #
        #
        return result

    def get_cell_value(self, i: int, j: int, default=".") -> char:
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def start(self) -> None:
        h = Hiking(self)

        result = 0
        for zero in self.zeros:
            score = h.process(zero)
            result += score
        #
        print(result)

    def show(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                sys.stdout.write(c)
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"  # score: 1
    # fname = "example2.txt"  # score: 2
    # fname = "example3.txt"  # score: 4
    # fname = "example4.txt"  # score: 3
    # fname = "example5.txt"  # score: 36

    fname = "input.txt"

    g = Grid(fname)
    g.start()

    # g.show()


##############################################################################

if __name__ == "__main__":
    main()
