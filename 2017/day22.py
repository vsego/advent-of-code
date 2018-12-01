#!/usr/bin/env python3

from copy import deepcopy
import io
import sys
import textwrap


test = textwrap.dedent("""\
    ..#
    #..
    ...
""")
test1_n = 70
test1_res = 41
test2_res = 5587
test3_n = 100
test3_states = "cwif"
test3_res = 26
test4_n = 10000000
test4_states = "cwif"
test4_res = 2511944

def read_input(f):
    def proc_line(line):
        nonlocal size, d
        line = line.strip()
        if size is None:
            size = len(line)
            d = size // 2
        return line
    size = d = None
    return {
        "i": {
            (x - d, y - d)
            for y, line in enumerate(f.readlines())
            for x, ch in enumerate(proc_line(line))
            if ch == "#"
        },
    }


def solve(nodes, n=10000, states="ci"):
    nodes = deepcopy(nodes)
    states = dict(zip(states, states[1:] + states[:1]))
    for state in states:
        if state != 'c' and state not in nodes:
            nodes[state] = set()
    pos = (0, 0)
    dir = (0, -1)
    res = 0
    for burst in range(n):
        # For horizontal, reverse = left; for vertical, reverse = right
        # This factor makes them both left
        f = (1 if dir[0] == 0 else -1)
        for state, state_nodes in nodes.items():
            if pos in state_nodes:
                if state == "w":
                    pass
                elif state == "i":
                    dir = (-f * dir[1], -f * dir[0])
                elif state == "f":
                    dir = (-dir[0], -dir[1])
                else:
                    raise ValueError("wrong state: %s" + state)
                break
        else:
            state = "c"
            dir = (f * dir[1], f * dir[0])
        if state != "c":
            nodes[state].discard(pos)
        state = states[state]
        if state != "c":
            nodes[state].add(pos)
            if state == "i":
                res += 1
        pos = tuple(p + d for p, d in zip(pos, dir))
        # if burst < 5:
        #     print(burst)
        #     for y in range(-4, 5):
        #         print("".join(
        #             ("[%s]" if pos == (x, y) else " %s ") % (
        #                 '#' if (x, y) in nodes['i'] else '.'
        #             )
        #             for x in range(-4, 5)
        #         ))
    return res


res = solve(read_input(io.StringIO(test)), test1_n)
print("Testing: %d == %d?" % (res, test1_res))
assert res == test1_res

res = solve(read_input(io.StringIO(test)))
print("Testing: %d == %d?" % (res, test2_res))
assert res == test2_res

res = solve(read_input(io.StringIO(test)), test3_n, test3_states)
print("Testing: %d == %d?" % (res, test3_res))
assert res == test3_res

res = solve(read_input(io.StringIO(test)), test4_n, test4_states)
print("Testing: %d == %d?" % (res, test4_res))
assert res == test4_res

data = read_input(sys.stdin)
print("Part 1:", solve(data))
print("Part 2:", solve(data, 10000000, "cwif"))

