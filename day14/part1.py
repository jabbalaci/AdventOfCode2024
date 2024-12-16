#!/usr/bin/env python3

import math
import sys

from parse import parse

import helper

# ----------------------------------------------------------------------------


class Robot:
    def __init__(self, parent: "Area", px: int, py: int, vx: int, vy: int) -> None:
        self.parent = parent
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def move(self) -> None:
        x = self.px + self.vx
        y = self.py + self.vy
        self.px = x % self.parent.width
        self.py = y % self.parent.height

    def quadrant(self) -> int:
        """
        Where is the robot? In which quadrant?
        +---+---+
        | 1 | 2 |
        +---+---+
        | 3 | 4 |
        +---+---+
        Returns 0 if the robot is not in any quadrant
        (i.e., it's in the middle either vertically or horizontally).
        """
        vertical_split = self.parent.width // 2
        horizontal_split = self.parent.height // 2
        if self.px < vertical_split:
            if self.py < horizontal_split:
                return 1
            if self.py > horizontal_split:
                return 3
        if self.px > vertical_split:
            if self.py < horizontal_split:
                return 2
            if self.py > horizontal_split:
                return 4
        #
        return 0


# ----------------------------------------------------------------------------


class Area:
    def __init__(self, fname: str, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.robots: list[Robot] = []
        self.read_input_file(fname)

    def read_input_file(self, fname: str) -> None:
        lines: list[str] = helper.read_lines(fname)
        for line in lines:
            p = parse("p={px:d},{py:d} v={vx:d},{vy:d}", line)
            self.robots.append(Robot(self, p["px"], p["py"], p["vx"], p["vy"]))
        #

    def get_robots_at(self, x: int, y: int) -> list[Robot]:
        result: list[Robot] = []

        for r in self.robots:
            if (r.px == x) and (r.py == y):
                result.append(r)
            #
        #
        return result

    def start(self, iteration: int) -> None:
        # self.show("Initial state:")
        for i in range(iteration):
            sec = i + 1
            for r in self.robots:
                r.move()
            #
            # self.show(f"After {sec} second:")
        #

    def get_result(self) -> int:
        quads = [0, 0, 0, 0, 0]
        for r in self.robots:
            quads[r.quadrant()] += 1
        #
        return math.prod(quads[1:])

    def show(self, caption: str) -> None:
        print(caption)
        for i in range(self.height):
            for j in range(self.width):
                no_of_robots = len(self.get_robots_at(y=i, x=j))
                assert no_of_robots < 10, "too many robots, drawing error"
                if no_of_robots == 0:
                    sys.stdout.write(".")
                else:
                    print(no_of_robots, end="")
                #
            #
            print()
        #
        print()


# ----------------------------------------------------------------------------


def main() -> None:
    # area = Area("example1.txt", 11, 7)
    # area = Area("example2.txt", 11, 7)

    area = Area("input.txt", 101, 103)

    area.start(100)

    result = area.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
