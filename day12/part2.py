#!/usr/bin/env python3

import sys
from collections import deque
from enum import Enum, auto
from pprint import pprint
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------

char = str

GridType = list[list[char]]


class FenceType(Enum):
    TOP = auto()  # the fence is above a letter
    BOTTOM = auto()  # the fence is below a letter
    LEFT = auto()  # the fence is on the left side of a letter
    RIGHT = auto()  # the fence is on the right side of a letter


class Point(NamedTuple):
    row: int
    col: int


class Triplet(NamedTuple):
    row: int
    col: int
    value: char


class FencePart(NamedTuple):
    row: int
    col: int
    type: FenceType


# ----------------------------------------------------------------------------


class Cluster:
    def __init__(self, points: list[Point], _type: FenceType) -> None:
        self.points: list[Point] = points
        self._type: FenceType = _type

    def distance_ok(self, prev: Point, new: Point, _type: FenceType) -> bool:
        assert prev != new, "the two points must be different"
        #
        diff_x = new.col - prev.col
        diff_y = new.row - prev.row
        if _type in (FenceType.TOP, FenceType.BOTTOM):
            return diff_y == 0 and diff_x == 1
        else:  # if _type in (FenceType.LEFT, FenceType.RIGHT)
            return diff_x == 0 and diff_y == 1

    def get_clusters(self) -> dict[int, list[Point]]:
        clusters: dict[int, list[Point]] = {}
        cid = 0

        for i, p in enumerate(self.points):
            if i == 0:
                clusters[cid] = []
                clusters[cid].append(p)
            else:
                last = clusters[cid][-1]
                if self.distance_ok(last, p, self._type):
                    clusters[cid].append(p)
                else:
                    cid += 1
                    clusters[cid] = []
                    clusters[cid].append(p)

        return clusters

    def no_of_clusters(self) -> int:
        return len(self.get_clusters())


# ----------------------------------------------------------------------------


class Region:
    def __init__(self, parent: "Grid", _id: char) -> None:
        self.parent = parent
        self._id = _id
        self.points: set[Point] = set()
        self.fence_parts: list[FencePart] = []

    def add(self, p: Point) -> None:
        self.points.add(p)

    def contains(self, p: Point) -> bool:
        return p in self.points

    def area(self) -> int:
        return len(self.points)

    def find_perimeter_parts(self) -> None:
        for p in self.points:
            up, right, down, left = self.parent.get_all_four_neighbors(p)
            if not self.contains(up):
                self.fence_parts.append(FencePart(row=up.row, col=up.col, type=FenceType.TOP))
            #
            if not self.contains(down):
                self.fence_parts.append(
                    FencePart(row=down.row, col=down.col, type=FenceType.BOTTOM)
                )
            #
            if not self.contains(right):
                self.fence_parts.append(
                    FencePart(row=right.row, col=right.col, type=FenceType.RIGHT)
                )
            #
            if not self.contains(left):
                self.fence_parts.append(FencePart(row=left.row, col=left.col, type=FenceType.LEFT))
            #
        #

    def perimeter(self) -> int:
        row_min = min(p.row for p in self.fence_parts)
        row_max = max(p.row for p in self.fence_parts)
        col_min = min(p.col for p in self.fence_parts)
        col_max = max(p.col for p in self.fence_parts)

        result = 0
        for curr_col in range(row_min, row_max + 1):
            types = [FenceType.TOP, FenceType.BOTTOM]
            for _type in types:
                points = sorted(
                    [
                        Point(row=p.row, col=p.col)
                        for p in self.fence_parts
                        if (p.type == _type) and (p.row == curr_col)
                    ]
                )
                cl = Cluster(points, _type)
                result += cl.no_of_clusters()
            #
        #
        for curr_col in range(col_min, col_max + 1):
            types = [FenceType.LEFT, FenceType.RIGHT]
            for _type in types:
                points = sorted(
                    [
                        Point(row=p.row, col=p.col)
                        for p in self.fence_parts
                        if (p.type == _type) and (p.col == curr_col)
                    ]
                )
                cl = Cluster(points, _type)
                result += cl.no_of_clusters()
            #
        #
        return result

    def price(self) -> int:
        return self.area() * self.perimeter()

    def debug(self) -> None:
        print("_id:      ", self._id)
        print("area:     ", self.area())
        print("perimeter:", self.perimeter())
        types = [FenceType.TOP, FenceType.RIGHT, FenceType.BOTTOM, FenceType.LEFT]
        for _type in types:
            print("   ", _type.name, end=": ")
            points = sorted(
                [Point(row=p.row, col=p.col) for p in self.fence_parts if p.type == _type]
            )
            print(points)
            cl = Cluster(points, _type)
            pprint(cl.get_clusters())


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.regions: list[Region] = []

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
        """
        Returns all four neighboring points (even if they're outside of the grid).

        The four points are returned in this order: up, right, down, left.
        """
        result: list[Point] = []
        i, j = p.row, p.col

        #            up          right        down       left
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
        self.find_regions()
        for r in self.regions:
            r.find_perimeter_parts()

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
    # fname = "example1.txt"  # price: 80
    # fname = "example2.txt"  # price: 436
    # fname = "example3.txt"  # price: 1206
    # fname = "example10.txt"  # price: 236
    # fname = "example11.txt"  # price: 368

    fname = "input.txt"

    g = Grid(fname)
    g.start()

    # g.show()
    # g.show_regions()

    result = g.get_result()
    print(result)

    # print("---")
    # g.show()


##############################################################################

if __name__ == "__main__":
    main()
