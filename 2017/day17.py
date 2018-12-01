#!/usr/bin/env python3

test = 3
test_res = 638


def part1(steps):
    state = [0]
    pos = 0
    for cycle in range(1, 2018):
        pos = (pos + steps) % len(state) + 1
        state = state[:pos] + [cycle] + state[pos:]
    return state[(pos + 1) % len(state)]


def part2(steps):
    pos = 0
    res = None
    for cycle in range(1, 50000001):
        pos = (pos + steps) % cycle + 1
        if pos == 1:
            res = cycle
    return res


res = part1(test)
print("Testing: part1(%d) == %d == %d?" % (test, res, test_res))
assert res == test_res

steps = int(input())
print("Part 1:", part1(steps))
print("Part 2:", part2(steps))
