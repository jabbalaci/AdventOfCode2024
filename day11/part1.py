#!/usr/bin/env python3

import helper

# ----------------------------------------------------------------------------


class Pluto:
    def __init__(self, line: str) -> None:
        self.stones = [int(n) for n in line.split()]

    def start(self, iteration: int) -> None:
        for _ in range(iteration):
            new: list[int] = []
            for n in self.stones:
                if n == 0:
                    new.append(1)
                else:
                    s = str(n)
                    if len(s) % 2 == 0:
                        half = len(s) // 2
                        new.append(int(s[:half]))
                        new.append(int(s[half:]))
                    else:
                        new.append(n * 2024)
                    #
                #
            #
            self.stones = new
        #

    def get_result(self):
        return len(self.stones)

    def show(self):
        print(self.stones)


# ----------------------------------------------------------------------------


def main() -> None:
    # line: str = helper.read("example1.txt", trim=True)  # after 1 blink: 1 2024 1 0 9 9 2021976
    # line: str = helper.read("example2.txt", trim=True)
    line: str = helper.read("input.txt", trim=True)

    p = Pluto(line)

    p.start(iteration=25)

    result = p.get_result()
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
