#!/usr/bin/env python3

"""
Naive approach.
Works well for Part 1.
"""

from typing import NamedTuple

from parse import parse

import helper


class Button(NamedTuple):
    x: int
    y: int


# each button was pressed how many times
class Press(NamedTuple):
    a: int
    b: int


# ----------------------------------------------------------------------------


class Machine:
    def __init__(self, content: str) -> None:
        self.a, self.b, self.prize = self.parse_lines(content)
        self.solutions: list[Press] = []

    def parse_lines(self, content: str) -> tuple[Button, Button, Button]:
        lines = content.splitlines()
        p = parse("Button A: X+{x:d}, Y+{y:d}", lines[0])
        a = Button(x=p["x"], y=p["y"])
        p = parse("Button B: X+{x:d}, Y+{y:d}", lines[1])
        b = Button(x=p["x"], y=p["y"])
        p = parse("Prize: X={x:d}, Y={y:d}", lines[2])
        prize = Button(x=p["x"], y=p["y"])
        #
        return (a, b, prize)

    def start(self) -> None:
        for one in range(100 + 1):
            for two in range(100 + 1):
                x = one * self.a.x + two * self.b.x
                y = one * self.a.y + two * self.b.y
                if (x == self.prize.x) and (y == self.prize.y):
                    self.solutions.append(Press(a=one, b=two))
                #
                if (x > self.prize.x) or (y > self.prize.y):
                    break
                #
            #
        #

    def tokens(self) -> int:
        length = len(self.solutions)
        if length == 0:
            return 0
        elif length == 1:
            elem = self.solutions[0]
            return 3 * elem.a + elem.b
        else:
            assert False, "too many solutions"

    def show(self):
        # print(self.a)
        # print(self.b)
        # print(self.prize)
        print(len(self.solutions), self.solutions)


# ----------------------------------------------------------------------------


def main() -> None:
    # content: str = helper.read("example.txt")
    content: str = helper.read("input.txt")

    result = 0
    machines = content.split("\n\n")
    for part in machines:
        m = Machine(part)
        m.start()
        # m.show()
        result += m.tokens()
        # print("---")
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
