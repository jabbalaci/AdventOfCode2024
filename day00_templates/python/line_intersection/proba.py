#!/usr/bin/env python3

from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


class Line(NamedTuple):
    a: Point
    b: Point


# from https://stackoverflow.com/questions/20677795
def line_intersection(line1: Line, line2: Line) -> Point:
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return Point(x, y)


def main() -> None:
    a = Point(x=19, y=13)
    b = Point(x=17, y=14)
    line1 = Line(a, b)
    c = Point(x=20, y=25)
    d = Point(x=18, y=23)
    line2 = Line(c, d)
    print(line_intersection(line1, line2))


##############################################################################

if __name__ == "__main__":
    main()
