#!/usr/bin/env python3

import re

import helper


def main() -> None:
    # content: str = helper.read("example.txt")
    content: str = helper.read("input.txt")

    muls = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", content)

    result = 0
    for a, b in muls:
        result += int(a) * int(b)
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
