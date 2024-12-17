#!/usr/bin/env python3

import sys

import helper

# ----------------------------------------------------------------------------


class Computer:
    def __init__(self, fname: str) -> None:
        self.regA: int
        self.regB: int
        self.regC: int
        self.ip: int
        self.program: list[int]
        #
        self.read_input(fname)

    def read_input(self, fname: str) -> None:
        lines: list[str] = helper.read_lines(fname)
        self.regA = int(lines[0].split(":")[1])
        self.regB = int(lines[1].split(":")[1])
        self.regC = int(lines[2].split(":")[1])
        self.program = [int(n) for n in lines[4].split(":")[1].split(",")]

    def combo(self, value: int) -> int:
        if value < 4:
            return value
        elif value == 4:
            return self.regA
        elif value == 5:
            return self.regB
        elif value == 6:
            return self.regC
        else:
            assert False, "invalid operator"

    def start(self) -> None:
        self.ip = 0
        first = True
        while True:
            try:
                opcode = self.program[self.ip]
                self.ip += 1
                operator = self.program[self.ip]
                self.ip += 1
            except IndexError:
                break

            if opcode == 0:
                self.regA = self.regA // (2 ** self.combo(operator))
            elif opcode == 1:
                self.regB = self.regB ^ operator
            elif opcode == 2:
                self.regB = self.combo(operator) % 8
            elif opcode == 3:
                if self.regA != 0:
                    self.ip = operator
                #
            elif opcode == 4:
                self.regB = self.regB ^ self.regC
            elif opcode == 5:
                if not first:
                    sys.stdout.write(",")
                #
                print(self.combo(operator) % 8, end="")
                first = False
            elif opcode == 6:
                self.regB = self.regA // (2 ** self.combo(operator))
            elif opcode == 7:
                self.regC = self.regA // (2 ** self.combo(operator))
            else:
                assert False, "invalid opcode"
            #
        #
        print()

    def show(self) -> None:
        print(f"Reg. A: {self.regA}")
        print(f"Reg. B: {self.regB}")
        print(f"Reg. C: {self.regC}")
        print()
        print("Program:", ",".join([str(n) for n in self.program]))


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"  # 4,6,3,5,6,3,5,2,1,0
    fname = "input.txt"

    c = Computer(fname)
    # c.show()

    c.start()


##############################################################################

if __name__ == "__main__":
    main()
