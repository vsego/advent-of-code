#!/usr/bin/env python3

"""
Solution for
[Day 1 of Advent of Code 2020](https://adventofcode.com/2020/day/1).
"""

import re

from common import AoCSolution, main


class Day02(AoCSolution):
    """
    Solution for
    [Day 2 of Advent of Code 2020](https://adventofcode.com/2020/day/2).
    """

    tests = [
        {
            "args": (
                [
                    {"min": 1, "max": 3, "ch": "a", "passwd": "abcde"},
                    {"min": 1, "max": 3, "ch": "b", "passwd": "cdefg"},
                    {"min": 2, "max": 9, "ch": "c", "passwd": "ccccccccc"},
                ],
            ),
            "results": {1: 2, 2: 1},
        },
    ]

    def __init__(self):
        self.expenses = None

    def init_from_values(self, data):
        """
        Initialise the object from arguments.
        """
        self.passwds = data

    @staticmethod
    def line_to_passwd(line):
        m = re.match(
            r"(?P<min>\d+)-(?P<max>\d+)\s+(?P<ch>\w):\s+(?P<passwd>.*)", line,
        )
        if not m:
            raise ValueError(f"invalid line {repr(line)}")
        return {
            f: t(m.group(f))
            for t, f in (
                (int, "min"), (int, "max"), (str, "ch"), (str, "passwd"),
            )
        }

    def init_from_file(self, f):
        """
        Initialise the object from the text file `f`.
        """
        self.passwds = [self.line_to_passwd(line.strip()) for line in f]

    def part1(self):
        """
        Return the solution for part 1.
        """
        return sum(
            1
            for passwd, cnt in (
                (passwd, sum(1 for c in passwd["passwd"] if c == passwd["ch"]))
                for passwd in self.passwds
            )
            if passwd["min"] <= cnt <= passwd["max"]
        )

    def part2(self):
        """
        Return the solution for part 2.
        """
        return sum(
            1
            for passwd, pos1, pos2, ch in (
                (passwd["passwd"], passwd["min"], passwd["max"], passwd["ch"])
                for passwd in self.passwds
            )
            if (
                1 <= pos1 <= len(passwd)
                and 1 <= pos2 <= len(passwd)
                and (passwd[pos1 - 1] == ch) is (passwd[pos2 - 1] != ch)
            )
        )


if __name__ == "__main__":
    main(Day02)
