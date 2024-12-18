#!/usr/bin/env python3

"""
Works with the two examples,
doesn't work with the real input.

Using Dijkstra's algorithm.

TODO: fix it
"""

import pprint
import sys
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

import helper

char = str

GridType = list[list[char]]

INFINITY = sys.maxsize  # a very big number


class Dir(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    DUMMY = "?"


TURN_LEFT = [Dir.UP, Dir.LEFT, Dir.DOWN, Dir.RIGHT, Dir.UP, Dir.LEFT, Dir.DOWN]
TURN_RIGHT = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT, Dir.UP, Dir.RIGHT, Dir.DOWN]


class Point(NamedTuple):
    row: int
    col: int


@dataclass
class Entry:
    node: Point
    dir: Dir
    dist_from_start: int
    prev_node: Point


DUMMY_POINT = Point(-1, -1)

# ----------------------------------------------------------------------------


class Maze:
    def __init__(self, fname: str) -> None:
        self.matrix: GridType = [list(line) for line in helper.read_lines(fname)]
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
        self.start_point: Point = maze.start_point
        self.end_point: Point = maze.end_point
        self.visited: set[Point] = set()
        self.unvisited: set[Point] = set(self.maze.get_all_points())
        self.table: dict[Point, Entry] = self.init_table()

    def init_table(self) -> dict[Point, Entry]:
        d: dict[Point, Entry] = {}
        for p in self.unvisited:
            d[p] = Entry(node=p, dir=Dir.DUMMY, dist_from_start=INFINITY, prev_node=DUMMY_POINT)
        #
        d[self.start_point].dir = Dir.RIGHT
        d[self.start_point].dist_from_start = 0
        #
        return d

    def get_direction_from_to(self, p1: Point, p2: Point) -> Dir:
        """
        If we want to go from p1 to p2, which direction do we need to take?
        That is, where is p2 compared to p1?
        """
        assert p1 != p2, "the two points must be different"
        result: Dir
        if p2.row < p1.row:
            result = Dir.UP
        elif p2.row > p1.row:
            result = Dir.DOWN
        else:
            if p2.col < p1.col:
                result = Dir.LEFT
            else:
                result = Dir.RIGHT
            #
        #
        return result

    def get_lowest_number_of_turns(self, dir1: Dir, dir2: Dir) -> int:
        if dir1 == dir2:
            return 0
        # else:
        idx1 = TURN_LEFT.index(dir1)
        idx2 = idx1 + 1
        while TURN_LEFT[idx2] != dir2:
            idx2 += 1
        #
        idx3 = TURN_RIGHT.index(dir1)
        idx4 = idx3 + 1
        while TURN_RIGHT[idx4] != dir2:
            idx4 += 1
        #
        return min([idx2 - idx1, idx4 - idx3])

    def get_cost_from_to(self, node1: Entry, node2: Entry) -> int:
        """
        Returns the cost of moving from node1 to node2.
        """
        # position of node2 compared to node1 (up, left, down, right):
        where_is_node2: Dir = self.get_direction_from_to(node1.node, node2.node)
        required_turns: int = self.get_lowest_number_of_turns(node1.dir, where_is_node2)
        #
        return (1000 * required_turns) + 1

    def start(self) -> None:
        while len(self.unvisited) > 0:  # not empty
            curr_entry: Entry = sorted(
                [self.table[p] for p in self.unvisited], key=lambda e: e.dist_from_start
            )[0]
            curr_value: int = curr_entry.dist_from_start
            #
            neighbors = self.maze.get_all_four_neighbors(curr_entry.node)
            unvisited_neighbors: set[Point] = self.unvisited.intersection(neighbors)
            for nb in unvisited_neighbors:
                nb_entry: Entry = self.table[nb]
                nb_cost = self.get_cost_from_to(curr_entry, nb_entry)
                nb_new_value: int = curr_value + nb_cost
                if nb_new_value < nb_entry.dist_from_start:
                    nb_entry.dist_from_start = nb_new_value
                    nb_entry.prev_node = curr_entry.node
                    nb_entry.dir = self.get_direction_from_to(curr_entry.node, nb_entry.node)
                #
            #
            self.unvisited.remove(curr_entry.node)
            self.visited.add(curr_entry.node)

            # self.show()
        #

    def debug(self) -> None:
        pass

    def get_result(self) -> int:
        node: Entry = self.table[self.end_point]
        return node.dist_from_start

    def show(self) -> None:
        pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")

    def show_maze_with_path(self):
        path: list[Point] = []
        node: Entry = self.table[self.end_point]
        while (prev_point := node.prev_node) != self.start_point:
            path.append(prev_point)
            node = self.table[prev_point]
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
                        node = self.table[p]
                        sys.stdout.write(node.dir.value)
                    else:
                        sys.stdout.write(".")
                    #
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    fname = "example1.txt"  # score: 7036
    # fname = "example2.txt"  # score: 11048
    # fname = "input.txt"

    maze = Maze(fname)
    # maze.show()

    d = Dijkstra(maze)

    # d.debug()

    d.start()

    # d.show()
    d.show_maze_with_path()

    result = d.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
