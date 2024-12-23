#!/usr/bin/env python3

"""
This is a graph problem.
In a graph, find the largest complete subgraph.
Complete subgraph: in this graph, every node is connected to every other node.

Solution: Bron-Kerbosch Algorithm

Link: https://www.altcademy.com/blog/discover-the-largest-complete-subgraph/
"""

from collections import defaultdict
from pprint import pprint

import helper

# ----------------------------------------------------------------------------


def bron_kerbosch(graph, r=set(), p=None, x=set()):
    if p is None:
        p = set(graph.keys())

    if not p and not x:
        yield r
    else:
        u = next(iter(p | x))  # Choose a pivot vertex
        for v in p - graph[u]:
            yield from bron_kerbosch(graph, r | {v}, p & graph[v], x & graph[v])
            p.remove(v)
            x.add(v)


def find_largest_complete_subgraph(graph):
    cliques = list(bron_kerbosch(graph))
    return max(cliques, key=len)


# ----------------------------------------------------------------------------


class Party:
    def __init__(self, fname: str) -> None:
        self.d: dict[str, set[str]] = self.parse_input(fname)

    def parse_input(self, fname: str) -> dict[str, set[str]]:
        d: dict[str, set[str]] = defaultdict(set)
        #
        lines: list[str] = helper.read_lines(fname)
        for line in lines:
            left, right = line.split("-")
            d[left].add(right)
            d[right].add(left)
        #
        return dict(d)

    def start(self) -> None:
        largest_complete_subgraph = find_largest_complete_subgraph(self.d)
        result = largest_complete_subgraph
        print(",".join(sorted(result)))

    def show(self) -> None:
        pprint(self.d)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    p = Party(fname)
    # p.show()

    p.start()


##############################################################################

if __name__ == "__main__":
    main()
