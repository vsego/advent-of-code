#!/usr/bin/env python3

from io import StringIO
from itertools import count
from sys import stdin


test = """
    0: 3
    1: 2
    4: 4
    6: 4"""
test_res = 24


def parse_input(inp):
    return dict(
        tuple(int(x) for x in line.split(": "))
        for line in (
            line.strip() for line in inp.readlines()
        )
        if line
    )


def part1(data):
    return sum(
        scanner * depth
        for scanner, depth in data.items()
        if depth == 1 or scanner % (2 * (depth - 1)) == 0
    )


def part2(data):
    if any(depth == 1 for depth in data.values()):
        return None
    return next(
        delay for delay in count()
        if not any(
            (scanner + delay) % (2 * (depth - 1)) == 0
            for scanner, depth in data.items()
        )
    )


res = part1(parse_input(StringIO(test)))
print("Testing: %d ?= %d" % (res, test_res))
assert res == test_res

data = parse_input(stdin)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
