#!/usr/bin/env python3

from math import ceil, sqrt


tests = (
    (1, 0), (12, 3), (23, 2), (1024, 31)
)


def solve1(n):
    r = int(ceil((sqrt(n) - 1) / 2))
    x = r
    y = min(abs(n - ((2 * r + 1) ** 2 - k * r)) for k in range(1, 9, 2))
    return x + y


def gv(m, x, y):
    try:
        if x >= 0 and y >= 0:
            return m[y][x]
        else:
            return 0
    except IndexError:
        return 0


def set_val_at(m, x, y, n):
    m[y][x] = res = sum(
        gv(m, i, j)
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
        if i != x or j != y
    )
    if res >= n:
        raise Done(res)


class Done(Exception):
    def __init__(self, n):
        self.n = n


def solve2(n):
    m = [[1]]
    d = 1
    try:
        while True:
            d += 2
            m = [
                [
                    0 if any(v in {0, d-1} for v in (x, y)) else m[y-1][x-1]
                    for x in range(d)
                ]
                for y in range(d)
            ]
            for y in range(d - 2, -1, -1):
                set_val_at(m, d - 1, y, n)
            for x in range(d - 2, -1, -1):
                set_val_at(m, x, 0, n)
            for y in range(1, d):
                set_val_at(m, 0, y, n)
            for x in range(1, d):
                set_val_at(m, x, d - 1, n)
    except Done as e:
        for line in m:
            print("".join("%7d" % v for v in line))
        return e.n


for test in tests:
    print("Testing that solve(%d) = %d = %d." % (test[0], solve1(test[0]), test[1]))
    assert solve1(test[0]) == test[1]

print()
n = int(input("Which square do you want to access? "))

print("Solution 1:", solve1(n))
print("Solution 2:", solve2(n))
