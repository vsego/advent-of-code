#!/usr/bin/env python3

"""
Solution for
[Day 1 of Advent of Code 2020](https://adventofcode.com/2020/day/1).
"""


from common import AoCSolution, main


class Day01(AoCSolution):
    """
    Solution for
    [Day 1 of Advent of Code 2020](https://adventofcode.com/2020/day/1).
    """

    tests = [
        {
            "args": ([1721, 979, 366, 299, 675, 1456],),
            "results": {1: 514579, 2: 241861950},
        },
    ]

    def __init__(self):
        self.expenses = None

    def init_from_values(self, expenses):
        """
        Initialise the object from arguments.
        """
        self.expenses = expenses

    def init_from_file(self, f):
        """
        Initialise the object from the text file `f`.
        """
        self.expenses = [int(line.strip()) for line in f]

    def part1(self):
        """
        Return the solution for part 1.
        """
        return next(
            exp1 * exp2
            for idx1, exp1 in enumerate(self.expenses)
            for idx2, exp2 in enumerate(self.expenses[idx1 + 1:])
            if exp1 + exp2 == 2020
        )

    def part2(self):
        """
        Return the solution for part 2.
        """
        return next(
            exp1 * exp2 * exp3
            for idx1, exp1 in enumerate(self.expenses)
            for idx2, exp2 in enumerate(self.expenses[idx1 + 1:])
            for idx3, exp3 in enumerate(self.expenses[idx2 + 1:])
            if exp1 + exp2 + exp3 == 2020
        )


if __name__ == "__main__":
    main(Day01)
