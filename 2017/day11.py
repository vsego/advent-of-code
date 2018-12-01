#!/usr/bin/env python3

tests = (
    ("ne,ne,ne", 3),
    ("ne,ne,sw,sw", 0),
    ("ne,ne,s,s", 2),
    ("se,sw,se,sw,sw", 3),
)

moves = {
    "nw": (-1, -1),
    "n":  (0, -2),
    "ne": (1, -1),
    "sw": (-1, 1),
    "s":  (0, 2),
    "se": (1, 1),
}


def solve(path):
    pos = (0, 0)
    md = 0
    for step in path.split(","):
        pos = tuple(pos[i] + moves[step][i] for i in (0, 1))
        d = abs(pos[0]) + max(0, abs(pos[1]) - abs(pos[0])) // 2
        if d > md:
            md = d
    return d, md


for test in tests:
    print(
        'Testing that solve("%s") == %d == %d' % (
            test[0], solve(test[0])[0], test[1]
        )
    )
    assert solve(test[0])[0] == test[1]

print("Solution:", solve(input()))
