#!/usr/bin/env python3

import io
import re
import sys
import textwrap


test = textwrap.dedent("""\
    Begin in state A.
    Perform a diagnostic checksum after 6 steps.

    In state A:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state B.
      If the current value is 1:
        - Write the value 0.
        - Move one slot to the left.
        - Continue with state B.

    In state B:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the left.
        - Continue with state A.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state A.
""")
test_res = 3


def read_input(f):
    res = {
        'begin_state': None,
        'chksm_steps': None,
        'transforms': dict(),
    }
    rule = {
        "state": None,
        "read": None,
        "write": None,
        "move_by": None,
        "new_state": None,
    }
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"Begin in state (\w+).$", line)
        if m:
            res["begin_state"] = m.group(1)
            continue
        m = re.match(
            r"Perform a diagnostic checksum after (\d+) steps.$", line
        )
        if m:
            res["chksm_steps"] = int(m.group(1))
            continue
        m = re.match(r"In state (\w+):$", line)
        if m:
            rule["state"] = m.group(1)
            continue
        m = re.match(r"If the current value is ([01]):$", line)
        if m:
            rule["read"] = (m.group(1) == "1")
            continue
        m = re.match(r"- Write the value ([01]).$", line)
        if m:
            rule["write"] = (m.group(1) == "1")
            continue
        m = re.match(r"- Move one slot to the (left|right).$", line)
        if m:
            rule["move_by"] = (1 if m.group(1).lower() == "right" else -1)
            continue
        m = re.match(r"- Continue with state (\w+).$", line)
        if m:
            rule["new_state"] = m.group(1)
            res["transforms"][(rule["state"], rule["read"])] = {
                f: rule[f] for f in ("new_state", "write", "move_by")
            }
            continue
    return res


def run(blueprint):
    tape1 = set()
    pos = 0
    state = blueprint["begin_state"]
    for step in range(blueprint["chksm_steps"]):
        read = (pos in tape1)
        action = blueprint["transforms"][(state, read)]
        if action["write"] != read:
            if action["write"]:
                tape1.add(pos)
            else:
                tape1.discard(pos)
        pos += action["move_by"]
        state = action["new_state"]
    return len(tape1)


res = run(read_input(io.StringIO(test)))
print("Testing: %d == %d?" % (res, test_res))
assert res == test_res

blueprint = read_input(sys.stdin)
print("Solution:", run(blueprint))
