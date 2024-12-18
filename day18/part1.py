#!/usr/bin/env python3

import pprint
import sys
from dataclasses import dataclass
from typing import NamedTuple

import helper

char = str

GridType = list[list[char]]

INFINITY = sys.maxsize  # a very big number


class Point(NamedTuple):
    row: int
    col: int


@dataclass
class Entry:
    node: Point
    dist_from_start: int
    prev_node: Point


DUMMY_POINT = Point(-1, -1)

# ----------------------------------------------------------------------------


class Maze:
    def __init__(self, fname: str, size: int, lines_to_process: int) -> None:
        self.width, self.height = size, size
        self.matrix: GridType = [list("." * self.width) for _ in range(self.height)]
        self.bytes: list[Point] = self.read_input(fname)
        self.bytes = self.bytes[:lines_to_process]
        self.update_matrix()

    def read_input(self, fname: str) -> list[Point]:
        result: list[Point] = []
        #
        lines: list[str] = helper.read_lines(fname)
        for line in lines:
            x, y = line.split(",")
            result.append(Point(row=int(y), col=int(x)))
        #
        return result

    def update_matrix(self) -> None:
        for p in self.bytes:
            self.matrix[p.row][p.col] = "#"
        #

    def get_cell_value(self, row: int, col: int, default=" ") -> char:
        """Space means: the position is outside of the matrix."""
        i, j = row, col
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def get_all_points(self) -> list[Point]:
        """Returns the available points, where we can move."""
        result: list[Point] = []
        #
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == ".":
                    result.append(Point(row=i, col=j))
                #
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

    def show(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                sys.stdout.write(c)
            #
            print()
        #


# ----------------------------------------------------------------------------


class Dijkstra:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.start_point: Point = Point(row=0, col=0)
        self.end_point: Point = Point(row=self.maze.height - 1, col=self.maze.width - 1)
        self.visited: set[Point] = set()
        self.unvisited: set[Point] = set(self.maze.get_all_points())
        self.table: dict[Point, Entry] = self.init_table()

    def init_table(self) -> dict[Point, Entry]:
        d: dict[Point, Entry] = {}
        for p in self.unvisited:
            d[p] = Entry(node=p, dist_from_start=INFINITY, prev_node=DUMMY_POINT)
        #
        d[self.start_point].dist_from_start = 0
        #
        return d

    def start(self) -> None:
        while len(self.unvisited) > 0:  # not empty
            entry: Entry = sorted(
                [self.table[p] for p in self.unvisited], key=lambda e: e.dist_from_start
            )[0]
            current_value: int = entry.dist_from_start
            #
            neighbors = self.maze.get_all_four_neighbors(entry.node)
            unvisited_neighbors: set[Point] = self.unvisited.intersection(neighbors)
            for nb in unvisited_neighbors:
                nb_entry: Entry = self.table[nb]
                nb_distance = 1
                nb_new_value: int = current_value + nb_distance
                if nb_new_value < nb_entry.dist_from_start:
                    nb_entry.dist_from_start = nb_new_value
                    nb_entry.prev_node = entry.node
                #
            #
            self.unvisited.remove(entry.node)
            self.visited.add(entry.node)

            # self.show()
        #

    def get_result(self) -> int:
        node = self.table[self.end_point]
        return node.dist_from_start

    def show(self) -> None:
        pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")


# ----------------------------------------------------------------------------


def main() -> None:
    # m = Maze("example.txt", size=7, lines_to_process=12)
    m = Maze("input.txt", size=71, lines_to_process=1024)

    # m.show()

    d = Dijkstra(m)

    d.start()

    result = d.get_result()
    print(result)

    # d.show()


##############################################################################

if __name__ == "__main__":
    main()
