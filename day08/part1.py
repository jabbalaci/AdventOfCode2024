#!/usr/bin/env python3

import string
import sys
from itertools import combinations
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------

char = str

GridType = list[list[char]]

ACCEPTED_CHARS = string.ascii_letters + string.digits


class Point(NamedTuple):
    row: int
    col: int


class Antenna(NamedTuple):
    value: char
    row: int
    col: int


# ----------------------------------------------------------------------------


class Antinodes:
    def __init__(self, parent: "Grid") -> None:
        self.parent: Grid = parent
        self.antennas: list[Antenna] = self.parent.antennas
        self.unique_ids: list[char] = sorted(set([a.value for a in self.antennas]))
        self.antinodes: set[Point] = self.process()

    def is_inside(self, p: Point) -> bool:
        return (0 <= p.row < self.parent.no_of_rows) and (0 <= p.col < self.parent.no_of_cols)

    def process(self) -> set[Point]:
        antinodes: set[Point] = set()
        for _id in self.unique_ids:
            current_antennas: list[Antenna] = [a for a in self.antennas if a.value == _id]
            for a, b in combinations(current_antennas, 2):
                diff_x = a.col - b.col
                diff_y = a.row - b.row
                #
                p1 = Point(col=a.col + diff_x, row=a.row + diff_y)
                p2 = Point(col=b.col - diff_x, row=b.row - diff_y)
                #
                if self.is_inside(p1):
                    antinodes.add(p1)
                if self.is_inside(p2):
                    antinodes.add(p2)
            #
        #
        return antinodes


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.update_matrix()
        self.antennas: list[Antenna] = self.locate_antennas()
        self.no_of_rows: int = len(self.matrix)
        self.no_of_cols: int = len(self.matrix[0])

    def locate_antennas(self):
        li: list[Antenna] = []
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c in ACCEPTED_CHARS:
                    li.append(Antenna(value=c, row=i, col=j))
                #
            #
        #
        return li

    def update_matrix(self):
        """Hashmarks (#) are replaced with dots (.)"""
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == "#":
                    self.matrix[i][j] = "."
                #
            #
        #

    def start(self) -> None:
        self.antinodes = Antinodes(self)

    def get_result(self) -> int:
        return len(self.antinodes.antinodes)

    def show(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                c = self.matrix[i][j]
                p = Point(row=i, col=j)
                if p in self.antinodes.antinodes:
                    c = "#"
                if self.matrix[i][j] in ACCEPTED_CHARS:
                    c = self.matrix[i][j]
                sys.stdout.write(c)
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"
    # fname = "example2.txt"
    # fname = "example3.txt"
    # fname = "example4.txt"
    # fname = "example5.txt"

    fname = "input.txt"

    g = Grid(fname)
    g.start()

    result = g.get_result()
    print(result)

    # g.show()


##############################################################################

if __name__ == "__main__":
    main()
