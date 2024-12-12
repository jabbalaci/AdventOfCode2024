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


class Triplet(NamedTuple):
    row: int
    col: int
    value: char


# ----------------------------------------------------------------------------


class Region:
    def __init__(self, parent: "Grid", _id: char) -> None:
        self.parent = parent
        self._id = _id
        self.points: set[Point] = set()

    def add(self, p: Point) -> None:
        self.points.add(p)

    def contains(self, p: Point) -> bool:
        return p in self.points

    def area(self) -> int:
        return len(self.points)

    def perimeter(self) -> int:
        fence = 0

        for p in self.points:
            for nb in self.parent.get_all_four_neighbors(p):
                if not self.contains(nb):
                    fence += 1
                #
            #
        #
        return fence

    def price(self) -> int:
        return self.area() * self.perimeter()

    def debug(self) -> None:
        print("_id:      ", self._id)
        print("area:     ", self.area())
        print("perimeter:", self.perimeter())
        # print(self.points)


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.regions: list[Region] = []
        self.find_regions()

    def find_regions(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if not self.found(i, j):
                    r: Region = self.fill(i, j)
                    self.regions.append(r)
                #
            #
        #

    def get_neighbors(self, p: Point) -> list[Triplet]:
        """Returns valid (inside the grid) neighbors only as triplets."""
        result: list[Triplet] = []
        i, j = p.row, p.col

        positions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        for i, j in positions:
            value = self.get_cell_value(i, j)
            if value != ".":
                result.append(Triplet(row=i, col=j, value=value))
            #
        #
        return result

    def get_all_four_neighbors(self, p: Point) -> list[Point]:
        """Returns all four neighboring points (even if they're outside of the grid)."""
        result: list[Point] = []
        i, j = p.row, p.col

        positions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        for i, j in positions:
            result.append(Point(row=i, col=j))
        #
        return result

    def fill(self, i: int, j: int) -> Region:
        r = Region(self, _id=self.matrix[i][j])
        q = deque([Point(row=i, col=j)])
        done: set[Point] = set()

        while len(q) > 0:
            p = q.popleft()
            r.add(p)
            done.add(p)
            for tr in self.get_neighbors(p):
                nb = Point(row=tr.row, col=tr.col)
                if (nb not in done) and (nb not in q) and (tr.value == r._id):
                    q.append(nb)
                #
            #
        #
        return r

    def found(self, row: int, col: int) -> bool:
        for r in self.regions:
            if r.contains(Point(row, col)):
                return True
            #
        #
        return False

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

    def show_regions(self) -> None:
        for r in self.regions:
            r.debug()
            print("---")

    def get_result(self) -> int:
        return sum([r.price() for r in self.regions])


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"  # price: 140
    # fname = "example2.txt"  # price: 772
    # fname = "example3.txt"  # price: 1930

    fname = "input.txt"

    g = Grid(fname)
    g.start()

    result = g.get_result()
    print(result)

    # g.show()
    # g.show_regions()


##############################################################################

if __name__ == "__main__":
    main()
