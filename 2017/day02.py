#!/usr/bin/env python3

import io
import sys
import textwrap


test1 = textwrap.dedent("""\
    5 1 9 5
    7 5 3
    2 4 6 8
""")
test1_res = 18
test2 = textwrap.dedent("""\
    5 9 2 8
    9 4 7 3
    3 8 6 5
""")
test2_res = 9


def read_input(f, sep="\t"):
    return [
        [int(x) for x in line.strip().split(sep)]
        for line in f.readlines()
        if line
    ]


def part1(data):
    return sum(max(row) - min(row) for row in data)


def part2(data):
    return sum(
        x // y
        for row in data
        for ix, x in enumerate(row)
        for iy, y in enumerate(row)
        if ix != iy and x % y == 0
    )


res = part1(read_input(io.StringIO(test1), " "))
print("Test 1: %d == %d?" % (res, test1_res))
assert res == test1_res

res = part2(read_input(io.StringIO(test2), " "))
print("Test 2: %d == %d?" % (res, test2_res))
assert res == test2_res

data = read_input(sys.stdin)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
