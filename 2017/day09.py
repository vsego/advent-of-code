#!/usr/bin/env python3

tests = (
    ("{}", 1),
    ("{{{}}}", 6),
    ("{{},{}}", 5),
    ("{{{},{},{{}}}}", 16),
    ("{<a>,<a>,<a>,<a>}", 1),
    ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
    ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
    ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
)


def strip_garbage(data, fr=0):
    removed = 0
    while True:
        if data[fr] == ">":
            return removed, fr
        if data[fr] == "!":
            fr += 2
        else:
            fr += 1
            removed += 1


def get_score(data, fr=0, score=0):
    res = [score, 0]
    score += 1
    while True:
        try:
            ch = data[fr]
        except IndexError:
            return res, fr
        if ch == "}":
            return res, fr
        elif ch == "{":
            gs, fr = get_score(data, fr + 1, score)
            res[0] += gs[0]
            res[1] += gs[1]
        elif ch == "<":
            gs, fr = strip_garbage(data, fr + 1)
            res[1] += gs
        fr += 1


for test, res in tests:
    print(
        'Testing that get_score("%s") == %d == %d...' % (
           test, get_score(test)[0][0], res
        )
    )
    assert get_score(test)[0][0] == res

print(get_score(input())[0])
