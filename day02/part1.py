#!/usr/bin/env python3

import helper


def valid(numbers: list[int]) -> bool:
    for i in range(len(numbers) - 1):
        diff = abs(numbers[i] - numbers[i + 1])
        if (diff < 1) or (diff > 3):
            return False
        #
    #
    return True


def main() -> None:
    # lines: list[str] = helper.read_lines("example.txt")
    lines: list[str] = helper.read_lines("input.txt")

    cnt = 0
    for line in lines:
        numbers = [int(n) for n in line.split()]
        if (numbers == sorted(numbers)) or (numbers == sorted(numbers, reverse=True)):
            if valid(numbers):
                cnt += 1
            #
        #
    #
    print(cnt)


##############################################################################

if __name__ == "__main__":
    main()
