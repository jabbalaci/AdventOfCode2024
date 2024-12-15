#!/usr/bin/env python3

import sys

import helper

char = str

GridType = list[list[char]]


# ----------------------------------------------------------------------------


class Box:
    def __init__(self, parent: "Area", row: int, col: int, is_robot: bool) -> None:
        self.parent: Area = parent
        self.row: int = row
        self.col: int = col
        self.is_robot: bool = is_robot

    def move_left(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        nb: char = self.parent.get_cell_value(row=self.row, col=self.col - 1)
        if nb == ".":
            self.col -= 1
            return True
        elif nb == "]":
            box: Box = self.parent.get_box_at(row=self.row, col=self.col - 2)
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
        nb: char
        if self.is_robot:
            nb = self.parent.get_cell_value(row=self.row, col=self.col + 1)
        else:
            nb = self.parent.get_cell_value(row=self.row, col=self.col + 2)
        #
        if nb == ".":
            self.col += 1
            return True
        elif nb == "[":
            box: Box
            if self.is_robot:
                box = self.parent.get_box_at(row=self.row, col=self.col + 1)
            else:
                box = self.parent.get_box_at(row=self.row, col=self.col + 2)
            #
            if box.move_right():
                self.col += 1
                return True
            else:
                return False
            #
        else:
            return False

    def can_move_up(self) -> bool:
        """This is a real box, not a robot."""
        nb: char = self.parent.get_cell_value(row=self.row - 1, col=self.col)
        nb_plus1: char = self.parent.get_cell_value(row=self.row - 1, col=self.col + 1)
        top = nb + nb_plus1

        if top == "..":
            return True
        elif "#" in top:
            return False
        elif top == "[]":
            top_box = self.parent.get_box_at(row=self.row - 1, col=self.col)
            return top_box.can_move_up()
        elif top == "][":
            box1 = self.parent.get_box_at(row=self.row - 1, col=self.col - 1)
            box2 = self.parent.get_box_at(row=self.row - 1, col=self.col + 1)
            return box1.can_move_up() and box2.can_move_up()
        elif top == ".[":
            box = self.parent.get_box_at(row=self.row - 1, col=self.col + 1)
            return box.can_move_up()
        elif top == "].":
            box = self.parent.get_box_at(row=self.row - 1, col=self.col - 1)
            return box.can_move_up()
        else:
            assert False, "we shouldn't get here"

    def move_up(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        top_nb: char = self.parent.get_cell_value(row=self.row - 1, col=self.col)

        if self.is_robot:
            if top_nb == ".":
                self.row -= 1
                return True
            elif (top_nb == "[") or (top_nb == "]"):
                box: Box
                if top_nb == "[":
                    box = self.parent.get_box_at(row=self.row - 1, col=self.col)
                else:  # ']'
                    box = self.parent.get_box_at(row=self.row - 1, col=self.col - 1)
                #
                if box.can_move_up():
                    box.move_up()
                    self.row -= 1
                    return True
                else:
                    return False
                #
            else:
                return False
            #
        else:  # if it's a real box that we need to move (not a robot)
            if self.can_move_up():
                top_nb_plus1: char = self.parent.get_cell_value(row=self.row - 1, col=self.col + 1)
                top = top_nb + top_nb_plus1
                if top == "[]":
                    top_box = self.parent.get_box_at(row=self.row - 1, col=self.col)
                    top_box.move_up()
                elif top == "][":
                    box1 = self.parent.get_box_at(row=self.row - 1, col=self.col - 1)
                    box2 = self.parent.get_box_at(row=self.row - 1, col=self.col + 1)
                    box1.move_up()
                    box2.move_up()
                elif top == ".[":
                    box = self.parent.get_box_at(row=self.row - 1, col=self.col + 1)
                    box.move_up()
                elif top == "].":
                    box = self.parent.get_box_at(row=self.row - 1, col=self.col - 1)
                    box.move_up()
                #
                self.row -= 1
                return True
            else:
                return False
            #
        #
        assert False, "we shouldn't get here"

    def can_move_down(self) -> bool:
        """This is a real box, not a robot."""
        bottom_nb: char = self.parent.get_cell_value(row=self.row + 1, col=self.col)
        bottom_nb_plus1: char = self.parent.get_cell_value(row=self.row + 1, col=self.col + 1)
        bottom = bottom_nb + bottom_nb_plus1

        if bottom == "..":
            return True
        elif "#" in bottom:
            return False
        elif bottom == "[]":
            box = self.parent.get_box_at(row=self.row + 1, col=self.col)
            return box.can_move_down()
        elif bottom == "][":
            box1 = self.parent.get_box_at(row=self.row + 1, col=self.col - 1)
            box2 = self.parent.get_box_at(row=self.row + 1, col=self.col + 1)
            return box1.can_move_down() and box2.can_move_down()
        elif bottom == ".[":
            box = self.parent.get_box_at(row=self.row + 1, col=self.col + 1)
            return box.can_move_down()
        elif bottom == "].":
            box = self.parent.get_box_at(row=self.row + 1, col=self.col - 1)
            return box.can_move_down()
        else:
            assert False, "we shouldn't get here"

    def move_down(self) -> bool:
        """Returns True if the box moved, False otherwise."""
        bottom_nb: char = self.parent.get_cell_value(row=self.row + 1, col=self.col)

        if self.is_robot:
            if bottom_nb == ".":
                self.row += 1
                return True
            elif (bottom_nb == "[") or (bottom_nb == "]"):
                box: Box
                if bottom_nb == "[":
                    box = self.parent.get_box_at(row=self.row + 1, col=self.col)
                else:  # ']'
                    box = self.parent.get_box_at(row=self.row + 1, col=self.col - 1)
                #
                if box.can_move_down():
                    box.move_down()
                    self.row += 1
                    return True
                else:
                    return False
                #
            else:
                return False
            #
        else:  # if it's a real box that we need to move (not a robot)
            if self.can_move_down():
                bottom_nb_plus1: char = self.parent.get_cell_value(
                    row=self.row + 1, col=self.col + 1
                )
                bottom = bottom_nb + bottom_nb_plus1
                if bottom == "[]":
                    box = self.parent.get_box_at(row=self.row + 1, col=self.col)
                    box.move_down()
                elif bottom == "][":
                    box1 = self.parent.get_box_at(row=self.row + 1, col=self.col - 1)
                    box2 = self.parent.get_box_at(row=self.row + 1, col=self.col + 1)
                    box1.move_down()
                    box2.move_down()
                elif bottom == ".[":
                    box = self.parent.get_box_at(row=self.row + 1, col=self.col + 1)
                    box.move_down()
                elif bottom == "].":
                    box = self.parent.get_box_at(row=self.row + 1, col=self.col - 1)
                    box.move_down()
                #
                self.row += 1
                return True
            else:
                return False
            #
        #
        assert False, "we shouldn't get here"

    def move(self, where: char) -> None:
        """We're moving the robot here."""
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

    def expand_matrix(self, old_matrix: GridType) -> GridType:
        new_matrix: GridType = []
        #
        for i, row in enumerate(old_matrix):
            new_row: list[char] = []
            for j, c in enumerate(row):
                if c == "#":
                    new_row.append("#")
                    new_row.append("#")
                elif c == "O":
                    new_row.append("[")
                    new_row.append("]")
                elif c == ".":
                    new_row.append(".")
                    new_row.append(".")
                elif c == "@":
                    new_row.append("@")
                    new_row.append(".")
                else:
                    assert False, "invalid character"
                #
            #
            new_matrix.append(new_row)
        #
        return new_matrix

    def read_input_file(self, fname: str) -> None:
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.steps = part2.replace("\n", "")
        old_matrix: GridType = [list(line) for line in part1.splitlines()]
        #
        self.matrix = self.expand_matrix(old_matrix)
        #
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == "[":
                    self.matrix[i][j] = "."
                    self.matrix[i][j + 1] = "."
                    self.boxes.append(Box(self, row=i, col=j, is_robot=False))
                elif c == "@":
                    self.matrix[i][j] = "."
                    self.robot = Box(self, row=i, col=j, is_robot=True)
                #
            #
        #

    def get_cell_value(self, row: int, col: int, default="#") -> char:
        i, j = row, col
        if (i < 0) or (j < 0):
            return default  # type: ignore
        try:
            if c := self.is_box(row=i, col=j):
                return c
            elif self.is_robot(row=i, col=j):
                return "@"
            else:
                return self.matrix[i][j]
        except IndexError:
            return default  # type: ignore

    def is_box(self, row: int, col: int) -> char:
        """
        Return values:
        "["         -> it's a box, return the left part
        "]"         -> it's a box, return the right part
        ""          -> it's NOT a box, return the empty string
        """
        for box in self.boxes:
            if box.row == row:
                if box.col == col:
                    return "["
                if box.col + 1 == col:
                    return "]"
            #
        #
        return ""

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
        for i, c in enumerate(self.steps):
            next_step: char
            try:
                next_step = self.steps[i + 1]
            except IndexError:
                next_step = "-"
            #
            self.robot.move(c)
            # self.show(f"Move {c}:", next_step)
            # print()
            # input("Press ENTER...")
        #

    def get_result(self) -> int:
        result = 0
        for box in self.boxes:
            result += 100 * box.row + box.col
        #
        return result

    def show(self, caption: str, next_step: char = "?") -> None:
        print(caption)
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                sys.stdout.write(self.get_cell_value(i, j))
            #
            print()
        #
        print(f"Next move: {next_step}")


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"  # sum: 9021
    # fname = "example2.txt"  # sum: ?
    # fname = "example3.txt"  # sum: ?

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
