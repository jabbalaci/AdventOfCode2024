#!/usr/bin/env python3

import helper


def has_negative(indexes: list[int]) -> bool:
    return any(True for i in indexes if i < 0)


def go_e(m: list[str], i: int, j: int) -> str:
    try:
        return m[i][j] + m[i][j + 1] + m[i][j + 2] + m[i][j + 3]
    except IndexError:
        return ""


def go_se(m: list[str], i: int, j: int) -> str:
    try:
        return m[i][j] + m[i + 1][j + 1] + m[i + 2][j + 2] + m[i + 3][j + 3]
    except IndexError:
        return ""


def go_s(m: list[str], i: int, j: int) -> str:
    try:
        return m[i][j] + m[i + 1][j] + m[i + 2][j] + m[i + 3][j]
    except IndexError:
        return ""


def go_sw(m: list[str], i: int, j: int) -> str:
    try:
        indexes = [j - 1, j - 2, j - 3]
        if has_negative(indexes):
            raise IndexError
        #
        return m[i][j] + m[i + 1][j - 1] + m[i + 2][j - 2] + m[i + 3][j - 3]
    except IndexError:
        return ""


def go_w(m: list[str], i: int, j: int) -> str:
    try:
        indexes = [j - 1, j - 2, j - 3]
        if has_negative(indexes):
            raise IndexError
        #
        return m[i][j] + m[i][j - 1] + m[i][j - 2] + m[i][j - 3]
    except IndexError:
        return ""


def go_nw(m: list[str], i: int, j: int) -> str:
    try:
        indexes = [i - 1, j - 1, i - 2, j - 2, i - 3, j - 3]
        if has_negative(indexes):
            raise IndexError
        #
        return m[i][j] + m[i - 1][j - 1] + m[i - 2][j - 2] + m[i - 3][j - 3]
    except IndexError:
        return ""


def go_n(m: list[str], i: int, j: int) -> str:
    try:
        indexes = [i - 1, i - 2, i - 3]
        if has_negative(indexes):
            raise IndexError
        #
        return m[i][j] + m[i - 1][j] + m[i - 2][j] + m[i - 3][j]
    except IndexError:
        return ""


def go_ne(m: list[str], i: int, j: int) -> str:
    try:
        indexes = [i - 1, i - 2, i - 3]
        if has_negative(indexes):
            raise IndexError
        #
        return m[i][j] + m[i - 1][j + 1] + m[i - 2][j + 2] + m[i - 3][j + 3]
    except IndexError:
        return ""


def extract_words(matrix: list[str], i: int, j: int) -> list[str]:
    result: list[str] = []

    result.append(go_e(matrix, i, j))
    result.append(go_se(matrix, i, j))
    result.append(go_s(matrix, i, j))
    result.append(go_sw(matrix, i, j))
    result.append(go_w(matrix, i, j))
    result.append(go_nw(matrix, i, j))
    result.append(go_n(matrix, i, j))
    result.append(go_ne(matrix, i, j))

    return result


def main() -> None:
    # matrix: list[str] = helper.read_lines("example.txt")
    matrix: list[str] = helper.read_lines("input.txt")

    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            words: list[str] = extract_words(matrix, i, j)
            result += sum([1 for w in words if w == "XMAS"])
        #
    #
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
