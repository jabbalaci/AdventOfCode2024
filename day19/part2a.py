#!/usr/bin/env python3

"""
Very slow at the moment.

Works with the example.
"""

import helper

# ----------------------------------------------------------------------------


class Towel:
    def __init__(self, fname: str) -> None:
        self.patterns: list[str]
        self.words: list[str]
        self.read_input(fname)
        self.number_of_ways: int

    def read_input(self, fname: str):
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.patterns = part1.replace(" ", "").split(",")
        self.words = part2.split()

    def can_be_reduced_to_empty_string(self, word: str) -> bool:
        if len(word) == 0:
            self.number_of_ways += 1
            return True
        # else
        prefixes: list[str] = [p for p in self.patterns if word.startswith(p)]
        if len(prefixes) == 0:
            return False
        # else
        substrings: list[str] = [word[len(pre) :] for pre in prefixes]
        statuses: list[bool] = [self.can_be_reduced_to_empty_string(s) for s in substrings]
        return any(statuses)

    def possible(self, word: str) -> bool:
        self.number_of_ways = 0  # reset
        return self.can_be_reduced_to_empty_string(word)

    def start(self) -> int:
        total = 0
        #
        for word in self.words:
            print("#", word)
            if self.possible(word):
                total += self.number_of_ways
            #
        #
        return total


# ----------------------------------------------------------------------------


def main() -> None:
    fname = "example.txt"  # different ways: 16
    # fname = "input.txt"

    t = Towel(fname)
    result = t.start()
    print("---")
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
