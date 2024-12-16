#!/usr/bin/env python3

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

    def is_there_a_robot_at(self, x: int, y: int) -> bool:
        for r in self.robots:
            if (r.px == x) and (r.py == y):
                return True
            #
        #
        return False

    def start(self) -> None:
        # self.show("Initial state:")
        i = 0
        while True:
            sec = i + 1
            # print("# sec.:", sec)
            for r in self.robots:
                r.move()
            #
            if self.xmas_tree_found():
                print(f"Sec.: {sec}")
                self.show()
                print(f"Sec.: {sec}")
                break
            #
            i += 1
        #

    def xmas_tree_found(self) -> bool:
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += "*" if self.is_there_a_robot_at(y=i, x=j) else "."
            #
            if "*******" in line:
                return True
            #
        #
        return False

    def show(self, caption="") -> None:
        if caption:
            print(caption)
        #
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

    area.start()

    # area.show()


##############################################################################

if __name__ == "__main__":
    main()
