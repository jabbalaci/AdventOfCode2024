#!/usr/bin/env python3

"""
I suffered a lot with this one,
and my solution is quite slow.

I'm not sure that it gives the correct answer for example3.txt .
However, it worked for the input.
"""

from __future__ import annotations

import pprint
import sys
from enum import Enum
from functools import lru_cache
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


class Entry:
    def __init__(self, point: Point, dir: Dir, cost: int, prev_point: Point) -> None:
        self.point = point
        self.dir = dir
        self.cost = cost
        self.prev_point = prev_point

    def copy(self) -> Entry:
        return Entry(
            point=self.point,
            dir=self.dir,
            cost=self.cost,
            prev_point=self.prev_point,
        )


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
        self.visited: set[Entry] = set()
        self.unvisited: set[Entry] = set()
        self.init_dijkstra()

    @lru_cache
    def get_entry_by_point(self, p: Point) -> Entry | None:
        for e in self.unvisited:
            if e.point == p:
                return e
            #
        #
        for e in self.visited:
            if e.point == p:
                return e
            #
        #
        return None  # not found

    def init_dijkstra(self) -> None:
        for p in self.maze.get_all_points():
            self.unvisited.add(Entry(point=p, dir=Dir.DUMMY, cost=INFINITY, prev_point=DUMMY_POINT))
        #
        self.get_entry_by_point(self.start_point).dir = Dir.RIGHT  # type: ignore
        self.get_entry_by_point(self.start_point).cost = 0  # type: ignore

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

    @lru_cache
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
        where_is_node2: Dir = self.get_direction_from_to(node1.point, node2.point)
        required_turns: int = self.get_lowest_number_of_turns(node1.dir, where_is_node2)
        #
        return (1000 * required_turns) + 1

    def start(self) -> None:
        while len(self.unvisited) > 0:  # not empty
            # print("# unvisited:", len(self.unvisited))
            curr_entry: Entry = min(self.unvisited, key=lambda e: e.cost)
            curr_value: int = curr_entry.cost
            #
            neighbors_points: list[Point] = self.maze.get_all_four_neighbors(curr_entry.point)
            neighbors_entries: set[Entry] = set()
            for p in neighbors_points:
                if e := self.get_entry_by_point(p):
                    neighbors_entries.add(e)
                #
            #
            unvisited_neighbors: set[Entry] = self.unvisited.intersection(neighbors_entries)
            for nb_entry in unvisited_neighbors:
                nb_cost = self.get_cost_from_to(curr_entry, nb_entry)
                # if nb_cost > 1:  # must turn
                # copy: Entry = curr_entry.copy()
                # copy.cost += 1000
                # copy.dir = self.get_direction_from_to(curr_entry.point, nb_entry.point)
                # self.unvisited.add(copy)
                #
                nb_new_value: int = curr_value + nb_cost
                if nb_new_value < nb_entry.cost:
                    nb_entry.cost = nb_new_value
                    nb_entry.prev_point = curr_entry.point
                    nb_entry.dir = self.get_direction_from_to(curr_entry.point, nb_entry.point)
                    #
                    if nb_cost > 1:  # must turn
                        copy: Entry = curr_entry.copy()
                        copy.cost += 1000
                        copy.dir = nb_entry.dir
                        self.unvisited.add(copy)
                    #
                #
            #
            self.unvisited.remove(curr_entry)
            self.visited.add(curr_entry)

            # self.show()
        #

    def debug(self) -> None:
        pass

    def get_result(self) -> int:
        node: Entry = self.get_entry_by_point(self.end_point)  # type: ignore
        return node.cost

    def show(self) -> None:
        # pprint.pprint(self.table)
        print("# visited:", self.visited)
        print("# unvisited:", self.unvisited)
        print("---")
        input("Press ENTER to continue...")

    def show_maze_with_path(self):
        path: list[Point] = []
        node: Entry = self.get_entry_by_point(self.end_point)  # type: ignore
        while (prev_point := node.prev_point) != self.start_point:
            path.append(prev_point)
            node = self.get_entry_by_point(prev_point)  # type: ignore
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
                        node = self.get_entry_by_point(p)  # type: ignore
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
    # fname = "example1.txt"  # score: 7036
    # fname = "example2.txt"  # score: 11048
    # fname = "example3.txt"  # correct path would be the lower path, not the upper
    # fname = "example4.txt"  # score should be: 4013
    fname = "input.txt"

    maze = Maze(fname)
    # maze.show()

    d = Dijkstra(maze)

    # d.debug()

    d.start()

    # d.show()
    # d.show_maze_with_path()

    result = d.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
