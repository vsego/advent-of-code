#!/usr/bin/env python3

import re
import sys


class Done(Exception):
    def __init__(self, wrong):
        self.wrong = wrong


tree = dict()
all_children = set()


def tree_weight(root):
    children = tree[root]["children"]
    weight = tree[root]["weight"]
    c2w = {
        name: tree_weight(name)
        for name in children
    }
    w2cnt = dict()
    for n, w in c2w.items():
        try:
            w2cnt[w] += 1
        except KeyError:
            w2cnt[w] = 1
    if len(w2cnt) > 1:
        raise Done(
            tree[next(n for n, w in c2w.items() if w2cnt[w] == 1)]["weight"] -
            next(w for n, w in c2w.items() if w2cnt[w] == 1) +
            next(w for n, w in c2w.items() if w2cnt[w] > 1)
        )
    return weight + sum(c2w.values())


for line in sys.stdin.readlines():
    m = re.match(
        r'(?P<name>\w+)\s+\((?P<weight>\d+)\)'
        r'(?:\s*->\s*(?P<children>[\w,\s]+))?$',
        line.strip()
    )
    if m:
        children = (
            re.split(r',\s*', m.group("children"))
            if m.group("children") else
            list()
        )
        tree[m.group("name")] = {
            "children": children,
            "weight": int(m.group("weight")),
        }
        all_children |= set(children)

root = (set(tree) - all_children).pop()
print(root)
try:
    print("w =", tree_weight(root))
except Done as e:
    print("Correct:", e.wrong)
