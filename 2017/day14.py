#!/usr/bin/env python3

from day10 import part2 as knot_hash
from itertools import count


test = "flqrgnkx"
test_res1 = 8108
test_res2 = 1242


def get_map(key):
    print("Building the map...")
    return [
        [
            bool(int(c, 16) & 8 >> d)
            for c in h
            for d in range(4)
        ] for h in (knot_hash("%s-%d" % (key, i)) for i in range(128))
    ]


def part1(disk_map):
    return sum(int(cell) for row in disk_map for cell in row)


def part2(disk_map):
    for region in count():
        try:
            last_visited = {next(
                (x, y)
                for x in range(128)
                for y in range(128)
                if disk_map[y][x] is True
            )}
            while last_visited:
                for x,y in last_visited:
                    disk_map[y][x] = region
                new_last_visited = set()
                for x, y in last_visited:
                    for i in range(-1, 2, 2):
                        xi = x + i
                        yi = y + i
                        if 0 <= xi <= 127 and disk_map[y][xi] is True:
                            new_last_visited.add((xi, y))
                        if 0 <= yi <= 127 and disk_map[yi][x] is True:
                            new_last_visited.add((x, yi))
                last_visited = new_last_visited
        except StopIteration:
            return region


data = get_map(test)
for idx, row in enumerate(data[:8]):
    print("".join(
        "." if cell is False else "#"
        for cell in row[:8]
    ) + ("-->" if idx in {0, 7} else ""))
print("""|      |
V      V""")
res1 = part1(data)
print("Testing: %d ?= %d..." % (res1, test_res1))
assert res1 == test_res1
res2 = part2(data)
print("Testing: %d ?= %d..." % (res2, test_res2))
assert res2 == test_res2
print("Ok.")

data = get_map(input())
print("Part 1:", part1(data))
print("Part 2:", part2(data))
