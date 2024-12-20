#!/usr/bin/env python3

"""
This one is not perfect but works :)
If the word is valid, then the check is done quickly.
If the word in NOT valid, the check takes a lot of time.

My friend Mocsa gave me the idea to time out.
If we need to time out, then that word was invalid.
Not an elegant solution, I admit, but it worked here :)

TODO: find a solution without using timeout
"""

from stopit import ThreadingTimeout

import helper

TIMEOUT = 0.0001

# ----------------------------------------------------------------------------


class Towel:
    def __init__(self, fname: str) -> None:
        self.patterns: list[str]
        self.words: list[str]
        self.read_input(fname)

    def read_input(self, fname: str):
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        self.patterns = part1.replace(" ", "").split(",")
        self.words = part2.split()

    def can_be_reduced_to_empty_string(self, word: str) -> bool:
        if len(word) == 0:
            return True
        # else
        prefixes: list[str] = [p for p in self.patterns if word.startswith(p)]
        if len(prefixes) == 0:
            return False
        # else
        substrings: list[str] = [word[len(pre) :] for pre in prefixes]
        # statuses: list[bool] = [self.can_be_reduced_to_empty_string(s) for s in substrings]
        for s in substrings:
            if self.can_be_reduced_to_empty_string(s):
                return True
            #
        #
        return False

    def possible(self, word: str) -> bool:
        return self.can_be_reduced_to_empty_string(word)

    def start(self) -> int:
        counter = 0
        #
        for word in self.words:
            print("#", word)
            try:
                with ThreadingTimeout(TIMEOUT) as timeout_ctx:
                    if self.possible(word):
                        counter += 1
                    #
                #
            except:
                print("it was too slow", flush=True)
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
