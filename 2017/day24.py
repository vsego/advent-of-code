#!/usr/bin/env python3

import io
import re
import sys
import textwrap


test = textwrap.dedent("""\
    0/2
    2/2
    2/3
    3/4
    3/5
    0/1
    10/1
    9/10
""")
test_res = 31


def read_input(f):
    return [
        # A set would make more sense, but we'll have a set of these,
        # so we must use an immutable type
        (int(m.group(1)), int(m.group(2)))
        for m in (
            re.match(r"(\d+)/(\d+)$", line.strip())
            for line in f.readlines()
        )
        if m
    ]


def build(data, previous, used, res, length=None):
    try:
        return max(
            build(
                data,
                (comp[0] if comp[1] == previous else comp[1]),
                used | {comp},
                res + sum(comp),
                (None if length is None else length + 1)
            )
            for comp in data
            if previous in comp and comp not in used
        )
    except ValueError:
        return length, res

    
def part1(data):
    return build(data, 0, set(), 0)[1]


def part2(data):
    return build(data, 0, set(), 0, 0)[1]


print("Testing...", end="")
res = part1(read_input(io.StringIO(test)))
print(" %d == %d?" % (res, test_res))
assert res == test_res

data = read_input(sys.stdin)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
