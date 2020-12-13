#!/usr/bin/env python3

"""
Solution for
[Day 13 of Advent of Code 2020](https://adventofcode.com/2020/day/13).
"""

import math

from common import AoCSolution, main


class Day13(AoCSolution):
    """
    Solution for
    [Day 13 of Advent of Code 2020](https://adventofcode.com/2020/day/13).
    """

    tests = [
        {
            "args": (939, [7, 13, None, None, 59, None, 31, 19]),
            "results": {1: 295, 2: 1068781},
        },
        {
            "args": (None, [17, None, 13, 19]),
            "results": {2: 3417},
        },
        {
            "args": (None, [67, 7, 59, 61]),
            "results": {2: 754018},
        },
        {
            "args": (None, [67, None, 7, 59, 61]),
            "results": {2: 779210},
        },
        {
            "args": (None, [67, 7, None, 59, 61]),
            "results": {2: 1261476},
        },
        {
            "args": (None, [1789, 37, 47, 1889]),
            "results": {2: 1202161486},
        },
    ]

    def __init__(self):
        self.min_time = None
        self.buses = None

    def init_from_values(self, min_time, buses):
        """
        Return a `Day13` instance initialised from `min_time` and `buses`.
        """
        self.min_time = min_time
        self.buses = buses

    def init_from_file(self, f):
        """
        Return a `Day13` instance initialised from the text file `f`.
        """
        self.min_time = int(next(f).strip())
        self.buses = [
            None if bus == "x" else int(bus)
            for bus in next(f).strip().split(",")
        ]

    def part1(self):
        """
        Return the solution for part 1.
        """
        which_bus, wait_time = min(
            (
                (idx, bus - self.min_time % bus)
                for idx, bus in enumerate(self.buses)
                if bus
            ),
            key=lambda el: el[1],
        )
        return wait_time * self.buses[which_bus]

    @staticmethod
    def _euler2(a, p, b, q):
        """
        Return the result of Euler algorithm for `a`, `p`, `b`, and `q`.

        The arguments are used as in Euler's original article (see `euler` for
        more details).

        The method is ignoring special cases (like `a == b`).
        """
        if a < b:
            a, p, b, q = b, q, a, p
        v = p - q
        sign = 1
        oa, ob = a, b
        z0, z1 = 0, 1
        while True:
            z0, z1 = z1, z0 + z1 * (a // b)
            a, b = b, a % b
            sign *= -1
            if v % b == 0:
                factor = oa * ob // math.gcd(oa, ob)
                return factor, (q + sign * ob * z1 * (v // b)) % factor

    @classmethod
    def euler(cls, drs):
        """
        Return the result of Euler algorithm for `drs`.

        The arguments `drs` is a list of 2-tuples, each being a divisor and the
        required reminder. The method returns the smallest number that when
        divided by each divisor gives its corresponding reminder.

        The method is based on Euler's article that can be found
        [here](http://eulerarchive.maa.org/docs/translations/E036en.pdf).

        The algorithm can be generalised for more than 2 numbers, but it is
        quite fast this way, so I leave the optimisation to the reader. O:-)

        :param drs: An iterable of 2-tuples, each being a divisor and its
            required reminder.
        :return: The smallest nonnegative integer that divided by each of the
            divisors in `drs` gives their respective reminders.
        """
        while len(drs) > 1:
            drs = drs[:-2] + [cls._euler2(*drs[-1], *drs[-2])]
        return drs[0][1]

    def part2(self):
        return self.euler([
            (bus, -idx % bus) for idx, bus in enumerate(self.buses) if bus
        ])


if __name__ == "__main__":
    main(Day13)
