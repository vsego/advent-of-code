#!/usr/bin/env python3

from functools import reduce
from operator import ixor


test = "3,4,1,5"
test_len = 5
test_res = 12


def part1(lengths, n=256):
    pos = 0
    data = list(range(n))
    lengths = [int(x) for x in lengths.split(",")]
    for skip, length in enumerate(lengths):
        sublist = [
            data[i % len(data)]
            for i in range(pos, pos + length)
        ]
        sublist.reverse()
        for i, el in enumerate(sublist, start=pos):
            data[i % len(data)] = el
        pos += length + skip
    return data[0] * data[1]


def part2(lengths, n=256):
    pos = 0
    data = list(range(n))
    lengths = [ord(ch) for ch in lengths] + [17, 31, 73, 47, 23]
    skip = -1
    for round_ in range(64):
        for skip, length in enumerate(lengths, start=skip+1):
            sublist = [
                data[i % len(data)]
                for i in range(pos, pos + length)
            ]
            sublist.reverse()
            for i, el in enumerate(sublist, start=pos):
                data[i % len(data)] = el
            pos += length + skip
    res = "".join(
        "%02x" % reduce(ixor, data[fr+1:fr+16], data[fr])
        for fr in range(0, len(data), 16)
    )
    return res


if __name__ == "__main__":
    print(
        'Testing that part1("%s", %d) == %d == %d.' % (
            test, test_len, part1(test, test_len), test_res
        )
    )
    assert part1(test, test_len) == test_res

    lengths = input().strip()

    print("Part 1:", part1(lengths))
    print("Part 2:", part2(lengths))

