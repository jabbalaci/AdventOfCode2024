#!/usr/bin/env python3


from __future__ import annotations

import heapq
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


DUMMY_POINT = Point(-1, -1)

# PICOSECONDS_TO_SAVE = 30  # example
PICOSECONDS_TO_SAVE = 100  # real input

# ----------------------------------------------------------------------------


@dataclass
class Entry:
    node: Point
    dist_from_start: int
    prev_node: Point

    def __lt__(self, other: Entry):
        return self.dist_from_start < other.dist_from_start


# ----------------------------------------------------------------------------


class Maze:
    def __init__(self, fname: str, cheat: bool = False) -> None:
        self.cheat = cheat
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
        self.width: int = len(self.matrix[0])
        self.height: int = len(self.matrix)
        self.start_point: Point
        self.end_point: Point
        self.traverse_matrix()

    def traverse_matrix(self) -> None:
        """Find start point, find end point, replace S and E with dot (.)"""
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == "S":
                    self.start_point = Point(row=i, col=j)
                    self.matrix[i][j] = "."
                elif c == "E":
                    self.end_point = Point(row=i, col=j)
                    self.matrix[i][j] = "."
                #
            #
        #

    def get_cell_value(self, row: int, col: int, default="#") -> char:
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

    def get_all_possible_walls(self) -> list[Point]:
        """
        Returns the list of possible walls.
        What walls are NOT returned:
        - a wall in the border
        - a wall surrounded by 4 walls
        """
        result: list[Point] = []
        #
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.get_cell_value(row=i, col=j) == "#":
                    p = Point(row=i, col=j)
                    around = ""
                    for nb in self.get_all_four_neighbors(p):
                        around += self.get_cell_value(row=nb.row, col=nb.col)
                    #
                    if "." in around:
                        result.append(p)
                    #
                #
            #
        #
        return result

    def replace(self, p: Point, new_value: char) -> None:
        self.matrix[p.row][p.col] = new_value

    def show(self) -> None:
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                p = Point(row=i, col=j)
                if p == self.start_point:
                    sys.stdout.write("S")
                elif p == self.end_point:
                    sys.stdout.write("E")
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #


# ----------------------------------------------------------------------------


class Dijkstra:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.start_point: Point = self.maze.start_point
        self.end_point: Point = self.maze.end_point
        self.visited: set[Point]
        self.unvisited: set[Point]
        self.table: dict[Point, Entry]

    def reset(self) -> None:
        self.visited = set()
        self.unvisited = set(self.maze.get_all_points())
        self.table = self.init_table()

    def init_table(self) -> dict[Point, Entry]:
        d: dict[Point, Entry] = {}
        for p in self.unvisited:
            d[p] = Entry(node=p, dist_from_start=INFINITY, prev_node=DUMMY_POINT)
        #
        d[self.start_point].dist_from_start = 0
        #
        return d

    def start(self, first_run: bool, original_picoseconds: int = -1) -> int:
        """
        Returns:
        * 1, if we could save at least 100 picoseconds
        * 0, otherwise
        """
        self.reset()
        #
        unvisited_heap: list[Entry] = [self.table[p] for p in self.unvisited]
        while len(self.unvisited) > 0:  # not empty
            heapq.heapify(unvisited_heap)
            entry: Entry = heapq.heappop(unvisited_heap)
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

            # if we reached the end point, then we can stop
            if not first_run:
                if entry.node == self.end_point:
                    saved = original_picoseconds - entry.dist_from_start
                    # print("# early stoppage")
                    if saved >= PICOSECONDS_TO_SAVE:
                        return 1
                    else:
                        return 0
                    #
                #
            #

            # self.show()
        #
        return 0

    def process(self) -> None:
        # execute once and measure the picoseconds
        self.start(first_run=True)
        original_picoseconds = self.get_result()
        #
        # self.show_maze_with_path()
        # print(original_picoseconds)
        walls: list[Point] = self.maze.get_all_possible_walls()
        counter = 0
        print("# number of possible walls:", len(walls))
        for idx, p in enumerate(walls):
            print("# this is wall no.", idx + 1)
            self.maze.replace(p, ".")
            #
            counter += self.start(first_run=False, original_picoseconds=original_picoseconds)
            print("# counter:", counter)
            #
            self.maze.replace(p, "#")
        #
        print("---")
        print(counter)

    def get_result(self) -> int:
        """
        How many steps are needed to go from S to E?
        """
        cheat: bool = self.maze.cheat  # noqa
        path: list[Point] = self.collect_path()
        result = len(path) + 1  # since the path doesn't include S and E
        return result

    def collect_path(self) -> list[Point]:
        """
        Returns the path between S and E.
        The returned path doesn't include S and E.
        """
        path: list[Point] = []
        node: Entry = self.table[self.end_point]
        while (prev_point := node.prev_node) != self.start_point:
            path.append(prev_point)
            node = self.table[prev_point]
        #
        return path

    def show(self) -> None:
        pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")

    def show_maze_with_path(self):
        path: list[Point] = self.collect_path()
        #
        for i, row in enumerate(self.maze.matrix):
            for j, c in enumerate(row):
                p = Point(row=i, col=j)
                if p == self.start_point:
                    sys.stdout.write("S")
                elif p == self.end_point:
                    sys.stdout.write("E")
                elif c == ".":
                    if p in path:
                        sys.stdout.write("·")
                    else:
                        sys.stdout.write(" ")
                    #
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    # m = Maze("example.txt")  # 84
    # m = Maze("example_cheat1.txt", cheat=True)  # 72, saved: 84 - 72 = 12
    # m = Maze("example_cheat2.txt", cheat=True)  # 64, saved: 20
    # m = Maze("example_cheat3.txt", cheat=True)  # 46, saved: 38
    # m = Maze("example_cheat4.txt", cheat=True)  # 20, saved: 64
    #
    m = Maze("input.txt")  # 9380

    # m.show()

    d = Dijkstra(m)

    d.process()


##############################################################################

if __name__ == "__main__":
    main()
