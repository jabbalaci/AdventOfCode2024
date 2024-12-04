#!/usr/bin/env python3

import helper


def diagonal(m: list[str], i: int, j: int) -> str:
    try:
        return m[i][j] + m[i + 1][j + 1] + m[i + 2][j + 2]
    except IndexError:
        return ""


def antidiagonal(m: list[str], i: int, j: int) -> str:
    try:
        return m[i][j + 2] + m[i + 1][j + 1] + m[i + 2][j]
    except IndexError:
        return ""


def xmas(matrix: list[str], i: int, j: int) -> bool:
    words: list[str] = []

    words.append(diagonal(matrix, i, j))
    words.append(antidiagonal(matrix, i, j))

    if (words[0] == "MAS") or (words[0] == "SAM"):
        if (words[1] == "MAS") or (words[1] == "SAM"):
            return True
        #
    #
    return False


def main() -> None:
    # matrix: list[str] = helper.read_lines("example2.txt")
    matrix: list[str] = helper.read_lines("input.txt")

    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if xmas(matrix, i, j):
                result += 1
            #
        #
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
