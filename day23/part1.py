#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint

import helper

# ----------------------------------------------------------------------------


class Party:
    def __init__(self, fname: str) -> None:
        self.d: dict[str, set[str]] = self.parse_input(fname)

    def parse_input(self, fname: str) -> dict[str, set[str]]:
        d: dict[str, set[str]] = defaultdict(set)
        #
        lines: list[str] = helper.read_lines(fname)
        for line in lines:
            left, right = line.split("-")
            d[left].add(right)
            d[right].add(left)
        #
        return dict(d)

    def whats_connected_to(self, c1: str, c2: str) -> list[str]:
        result: list[str] = []
        #
        for c3, others in self.d.items():
            if c3 != c1 and c3 != c2:
                if c1 in others and c2 in others:
                    result.append(c3)
                #
            #
        #
        return result

    def start(self) -> None:
        result: set[tuple[str, str, str]] = set()

        for c1, li in self.d.items():
            for c2 in li:
                links: list[str] = self.whats_connected_to(c1, c2)
                for c3 in links:
                    triplet: tuple[str, str, str] = tuple(sorted([c1, c2, c3]))  # type: ignore
                    a, b, c = triplet
                    if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                        result.add(triplet)
                    #
                #
            #
        #
        print(len(result))

    def show(self) -> None:
        pprint(self.d)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"  # 7
    fname = "input.txt"

    p = Party(fname)
    # p.show()

    p.start()


##############################################################################

if __name__ == "__main__":
    main()
