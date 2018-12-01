import itertools
import sys

instr = [int(x) for x in sys.stdin.readlines()]

def solve(instr, part2=False):
    p = 0
    for cnt in itertools.count():
        if not 0 <= p < len(instr):
            return cnt
        np = p + instr[p]
        instr[p] += (-1 if part2 and instr[p] >= 3 else 1)
        p = np

print(solve(instr[:]))
print(solve(instr[:], True))
