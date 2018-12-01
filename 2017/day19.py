#!/usr/bin/env python3

import io
import sys
import textwrap


test = textwrap.dedent("""\
         |          
         |  +--+    
         A  |  C    
     F---|----E|--+ 
         |  |  |  D 
         +B-+  +--+ 
    """)
test_res = ("ABCDEF", 38)


def read_map(f):
    return [
        line.rstrip("\n") for line in f.readlines()
    ]


def find_path(map_):
    d = (0, 1)
    p = (next(i for i, c in enumerate(map_[0]) if c != " "), 0)
    path = list()
    steps = 0
    while True:
        steps += 1
        for nd in (d, (d[1], d[0]), (-d[1], -d[0])):
            np = tuple(x + y for x, y in zip(p, nd))
            if 0 <= np[1] < len(map_):
                if 0 <= np[0] < len(map_[np[1]]):
                    c = map_[np[1]][np[0]]
                    if c != " ":
                        p = np
                        d = nd
                        break
        else:
            return "".join(path), steps
        if c not in "-|+":
            path.append(c)


res = find_path(read_map(io.StringIO(test)))
print("Testing: %s == %s?" % (repr(res), repr(test_res)))
assert res == test_res

map_ = read_map(sys.stdin)
print("Solution:", find_path(map_))
