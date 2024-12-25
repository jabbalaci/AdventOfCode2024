#!/usr/bin/env python3

Point = tuple[int, int]


# from https://web.archive.org/web/20100405070507/http://valis.cs.uiuc.edu/~sariel/research/CG/compgeom/msg00831.html
def my_area(vertices: list[Point]) -> float:
    N = len(vertices)
    area = 0.0
    for i in range(N - 1):
        j = (i + 1) % N
        area = area + vertices[i][0] * vertices[j][1]
        area = area - vertices[i][1] * vertices[j][0]
    #
    return abs(area) / 2


def get_perimeter(points: list[Point]) -> int:
    """
    It also compares the first point (idx: 0) with the last point (idx: -1).

    So the perimeter is calculated correctly even if the first point
    is not repeated in the last position.
    """
    total = 0
    for i in range(len(points)):
        curr = points[i]
        prev = points[i - 1]
        value = abs(curr[0] - prev[0]) + abs(curr[1] - prev[1])
        total += value
    #
    return total


def main():
    # (row, column)
    points: list[Point] = [
        (0, 0),
        (0, 6),  # 6
        (5, 6),  # 5
        (5, 4),  # 2
        (7, 4),  # 2
        (7, 6),  # 2
        (9, 6),  # 2
        (9, 1),  # 5
        (7, 1),  # 2
        (7, 0),  # 1
        (5, 0),  # 2
        (5, 2),  # 2
        (2, 2),  # 3
        (2, 0),  # 2
    ]
    # points = [(0, 0), (0, 5), (5, 5), (5, 0)]
    #
    area: float = my_area(points)
    print(f"{area=}")
    perimeter: int = get_perimeter(points)
    print(f"{perimeter=}")
    result: int = int(area) + (perimeter // 2) + 1
    print("---")
    print(f"{result=}")


##############################################################################

if __name__ == "__main__":
    main()
