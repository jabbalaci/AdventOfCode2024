#!/usr/bin/env python3

from itertools import product

import helper


def solve_v1(numbers: list[int], total: int) -> bool:
    length = len(numbers) - 1
    all_signs = product("+*", repeat=length)
    for sign_line in all_signs:
        result = numbers[0]
        for i in range(len(sign_line)):
            sign = sign_line[i]
            if sign == "+":
                result += numbers[i + 1]
            else:  # *
                result *= numbers[i + 1]
            #
        #
        if result == total:
            return True
        #
    #
    return False


def solve_v2(numbers: list[int], total: int) -> bool:
    length = len(numbers) - 1
    all_signs = product("+*|", repeat=length)
    for sign_line in all_signs:
        result = numbers[0]
        for i in range(len(sign_line)):
            sign = sign_line[i]
            if sign == "+":
                result += numbers[i + 1]
            elif sign == "*":
                result *= numbers[i + 1]
            else:  # | (which is || in the exercise)
                result = int(str(result) + str(numbers[i + 1]))
            #
        #
        if result == total:
            return True
        #
    #
    return False


def main() -> None:
    # lines: list[str] = helper.read_lines("example.txt")
    lines: list[str] = helper.read_lines("input.txt")

    result = 0
    for line in lines:
        parts = line.split(":")
        total = int(parts[0])
        numbers = [int(n) for n in parts[1].split()]
        status = solve_v1(numbers, total)
        if status:
            result += total
        else:
            status = solve_v2(numbers, total)
            if status:
                result += total
            #
        #
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
