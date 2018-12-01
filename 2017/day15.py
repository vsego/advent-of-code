#!/usr/bin/env python3

import re


test = (65, 8921)
test_res = 588


def mkgen(name, value, check=False):
    factor = {"A": 16807, "B": 48271}[name.upper()]
    if check:
        check = {"A": 4, "B": 8}[name.upper()] - 1
    while True:
        value = (value * factor) % 2147483647
        if not check or value & check == 0:
            yield value


def solve(startA, startB, part=1):
    patt = (1 << 16) - 1
    genA = mkgen("A", startA, part == 2)
    genB = mkgen("B", startB, part == 2)
    return sum(
        1
        for step in range(40000000 if part == 1 else 5000000)
        if next(genA) & patt == next(genB) & patt
    )


def get_input_line():
    m = re.search("\d+", input())
    if m:
        return int(m.group(0))


print("Testing...")
res = solve(*test)
print("Is %d = %d?" % (res, test_res))
assert res == test_res

a = get_input_line()
b = get_input_line()
print("Part 1:", solve(a, b))
print("Part 2:", solve(a, b, 2))
