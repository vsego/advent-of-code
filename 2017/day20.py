#!/usr/bin/env python3

from io import StringIO
import itertools
import re
import sys
import textwrap


test = textwrap.dedent("""\
    p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")
test_res = 0

test2 = textwrap.dedent("""\
    p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
    p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
    p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
    p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
""")
test2_res = 1


def line2dict(line):
    coords_re = re.compile(
        r"\s*" +
        r"\s*,\s*".join(
            r"%s\s*=\s*<" % pva + ",".join(
                r"\s*(?P<%s%s>-?\d+)\s*" % (pva, c)
                for c in "xyz"
            ) + ">" for pva in "pva"
        ) +
        r"\s*$"
    )
    m = coords_re.match(line)
    if m:
        return {
            pva: tuple(int(m.group("%s%s" % (pva, c))) for c in "xyz")
            for pva in "pva"
        }


def read_data(f):
    return [
        d for d in (
            line2dict(line)
            for line in f.readlines()
        )
        if d
    ]


def dist(vect1, vect2=None):
    if vect2 is None:
        vect2 = (0, 0, 0)
    return sum(abs(v1-v2) for v1, v2 in zip(vect1, vect2))


def sort_key(particle):
    return tuple(dist(particle[pva]) for pva in "avp")


def part1(data):
    return min(enumerate(data), key=lambda iv: sort_key(iv[1]))[0]


def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


def part2(data):
    data.sort(key=sort_key)
    for t in itertools.count():
        cnts = dict()
        for part in data:
            try:
                cnts[part["p"]] += 1
            except KeyError:
                cnts[part["p"]] = 1
        data = [part for part in data if cnts[part["p"]] <= 1]
        dists1 = [dist(part1["p"], part2["p"]) for part1, part2 in zip(data, data[1:])]
        for part in data:
            for f1, f2 in ("va", "pv"):
                part[f1] = tuple(x + y for x, y in zip(part[f1], part[f2]))
        dists2 = [dist(part1["p"], part2["p"]) for part1, part2 in zip(data, data[1:])]
        if (
            all(
                len({sign(part[pva][i]) for pva in "pva"} - {0}) <= 1
                for part in data
                for i in range(3)
            ) and
            all(d1 <= d2 for d1, d2 in zip(dists1, dists2))
        ):
            return len(data)


res = part1(read_data(StringIO(test)))
print("Testing: %d == %d?" % (res, test_res))
assert res == test_res

res = part2(read_data(StringIO(test2)))
print("Testing: %d == %d?" % (res, test2_res))
assert res == test2_res

data = read_data(sys.stdin)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
