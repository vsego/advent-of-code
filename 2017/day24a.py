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
    comps = [
        # A set would make more sense, but we'll have a set of these,
        # so we must use an immutable type
        (int(m.group(1)), int(m.group(2)))
        for m in (
            re.match(r"(\d+)/(\d+)$", line.strip())
            for line in f.readlines()
        )
        if m
    ]
    followups = {
        port: [comp for comp in comps if port in comp]
        for port in set.union(*[set(comp) for comp in comps])
    }
    available = {
        comp: sum(1 for c in comps if set(comp) == set(c))
        for comp in comps
    }
    return followups, available


def build(data, previous, res, length=None, pc=None):
    if pc:
        data[1][pc] -= 1
        # We could remove zeros from followups, but that would actually
        # slow the algorithm down
    if length is not None:
        length += 1
    try:
        res = max(
            build(
                data,
                (comp[0] if comp[1] == previous else comp[1]),
                res + sum(comp),
                length,
                comp
            )
            for comp in data[0][previous]
            if data[1][comp]
        )
        return res
    except ValueError:
        return length, res
    finally:
        if pc:
            data[1][pc] += 1

    
def part1(data):
    return build(data, 0, 0)[1]


def part2(data):
    return build(data, 0, 0, 0)[1]


print("Testing...", end="")
res = part1(read_input(io.StringIO(test)))
print(" %d == %d?" % (res, test_res))
assert res == test_res

data = read_input(sys.stdin)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
