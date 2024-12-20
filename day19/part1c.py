#!/usr/bin/env python3

"""
Fast version.

memoization is done with lru_cache
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache

import helper


@dataclass
class Node:
    word: str
    parent: Node | None


# ----------------------------------------------------------------------------


class Towel:
    def __init__(self, fname: str) -> None:
        self.patterns: list[str]
        self.words: list[str]
        self.read_input(fname)
        #
        self.nodes: dict[str, Node] = {}
        self.tree: dict[str, list[Node]]

    def read_input(self, fname: str):
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.patterns = part1.replace(" ", "").split(",")
        self.words = part2.split()

    @lru_cache
    def extend(self, word: str) -> bool:
        if len(word) == 0:
            return True
        # else:
        parent = self.nodes[word]
        prefixes: list[str] = [p for p in self.patterns if word.startswith(p)]
        if len(prefixes) == 0:
            return False
        # else:
        substrings: list[str] = [word.removeprefix(pre) for pre in prefixes]
        for ss in substrings:
            node = Node(ss, parent)
            self.nodes[ss] = node
            self.tree[word].append(node)
            if self.extend(ss):
                return True
            #
        #
        return False

    def is_valid(self, word: str) -> bool:
        self.tree = defaultdict(list)  # reset
        self.nodes[word] = Node(word, None)
        status = self.extend(word)
        return status

    def start(self) -> int:
        counter = 0
        #
        for word in self.words:
            print("#", word)
            if self.is_valid(word):
                counter += 1
            #
        #
        return counter


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"  # possible: 6
    fname = "input.txt"

    t = Towel(fname)
    result = t.start()
    print("---")
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
