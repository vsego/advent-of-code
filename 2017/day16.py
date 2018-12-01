#!/usr/bin/env python3

import re


test="s1,x3/4,pe/b"
test_res = "baedc"


def init_dancers(n=16):
    return [chr(i) for i in range(ord('a'), ord('a') + n)]


def dance(moves, dancers=None, n=16, join=True):
    if dancers is None:
        dancers = init_dancers(n)
    if moves:
        moves = moves.split(",")
    for move in moves:
        m = re.match(
            r'(?:(?:s(?P<X>\d+))|(?P<xp>[xp])(?P<A>\w+)/(?P<B>\w+))$',
            move.strip()
        )
        if m:
            try:
                x = int(m.group("X"))
                dancers = dancers[-x:] + dancers[:-x]
            except TypeError:
                a = m.group("A")
                b = m.group("B")
                if m.group("xp") == "x":
                    a = int(a)
                    b = int(b)
                else:
                    a = dancers.index(a)
                    b = dancers.index(b)
                dancers[a], dancers[b] = dancers[b], dancers[a]
        else:
            print('Invalid move: "%s"' % move)
    return ("".join(dancers) if join else dancers)


def superdance(moves, n=16):
    tot = 1000000000
    current = dance("", n=n, join=False)
    cache = {"".join(current): 0}
    for dance_id in range(1, tot):
        current = dance(moves, current, n, False)
        cs = "".join(current)
        try:
            prev = cache[cs] + (tot - cache[cs]) % (dance_id - cache[cs])
            print("Cache size:", len(cache))
            return next(d for d, di in cache.items() if di == prev)
        except KeyError:
            cache[cs] = dance_id
    return cs


res = dance(test, n=5)
print('Checking 1: "%s" ?= "%s"' % (res, test_res))
assert res == test_res

moves = input()
print("Part 1:", dance(moves))
print("Part 2:", superdance(moves))
