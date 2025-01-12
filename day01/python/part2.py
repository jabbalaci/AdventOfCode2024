#!/usr/bin/env python3

"""
3   4
4   3
2   5
1   3
3   9
3   3

d:
    4: 1
    3: 3
    5: 1
    9: 1

"""

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

    result = 0
    for n in first:
        result += n * second.count(n)
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
