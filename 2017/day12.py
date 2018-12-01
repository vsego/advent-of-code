#!/usr/bin/env python3

from io import StringIO
from itertools import count
import re
from sys import stdin


test = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
test_res = 6

def parse_input(inp):
    return {
        int(m.group("from")): [int(x) for x in m.group("to").split(", ")]
        for m in (
            re.match(
                r'(?P<from>\d+)\s*<->\s*(?P<to>\d+(?:,\s*\d+)*)$',
                line.strip()
            )
            for line in inp.readlines()
        )
        if m
    }


def part1(data, start=0):
    visited = {start}
    while True:
        newly_visited = (
            visited |
            {
                target
                for n, v in data.items()
                if n in visited
                for target in v
            }
        )
        if len(visited) == len(newly_visited):
            return visited
        visited = newly_visited


def part2(data):
    nodes = set(data.keys())
    for cnt in count(0):
        try:
            nodes -= part1(data, nodes.pop())
        except KeyError:
            return cnt


print(
    'Testing that len(part1(test)) == %d == %d' % (
        len(part1(parse_input(StringIO(test)))), test_res
    )
)
assert len(part1(parse_input(StringIO(test)))) == test_res

data = parse_input(stdin)
print("Part 1:", len(part1(data)))
print("Part 2:", part2(data))
