#!/usr/bin/env python3

import sys

import helper

char = str

GridType = list[list[char]]


# ----------------------------------------------------------------------------


class Box:
    def __init__(self, parent: "Area", row: int, col: int) -> None:
        self.parent = parent
        self.row = row
        self.col = col

    def move_left(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        nb: char = self.parent.get_cell_value(row=self.row, col=self.col - 1)
        if nb == ".":
            self.col -= 1
            return True
        elif nb == "O":
            box: Box = self.parent.get_box_at(row=self.row, col=self.col - 1)
            if box.move_left():
                self.col -= 1
                return True
            else:
                return False
            #
        else:
            return False

    def move_right(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        nb: char = self.parent.get_cell_value(row=self.row, col=self.col + 1)
        if nb == ".":
            self.col += 1
            return True
        elif nb == "O":
            box: Box = self.parent.get_box_at(row=self.row, col=self.col + 1)
            if box.move_right():
                self.col += 1
                return True
            else:
                return False
            #
        else:
            return False

    def move_up(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        nb: char = self.parent.get_cell_value(row=self.row - 1, col=self.col)
        if nb == ".":
            self.row -= 1
            return True
        elif nb == "O":
            box: Box = self.parent.get_box_at(row=self.row - 1, col=self.col)
            if box.move_up():
                self.row -= 1
                return True
            else:
                return False
            #
        else:
            return False

    def move_down(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        nb: char = self.parent.get_cell_value(row=self.row + 1, col=self.col)
        if nb == ".":
            self.row += 1
            return True
        elif nb == "O":
            box: Box = self.parent.get_box_at(row=self.row + 1, col=self.col)
            if box.move_down():
                self.row += 1
                return True
            else:
                return False
            #
        else:
            return False

    def move(self, where: char) -> None:
        if where == "<":
            self.move_left()
        elif where == ">":
            self.move_right()
        elif where == "^":
            self.move_up()
        elif where == "v":
            self.move_down()
        else:
            assert False, "cannot get here"


# ----------------------------------------------------------------------------


class Area:
    def __init__(self, fname: str) -> None:
        self.boxes: list[Box] = []
        self.robot: Box
        self.steps: str
        self.matrix: GridType
        self.read_input_file(fname)

    def read_input_file(self, fname: str) -> None:
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.steps = part2.replace("\n", "")
        self.matrix = [list(line) for line in part1.splitlines()]
        #
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == "O":
                    self.matrix[i][j] = "."
                    self.boxes.append(Box(self, row=i, col=j))
                elif c == "@":
                    self.matrix[i][j] = "."
                    self.robot = Box(self, row=i, col=j)
                #
            #
        #

    def get_cell_value(self, row: int, col: int, default="#") -> char:
        i, j = row, col
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            if self.is_box(row=i, col=j):
                return "O"
            elif self.is_robot(row=i, col=j):
                return "@"
            else:
                return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def is_box(self, row: int, col: int) -> bool:
        for box in self.boxes:
            if (box.row == row) and (box.col == col):
                return True
            #
        #
        return False

    def get_box_at(self, row: int, col: int) -> Box:
        for box in self.boxes:
            if (box.row == row) and (box.col == col):
                return box
            #
        #
        assert False, "we shouldn't get here"

    def is_robot(self, row: int, col: int) -> bool:
        return (self.robot.row == row) and (self.robot.col == col)

    def start(self) -> None:
        for c in self.steps:
            self.robot.move(c)
            # self.show(f"Move {c}:")
            # print()
            # input("Press ENTER...")
        #

    def get_result(self) -> int:
        result = 0
        for box in self.boxes:
            result += 100 * box.row + box.col
        #
        return result

    def show(self, caption: str) -> None:
        print(caption)
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                sys.stdout.write(self.get_cell_value(i, j))
            #
            print()
        #


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"  # sum: 10092
    # fname = "example2.txt"  # sum: 2028
    fname = "input.txt"

    area = Area(fname)
    # area.show("Initial state:")
    # print()

    area.start()

    result = area.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
