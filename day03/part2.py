#!/usr/bin/env python3

import re

import helper


def main() -> None:
    # content: str = helper.read("example2.txt")
    content: str = helper.read("input.txt")

    instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)", content)

    result = 0
    process = True
    for inst in instructions:
        if inst.startswith("mul"):
            if process:
                numbers = re.findall(r"\d+", inst)
                result += int(numbers[0]) * int(numbers[1])
            #
        #
        if inst == "don't()":
            process = False
        if inst == "do()":
            process = True
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
