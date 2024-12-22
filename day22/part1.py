#!/usr/bin/env python3

import helper

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
    # fname = "example.txt"
    fname = "input.txt"

    numbers: list[int] = helper.read_lines_as_ints(fname)

    total = 0
    for n in numbers:
        p = PseudoRNG(n)
        #
        for _ in range(2000):
            v = p.next_number()
        #
        total += v
        print(f"{n}: {v}")
    #
    print("---")
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
