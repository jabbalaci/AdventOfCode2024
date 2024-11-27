#!/usr/bin/env python3

import json
from collections import deque
from pprint import pprint


class Graph:
    def __init__(self, fname: str) -> None:
        self.d = self.read(fname)
        self.remove_self_references()
        self.make_undirected()
        self.remove_duplicates()

    def remove_duplicates(self) -> None:
        for k, values in self.d.items():
            self.d[k] = list(set(values))
        #

    def make_undirected(self) -> None:
        new = {}
        for k, values in self.d.items():
            for v in values:
                if k not in new:
                    new[k] = []
                new[k].append(v)
                if v not in new:
                    new[v] = []
                new[v].append(k)
            #
        #
        self.d = new

    def remove_self_references(self) -> None:
        for k, values in self.d.items():
            to_remove = []
            for v in values:
                if v == k:
                    to_remove.append(v)
                #
            #
            for e in to_remove:
                values.remove(e)
            #
        #

    def traverse(self, start_node: str) -> None:
        d = self.d
        if start_node not in d:
            raise Exception(f"start node '{start_node}' not found")
        # else
        visited: list[str] = []
        visible: deque[str] = deque([start_node])

        while visible:  # while not empty
            curr = visible.popleft()
            can_be_seen = d[curr]
            for e in can_be_seen:
                if (e not in visible) and (e not in visited):
                    visible.append(e)
                #
            #
            visited.append(curr)
            #
            # print(visited)
            # print(visible)
            # print("---")
            # input()
        #
        print("Number of visited nodes:", len(visited))

    def read(self, fname: str) -> dict:
        with open(fname) as f:
            return json.load(f)

    def debug(self) -> None:
        pprint(self.d)


def main():
    fname = "graph.json"

    g = Graph(fname)

    g.debug()
    print("---")

    g.traverse("a")


##############################################################################

if __name__ == "__main__":
    main()
