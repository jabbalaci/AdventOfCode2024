#!/usr/bin/env python3

import helper

Entry = tuple[int, int, int, int, int]

LOCK, KEY = range(2)

# ----------------------------------------------------------------------------


class LockPick:
    def __init__(self, fname: str) -> None:
        self.locks: list[Entry] = []
        self.keys: list[Entry] = []
        self.read_input(fname)

    def read_input(self, fname: str) -> None:
        content: str = helper.read(fname)
        for entry in content.split("\n\n"):
            tup, kind = self.to_tuple(entry)
            if kind == LOCK:
                self.locks.append(tup)
            else:
                self.keys.append(tup)
            #
        #

    def to_tuple(self, entry: str) -> tuple[Entry, int]:
        kind = LOCK if entry[0] == "#" else KEY
        lines: list[str] = entry.splitlines()
        lines.pop(0)  # remove first line
        lines.pop()  # remove last line
        array = [0, 0, 0, 0, 0]
        for line in lines:
            for i, c in enumerate(line):
                if c == "#":
                    array[i] += 1
                #
            #
        #
        return (tuple(array), kind)  # type: ignore

    def fit(self, lock: Entry, key: Entry) -> bool:
        for a, b in zip(lock, key):
            if a + b > 5:
                return False
            #
        #
        return True

    def start(self) -> None:
        total = 0
        for lock in self.locks:
            for key in self.keys:
                if self.fit(lock, key):
                    total += 1
                #
            #
        #
        print(total)

    def show(self) -> None:
        for e in self.locks:
            print(e)
        print("---")
        for e in self.keys:
            print(e)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    lp = LockPick(fname)

    lp.start()

    # lp.show()


##############################################################################

if __name__ == "__main__":
    main()
