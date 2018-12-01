#!/usr/bin/env python3

import io
import sys
import textwrap


test1 = textwrap.dedent("""\
    aa bb cc dd ee
    aa bb cc dd aa
    aa bb cc dd aaa
""")
test1_res = 2
test2 = textwrap.dedent("""\
    abcde fghij
    abcde xyz ecdab
    a ab abc abd abf abj
    iiii oiii ooii oooi oooo
    oiii ioii iioi iiio
""")
test2_res = 3


def read_input(f):
    return [line.split(" ") for line in f.read().splitlines() if line]


def part1(lines):
    return sum(
        1
        for line in lines
        if len(set(line)) == len(line)
    )


def part2(lines):
    return sum(
        1
        for line in (
            ["".join(sorted(w)) for w in line]
            for line in lines
        )
        if len(set(line)) == len(line)
    )


res = part1(read_input(io.StringIO(test1)))
print("Testing: %d == %d?" % (res, test1_res))
assert res == test1_res

res = part2(read_input(io.StringIO(test2)))
print("Testing: %d == %d?" % (res, test2_res))
assert res == test2_res

lines = read_input(sys.stdin)
print("Part 1:", part1(lines))
print("Part 2:", part2(lines))
