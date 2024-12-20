#!/usr/bin/env python3


from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import helper


@dataclass
class Node:
    word: str
    parent: Node | None
    counter: int


# ----------------------------------------------------------------------------


class Tree:
    def __init__(self, parent: Towel) -> None:
        self.parent = parent
        self.counter_cache: dict[str, int] = {}
        self.reset()

    def reset(self) -> None:
        self.nodes: dict[str, Node] = {}

    def update_counters_upwards(self, node: Node | None, by: int = 1) -> None:
        while node:
            node.counter += by
            self.counter_cache[node.word] = node.counter
            node = node.parent
        #

    def extend(self, word: str, parent_node: Node | None) -> None:
        if value := self.counter_cache.get(word):
            self.update_counters_upwards(parent_node, by=value)
            return
        # else:
        if len(word) == 0:
            self.update_counters_upwards(parent_node)
            return
        # else:
        current_node = self.nodes[word]
        prefixes: list[str] = [p for p in self.parent.patterns if word.startswith(p)]
        substrings: list[str] = [word.removeprefix(pre) for pre in prefixes]
        for ss in substrings:
            node = Node(word=ss, parent=current_node, counter=0)
            self.nodes[ss] = node
            self.extend(ss, parent_node=current_node)
        #

    def build(self, word: str) -> int:
        if value := self.counter_cache.get(word):
            return value
        # else:
        self.reset()
        #
        root = Node(word=word, parent=None, counter=0)
        self.nodes[word] = root
        self.extend(word, parent_node=None)
        return root.counter


# ----------------------------------------------------------------------------


class Towel:
    def __init__(self, fname: str) -> None:
        self.patterns: list[str]
        self.words: list[str]
        self.read_input(fname)
        #
        self.nodes: dict[str, Node] = {}

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
            node = Node(word=ss, parent=parent, counter=0)
            self.nodes[ss] = node
            if self.extend(ss):
                return True
            #
        #
        return False

    def is_valid(self, word: str) -> bool:
        self.nodes[word] = Node(word=word, parent=None, counter=0)
        status = self.extend(word)
        return status

    def start(self) -> int:
        total = 0
        #
        tree = Tree(self)
        for word in self.words:
            if self.is_valid(word):
                result = tree.build(word)
                print(f"{word}: {result}")
                total += result
            #
        #
        return total


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"  # 16
    fname = "input.txt"

    t = Towel(fname)
    result = t.start()
    print("---")
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
