#!/usr/bin/env python3

"""
Optimized solution.
"""

from typing import NamedTuple

import sympy as sp
from parse import parse

import helper


class Button(NamedTuple):
    x: int
    y: int


# each button was pressed how many times
class Press(NamedTuple):
    a: int
    b: int


ADDITION = 0

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
        prize = Button(x=p["x"] + ADDITION, y=p["y"] + ADDITION)
        #
        return (a, b, prize)

    def start(self) -> None:
        x = sp.symbols("x")
        y = sp.symbols("y")
        eq1 = sp.Eq(self.a.x * x + self.b.x * y, self.prize.x)
        eq2 = sp.Eq(self.a.y * x + self.b.y * y, self.prize.y)
        system = [eq1, eq2]
        sol_set = sp.linsolve(system, x, y)
        assert len(sol_set) == 1
        t = list(sol_set)[0]
        a, b = t
        if isinstance(a, sp.core.numbers.Integer) and isinstance(b, sp.core.numbers.Integer):
            self.solutions.append(Press(a=int(a), b=int(b)))
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
