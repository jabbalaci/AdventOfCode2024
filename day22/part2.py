#!/usr/bin/env python3

"""
Very slow but it gives the correct answer.
"""

from collections import deque
from pprint import pprint

import helper

# ITERATION = 10  # example
ITERATION = 2000  # real thing


def my_search(li: list[int], sublist: list[int]) -> int:
    assert len(sublist) == 4, "sublist must be 4-long"
    #
    for i in range(len(li) - 3):
        if (
            li[i] == sublist[0]
            and li[i + 1] == sublist[1]
            and li[i + 2] == sublist[2]
            and li[i + 3] == sublist[3]
        ):
            return i
        #
    #
    return -1


# ----------------------------------------------------------------------------


class Solution:
    def __init__(self, d: dict[int, dict]) -> None:
        # keys of subdicts: "prices", "changes"
        self.d: dict[int, dict] = d
        self.keys: deque[int] = deque(self.d.keys())
        self.maxi: int = -1

    def start(self) -> None:
        for outer in range(len(self.keys)):
            print("# outer:", outer)
            self.keys.rotate(-1)
            first_key: int = self.keys[0]
            other_keys: list[int] = list(self.keys)[1:]
            #
            changes: list[int] = self.d[first_key]["changes"]
            for i in range(len(changes) - 3):
                sublist: list[int] = changes[i : i + 4]
                total = self.d[first_key]["prices"][i + 3]
                for other_key in other_keys:
                    other_changes: list[int] = self.d[other_key]["changes"]
                    idx = my_search(other_changes, sublist)
                    if idx != -1:
                        total += self.d[other_key]["prices"][idx + 3]
                    #
                #
                if total > self.maxi:
                    self.maxi = total
                #
            #
            print("---")
            print(self.maxi)
        #
        print("=========")
        print(self.maxi)


# ----------------------------------------------------------------------------


class PseudoRNG:
    def __init__(self, secret: int) -> None:
        self.secret: int = secret

    def next_number(self) -> int:
        secret = self.secret
        res = secret * 64
        secret ^= res
        secret %= 16777216
        #
        res = secret // 32
        secret ^= res
        secret %= 16777216
        #
        res = secret * 2048
        secret ^= res
        secret %= 16777216
        #
        self.secret = secret
        return secret


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example2.txt"
    fname = "input.txt"

    numbers: list[int] = helper.read_lines_as_ints(fname)

    d: dict[int, dict] = {}

    for n in numbers:
        prices: list[int] = []
        changes: list[int] = []
        p = PseudoRNG(n)
        prev_price = n % 10
        #
        for _ in range(ITERATION):
            v = p.next_number()
            price = v % 10
            prices.append(price)
            changes.append(price - prev_price)
            prev_price = price
        #
        d[n] = {
            "prices": prices,
            "changes": changes,
        }
    #

    # pprint(d)

    sol = Solution(d)
    sol.start()


##############################################################################

if __name__ == "__main__":
    main()
