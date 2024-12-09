#!/usr/bin/env python3

import helper

# DEBUG = True
DEBUG = False

# ----------------------------------------------------------------------------


class Fragment:
    def __init__(self, _id: int, used: int, free: int) -> None:
        self._id = _id
        self.used = used
        self.free = free

    def __repr__(self) -> str:
        return f"(id:{self._id}, used:{self.used}, free:{self.free})"


# ----------------------------------------------------------------------------


class HardDrive:
    def __init__(self, content: str) -> None:
        self.layout: list[Fragment] = []
        for idx, gr in enumerate(helper.grouper(content, 2, fillvalue=0)):
            _id = idx
            used = int(gr[0])
            free = int(gr[1])
            self.layout.append(Fragment(_id, used, free))
        #

    def get_first_fr_with_free_space(self) -> tuple[int, Fragment]:
        for idx, fr in enumerate(self.layout):
            if fr.free > 0:
                return (idx, fr)
            #
        #
        assert False, "we should never get here"

    def start(self) -> None:
        cnt = 0
        while True:
            cnt += 1
            #
            last_idx = len(self.layout) - 1
            idx, first = self.get_first_fr_with_free_space()
            if idx == last_idx:
                break
            # else:
            last = self.layout[-1]
            new = Fragment(_id=last._id, used=1, free=first.free - 1)
            first.free = 0
            self.layout.insert(idx + 1, new)
            last.used -= 1
            last.free += 1
            if last.used == 0:
                before = self.layout[-2]
                before.free += last.free
                del self.layout[-1]
            #
            if DEBUG:
                self.debug()
                self.show_layout()
                print("---")
            #
            # if cnt == 5:
            # break
        #

    def checksum(self) -> int:
        result = 0
        idx = -1
        for fr in self.layout:
            for i in range(fr.used):
                idx += 1
                result += idx * fr._id
            #
        #
        return result

    def debug(self) -> None:
        print(self.layout)

    def show_layout(self) -> None:
        for fr in self.layout:
            print(str(fr._id) * fr.used, end="")
            print("." * fr.free, end="")
        #
        print()


# ----------------------------------------------------------------------------


def main() -> None:
    # content: str = helper.read("example1.txt", trim=True)
    # content: str = helper.read("example2.txt", trim=True)
    content: str = helper.read("input.txt", trim=True)

    hd = HardDrive(content)

    if DEBUG:
        hd.debug()
        hd.show_layout()
        print("---")

    hd.start()

    result = hd.checksum()
    print(result)

    # hd.debug()
    # hd.show_layout()


##############################################################################

if __name__ == "__main__":
    main()
