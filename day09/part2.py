#!/usr/bin/env python3

"""
Here I had to use some help.
Link: https://old.reddit.com/r/adventofcode/comments/1ha5we4/2024_day_9_part_2_good_for_the_example_wrong_for/
Thanks /r/adventofcode and /u/tyomka896 !
"""

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

    def get_first_fr_with_enough_free_space(self, required: int) -> tuple[int, Fragment]:
        for idx, fr in enumerate(self.layout):
            if fr.free >= required:
                return (idx, fr)
            #
        #
        return (-1, Fragment(-1, -1, -1))  # dummy value

    def find_by_id(self, _id: int) -> tuple[int, Fragment]:
        for idx, fr in enumerate(self.layout):
            if fr._id == _id:
                return (idx, fr)
            #
        #
        assert False, "we should never get here"

    def start(self) -> None:
        current_id = self.layout[-1]._id
        # fragment with ID 0 is the first one, it won't move
        cnt = 0
        while current_id > 0:
            if DEBUG:
                print("# current ID:", current_id)
            cnt += 1
            current_idx, current_fr = self.find_by_id(current_id)
            first_idx, first_fr = self.get_first_fr_with_enough_free_space(current_fr.used)
            #
            if (first_idx != -1) and (first_idx < current_idx):
                new = Fragment(
                    _id=current_fr._id, used=current_fr.used, free=first_fr.free - current_fr.used
                )
                first_fr.free = 0
                self.layout.insert(first_idx + 1, new)

                del self.layout[current_idx + 1]  # +1 because of the previous insertion

                before_fr = self.layout[
                    current_idx
                ]  # the fragment just before the previously deleted fragment
                before_fr.free += current_fr.used + current_fr.free
            #
            if DEBUG:
                self.debug()
                self.show_layout()
                print("---")
            #
            # if cnt == 3:
            # break
            #
            current_id -= 1
        #

    def checksum(self) -> int:
        result = 0
        idx = -1
        for fr in self.layout:
            for i in range(fr.used):
                idx += 1
                result += idx * fr._id
            #
            idx += fr.free
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
    # content: str = helper.read("example2.txt", trim=True)  # result: 2858
    # content: str = helper.read("example3.txt", trim=True)  # result: 169
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
