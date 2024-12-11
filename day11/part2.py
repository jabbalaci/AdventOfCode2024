#!/usr/bin/env python3

"""
Runtime: 0.182 sec

I also tried to add lru_cache, but it became slower :)
Runtime with lru_cache: 0.206 sec
"""

from collections import defaultdict
from pprint import pprint

import helper

# ----------------------------------------------------------------------------


class Pluto:
    def __init__(self, line: str) -> None:
        stones = [int(n) for n in line.split()]
        self.d: dict[int, int] = defaultdict(int)
        for k in stones:
            self.d[k] += 1

    def mutate(self, n: int) -> list[int]:
        result: list[int] = []

        if n == 0:
            result.append(1)
        else:
            s = str(n)
            if len(s) % 2 == 0:
                half = len(s) // 2
                result.append(int(s[:half]))
                result.append(int(s[half:]))
            else:
                result.append(n * 2024)
            #
        #
        return result

    def start(self, iteration: int) -> None:
        # self.show()
        for _ in range(iteration):
            d2: dict[int, int] = self.d.copy()
            for k in self.d.keys():
                v = self.d[k]
                new: list[int] = self.mutate(k)
                for n in new:
                    d2[n] += v
                #
                d2[k] -= v
                # cleaning up:
                if d2[k] == 0:
                    del d2[k]
                #
            #
            self.d = d2
            # self.show()
        #

    def get_result(self):
        return sum(self.d.values())

    def show(self):
        pprint(dict(self.d))


# ----------------------------------------------------------------------------


def main() -> None:
    # line: str = helper.read("example1.txt", trim=True)  # after 1 blink: 1 2024 1 0 9 9 2021976
    # line: str = helper.read("example2.txt", trim=True)
    line: str = helper.read("input.txt", trim=True)

    p = Pluto(line)

    p.start(iteration=75)

    result = p.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
