#!/usr/bin/env python3

from __future__ import annotations

from pprint import pprint

import helper

# ----------------------------------------------------------------------------


class Gate:
    def __init__(self, parent: System, kind: str, in1: str, in2: str, out: str) -> None:
        self.parent: System = parent
        self.kind: str = kind  # type of the fate: AND, OR, XOR
        self.in1: str = in1
        self.in2: str = in2
        self.out: str = out

    def is_ready(self) -> bool:
        return (self.in1 in self.parent.wires) and (self.in2 in self.parent.wires)

    def process(self) -> None:
        v1: int = self.parent.wires[self.in1]
        v2: int = self.parent.wires[self.in2]
        result: int

        if self.kind == "AND":
            result = 1 if v1 + v2 == 2 else 0
        elif self.kind == "OR":
            result = 1 if v1 + v2 > 0 else 0
        elif self.kind == "XOR":
            result = 1 if v1 != v2 else 0
        else:
            assert False, "we shouldn't get here"
        #
        self.parent.wires[self.out] = result

    def __str__(self) -> str:
        return f"{self.in1} {self.kind} {self.in2} -> {self.out}"


# ----------------------------------------------------------------------------


class System:
    def __init__(self, fname: str) -> None:
        self.wires: dict[str, int] = {}
        self.gates: list[Gate] = []
        self.read_input(fname)

    def read_input(self, fname: str) -> None:
        content: str = helper.read(fname)
        part1, part2 = content.split("\n\n")
        # process part1
        for line in part1.splitlines():
            l, r = line.split(": ")  # noqa
            self.wires[l] = int(r)
        # process part2
        for line in part2.splitlines():
            parts = line.split()
            g = Gate(parent=self, kind=parts[1], in1=parts[0], in2=parts[2], out=parts[-1])
            self.gates.append(g)

    def start(self) -> None:
        while len(self.gates) > 0:
            ready: list[Gate] = [g for g in self.gates if g.is_ready()]
            for g in ready:
                # print("# ready:", g)
                g.process()
                self.gates.remove(g)
            #
            # print("---")
        #

    def get_result(self) -> int:
        keys: list[str] = sorted([k for k in self.wires if k[0] == "z"], reverse=True)
        binary: str = "".join([str(self.wires[k]) for k in keys])
        return int(binary, 2)

    def show(self) -> None:
        pprint(self.wires)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"  # 4
    # fname = "example2.txt"  # 2024
    fname = "input.txt"

    system = System(fname)
    system.start()

    # system.show()

    result = system.get_result()
    # print("---")
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
