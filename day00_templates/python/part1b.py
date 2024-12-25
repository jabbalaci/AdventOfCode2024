#!/usr/bin/env python3

import helper

# ----------------------------------------------------------------------------


class Solver:
    def __init__(self, fname: str) -> None:
        self.read_input(fname)

    def read_input(self, fname: str) -> None:
        lines: list[str] = helper.read_lines(fname)
        #
        for line in lines:
            print(line)


# ----------------------------------------------------------------------------


def main() -> None:
    fname = "example.txt"
    # fname = "input.txt"

    sol = Solver(fname)


##############################################################################

if __name__ == "__main__":
    main()
