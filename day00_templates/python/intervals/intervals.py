#!/usr/bin/env python3

# made for AoC 2023, Day 5, Part 2

template: dict = {"outside": [], "inside": []}


def match(rule: list[int], mine: list[int]) -> dict:
    result = template.copy()

    # result["mine"] = mine

    a, b = rule
    c, d = mine

    if (d < a) or (b < c):
        result["outside"] = [mine]
    elif (a <= c) and (d <= b):
        result["inside"] = [mine]
    elif c < a <= d <= b:
        result["outside"] = [[c, a - 1]]
        result["inside"] = [[a, d]]
    elif a <= c <= b < d:
        result["outside"] = [[b + 1, d]]
        result["inside"] = [[c, b]]
    elif c < a and b < d:
        result["outside"] = [[c, a - 1], [b + 1, d]]
        result["inside"] = [[a, b]]
    else:
        print("# rule:", [a, b])
        print("# mine:", [c, d])
        assert False, "We should never get here"

    return result


def main():
    rule = [35, 42]

    tests = [[18, 23], [56, 60], [37, 39], [20, 37], [40, 45], [30, 45]]

    for mine in tests:
        d = match(rule, mine)
        print(d)


##############################################################################

if __name__ == "__main__":
    main()
