#!/usr/bin/env python3

from itertools import combinations
from pprint import pprint

import helper


class Validator:
    def __init__(self, content: str) -> None:
        self.first, self.second = content.split("\n\n")
        self.rules: dict[int, list[int]] = self.get_rules(self.first)
        # pprint(self.rules)

    def has_rule(self, a: int, b: int) -> bool:
        return (a in self.rules) and (b in self.rules[a])

    def get_rules(self, first: str) -> dict[int, list[int]]:
        d: dict[int, list[int]] = {}
        for line in first.splitlines():
            a_str, b_str = line.split("|")
            a = int(a_str)
            b = int(b_str)
            if a not in d:
                d[a] = [b]
            else:
                d[a].append(b)
            #
        #
        return d

    def is_valid(self, pages: list[int]) -> bool:
        for a, b in combinations(pages, 2):
            if not self.has_rule(a, b):
                return False
            #
        #
        return True

    def start(self) -> int:
        # print("---")
        result = 0
        for line in self.second.splitlines():
            pages = [int(p) for p in line.split(",")]
            if self.is_valid(pages):
                result += pages[len(pages) // 2]
            #
        #
        return result


def main() -> None:
    # content: str = helper.read("example.txt")
    content: str = helper.read("input.txt")

    v = Validator(content)
    result = v.start()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
