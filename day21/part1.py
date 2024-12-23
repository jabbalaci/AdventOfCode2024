#!/usr/bin/env python3

from enum import Enum, auto

import helper

char = str


class PanelType(Enum):
    BIGGER = auto()
    SMALLER = auto()


SPECIAL: dict[str, str] = {
    "70": ">vvv",
    "7A": ">>vvv",
    "40": ">vv",
    "4A": ">>vv",
    "10": ">v",
    "1A": ">>v",
    "01": "^<",
    "04": "^^<",
    "07": "^^^<",
    "A1": "^<<",
    "A4": "^^<<",
    "A7": "^^^<<",
    "^<": "v<",
    "A<": "v<<",
    "<^": ">^",
    "<A": ">>^",
}


BIGGER_LAYOUT: list[list[char]] = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]

SMALLER_LAYOUT: list[list[char]] = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]

# ----------------------------------------------------------------------------


class Panel:
    def __init__(self, panel_type: PanelType) -> None:
        self.panel_type = panel_type
        self.curr_row, self.curr_col = self.locate("A")

    def locate(self, what: char) -> tuple[int, int]:
        if self.panel_type == PanelType.BIGGER:
            matrix = BIGGER_LAYOUT
        else:
            matrix = SMALLER_LAYOUT
        #
        for i, row in enumerate(matrix):
            for j, c in enumerate(row):
                if c == what:
                    return (i, j)
                #
            #
        #
        assert False, "we shouldn't get here"

    def get_current_char(self) -> char:
        if self.panel_type == PanelType.BIGGER:
            matrix = BIGGER_LAYOUT
        else:
            matrix = SMALLER_LAYOUT
        #
        return matrix[self.curr_row][self.curr_col]


# ----------------------------------------------------------------------------


class Pressman:
    def __init__(self, original_code: str) -> None:
        self.original_code = original_code
        self.panels: list[Panel] = [
            Panel(PanelType.BIGGER),
            Panel(PanelType.SMALLER),
            Panel(PanelType.SMALLER),
            Panel(PanelType.SMALLER),
        ]

    def type(self, code: str, robot: Panel) -> str:
        """
        We have a code (e.g. 029A). Using the human panel, we want
        to instruct the robot panel to type in this code.
        """
        result = ""
        #
        for c in code:
            from_char = robot.get_current_char()
            to_char = c
            key = from_char + to_char
            to_row, to_col = robot.locate(c)
            #
            if dir := SPECIAL.get(key):
                result += dir
            else:
                diff_x, diff_y = robot.curr_col - to_col, robot.curr_row - to_row
                #
                # The order is important: v<^> (first down, then left, then up, then right)!
                if diff_y < 0:
                    result += "v" * abs(diff_y)
                if diff_x > 0:
                    result += "<" * diff_x
                if diff_y > 0:
                    result += "^" * diff_y
                if diff_x < 0:
                    result += ">" * abs(diff_x)
                #
            #
            result += "A"
            robot.curr_row, robot.curr_col = to_row, to_col
        #
        return result

    def start(self) -> str:
        # print(self.original_code)
        code = self.type(self.original_code, robot=self.panels[0])
        # print(code)
        code = self.type(code, robot=self.panels[1])
        # print(code)
        code = self.type(code, robot=self.panels[2])
        # print(code)
        return code


# ----------------------------------------------------------------------------


def clean(line: str) -> int:
    return int(line.replace("A", ""))


def main() -> None:
    # lines: list[str] = helper.read_lines("example1.txt")
    # lines: list[str] = helper.read_lines("example2.txt")
    lines: list[str] = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        p = Pressman(line)
        code = p.start()
        # print(f"{line}: {code}")
        value = clean(line) * len(code)
        # print(f"{clean(line)} * {len(code)} = {value}")
        # print(value)
        total += value
    #
    # print("---")
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
