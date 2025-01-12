#!/usr/bin/env python3

import helper


def main() -> None:
    # lines: list[str] = helper.read_lines("example.txt")
    lines: list[str] = helper.read_lines("input.txt")

    first: list[int] = []
    second: list[int] = []

    for line in lines:
        parts = line.split()
        first.append(int(parts[0]))
        second.append(int(parts[1]))
    #

    first.sort()
    second.sort()

    result = 0
    for a, b in zip(first, second):
        result += abs(a - b)
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
