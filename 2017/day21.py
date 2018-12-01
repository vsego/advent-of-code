#!/usr/bin/env python3

import io
import sys
import textwrap


test = textwrap.dedent("""\
    ../.# => ##./#../...
    .#./..#/### => #..#/..../..../#..#
""")
test_iters = 2
test_res = 12


def read_input(f):
    return dict(
        line.split(" => ", 1)
        for line in (
            line.strip()
            for line in f.readlines()
        )
        if line
    )


def pic2line(pic):
    return "/".join(pic)


def find_match(rules, pic):
    for i in range(8):
        try:
            return rules[pic2line(pic)].split("/")
        except KeyError:
            if i % 2:
                pic.reverse()
            else:
                pic = [
                    "".join(pic[j][i] for j in range(len(pic)))
                    for i in range(len(pic))
                ]
    print("Whoops!")


def get_chunk(pic, size, x, y):
    xs = x * size
    ys = y * size
    return [line[xs:xs + size] for line in pic[ys:ys + size]]


def join_chunks(chunks):
    return [
        "".join(block[i] for block in row)
        for row in chunks
        for i in range(len(row[0]))
    ]


def solve(rules, iters=5):
    pic = [".#.", "..#", "###"]
    for it in range(iters):
        chunk_size = (2 if len(pic) % 2 == 0 else 3)
        pic = join_chunks([
            [
                find_match(rules, get_chunk(pic, chunk_size, x, y))
                for x in range(len(pic) // chunk_size)
            ]
            for y in range(len(pic) // chunk_size)
        ])
    return sum(1 for line in pic for c in line if c == "#")


res = solve(read_input(io.StringIO(test)), test_iters)
print("Testing: %d == %d?" % (res, test_res))
assert res == test_res

pic = read_input(sys.stdin)
print("Part 1:", solve(pic))
print("Part 2:", solve(pic, 18))
