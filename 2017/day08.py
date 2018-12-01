#!/usr/bin/env python3

from io import StringIO
import re
import sys


test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
test_result = 1

def parse_line(line):
    m = re.match(
        r'(?P<name>\w+)\s+(?P<sign>inc|dec)\s+(?P<delta>-?\d+)\s+'
        'if\s+(?P<cond_name>\w+)\s*(?P<cond>.*)$',
        line.strip()
    )
    if m:
        return (
            m.group("name"),
            int(m.group("delta")) * (2 * int(m.group("sign") == "inc") - 1),
            m.group("cond_name"),
            m.group("cond"),
        )
    else:
        return None


def compile(inp):
    return [
        instr
        for instr in (
            parse_line(line)
            for line in inp.readlines()
        )
        if instr is not None
    ]


def execute(program):
    memory = dict()
    highest_value = 0
    for instr in program:
        try:
            value = memory[instr[0]]
        except KeyError:
            value = 0
        if eval("%d%s" % (memory.get(instr[2], 0), instr[3])):
            value += instr[1]
            if value > highest_value:
                highest_value = value
            memory[instr[0]] = value
    return max(memory.values()), highest_value


assert execute(compile(StringIO(test_input)))[0] == test_result

print("Final max: %d, highest value: %d" % execute(compile(sys.stdin)))
