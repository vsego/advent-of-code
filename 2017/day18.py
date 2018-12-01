#!/usr/bin/env python3

from io import StringIO
import sys
import textwrap


test = textwrap.dedent(
    """\
    set a 1
    add a 2
    mul a a
    mod a 5
    snd a
    set a 0
    rcv a
    jgz a -1
    set a 1
    jgz a -2 \
    """
)
test_res = 4


def read_code(f):
    return [line.strip().split() for line in f.readlines() if line]


def part1(prog):
    def set(n, v):
        mem[n] = v
    def get(n):
        try:
            return int(mem[n])
        except KeyError:
            try:
                return int(n)
            except ValueError:
                return 0
    mem = dict()
    last = None
    idx = 0
    while 0 <= idx < len(prog):
        line = prog[idx]
        cmd = line[0]
        if cmd == "snd":
            last = get(line[1])
        elif cmd == "set":
            set(line[1], get(line[2]))
        elif cmd == "add":
            set(line[1], get(line[1]) + get(line[2]))
        elif cmd == "mul":
            set(line[1], get(line[1]) * get(line[2]))
        elif cmd == "mod":
            set(line[1], get(line[1]) % get(line[2]))
        elif cmd == "rcv":
            if get(line[1]):
                return last
        elif cmd == "jgz":
            if get(line[1]) > 0:
                idx += get(line[2])
                continue
        idx += 1
    return last


def part2(prog):
    def set(n, v):
        mem[p][n] = v
    def get(n):
        try:
            return int(mem[p][n])
        except KeyError:
            try:
                return int(n)
            except ValueError:
                return 0
    mem = {i: {'p': i} for i in (0, 1)}
    queue = {i: list() for i in (0, 1)}
    idxes = [0, 0]
    res = 0
    p = 0
    while all(0 <= idx < len(prog) for idx in idxes):
        line = prog[idxes[p]]
        # print(p, line, mem[p])
        cmd = line[0]
        if cmd == "snd":
            queue[1 - p].append(get(line[1]))
            if p == 1:
                res += 1
        elif cmd == "set":
            set(line[1], get(line[2]))
        elif cmd == "add":
            set(line[1], get(line[1]) + get(line[2]))
        elif cmd == "mul":
            set(line[1], get(line[1]) * get(line[2]))
        elif cmd == "mod":
            set(line[1], get(line[1]) % get(line[2]))
        elif cmd == "rcv":
            try:
                set(line[1], queue[p].pop(0))
            except IndexError:
                p = 1 - p
                if prog[idxes[p]][0] == "rcv" and not queue[p]:
                    break
                else:
                    continue
        elif cmd == "jgz":
            if get(line[1]) > 0:
                idxes[p] += get(line[2]) - 1
        idxes[p] += 1
    return res


res = part1(read_code(StringIO(test)))
print("Testing: %d == %d?" % (res, test_res))
assert res == test_res

prog = read_code(sys.stdin)
print("Part 1:", part1(prog))
print("Part 2:", part2(prog))
