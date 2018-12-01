#!/usr/bin/env python3

import sys


def read_code(f):
    return [tuple(line.strip().split()) for line in f.readlines() if line]


def solve(prog, part=1):
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
    if part == 2:
        mem['a'] = 1
    mul_cnt = 0
    idx = 0
    while 0 <= idx < len(prog):
        cmd = prog[idx]
        delta = 1
        if cmd[0] == "set":
            set(cmd[1], get(cmd[2]))
        elif cmd[0] == "sub":
            set(cmd[1], get(cmd[1]) - get(cmd[2]))
        elif cmd[0] == "mul":
            set(cmd[1], get(cmd[1]) * get(cmd[2]))
            mul_cnt += 1
        elif cmd[0] == "jnz":
            if get(cmd[1]):
                delta = get(cmd[2])
        else:
            raise ValueError("wrong command: %s" % cmd[0])
        idx += delta
    return (mul_cnt if part == 1 else get('h'))


def translate(prog):
    print("Code analysis:")
    for idx, cmd in enumerate(prog):
        if cmd[0] == "set":
            cmd = "%s = %s" % cmd[1:]
        elif cmd[0] == "sub":
            if cmd[2][0] == "-":
                cmd = "%s += %d" % (cmd[1], -int(cmd[2]))
            else:
                cmd = "%s -= %s" % (cmd[1], cmd[2])
        elif cmd[0] == "mul":
            cmd = "%s *= %s" % cmd[1:]
        elif cmd[0] == "jnz":
            try:
                always = (int(cmd[1]) != 0)
            except ValueError:
                always = False
            if always:
                cmd = "goto(%d)" % (idx + int(cmd[2]))
            else:
                cmd = "if %s then goto(%d)" % (cmd[1], idx + int(cmd[2]))
        else:
            raise ValueError("wrong command: %s" % cmd[0])
        print("%6d: %s" % (idx, cmd))


def is_prime(x):
    if x < 2:
        return True
    for p in range(2, int(x ** 0.5) + 1):
        if x % p == 0:
            return False
    return True


def part2():
    h = 0
    b = 106700
    c = b + 17000
    for x in range(b, c + 1, 17):
        if not is_prime(x):
            h += 1
    return h


prog = read_code(sys.stdin)

# Brute force won't work. One needs to analyse the input and optimize the code
# print("Part 2:", solve(prog, 2))
# We first translate the prog to more readable format:
# translate(prog)
# Now, detect the loops, cut out the slack, optimize it, and write `part2`
# It should boil down to counting (non)primes between b and c
print("Part 1:", solve(prog))
print("Part 2:", part2())
print("Warning: Part 2 doesn't depend on input!")
print("Check the in-code comments for details.")
