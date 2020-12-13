#!/usr/bin/env python3

"""
Solution for
[Day 13 of Advent of Code 2020](https://adventofcode.com/2020/day/13).
"""

import math
import sys


class Day13:
    """
    Solution for
    [Day 13 of Advent of Code 2020](https://adventofcode.com/2020/day/13).
    """

    def __init__(self):
        self.min_time = None
        self.buses = None

    @classmethod
    def from_values(cls, min_time, buses):
        """
        Return a `Day13` instance initialised from `min_time` and `buses`.
        """
        result = cls()
        result.min_time = min_time
        result.buses = buses
        return result

    @classmethod
    def from_file(cls, fname):
        """
        Return a `Day13` instance initialised from the text file `fname`.
        """
        result = cls()
        with open(fname) as f:
            result.min_time = int(next(f).strip())
            result.buses = [
                None if bus == "x" else int(bus)
                for bus in next(f).strip().split(",")
            ]
        return result

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

    @classmethod
    def test(cls, part, min_time, buses, expected):
        """
        Return the solution for part 2.
        """
        print(f"Testing part {part} for ({min_time}, {buses})...", end="")
        result = getattr(cls.from_values(min_time, buses), f"part{part}")()
        if result == expected:
            print(" Ok.")
        else:
            print(f" Failed, with {result} != {expected}.")


if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except IndexError:
        # Run tests.
        Day13.test(1, 939, [7, 13, None, None, 59, None, 31, 19], 295)
        Day13.test(2, None, [7, 13, None, None, 59, None, 31, 19], 1068781)
        Day13.test(2, None, [17, None, 13, 19], 3417)
        Day13.test(2, None, [67, 7, 59, 61], 754018)
        Day13.test(2, None, [67, None, 7, 59, 61], 779210)
        Day13.test(2, None, [67, 7, None, 59, 61], 1261476)
        Day13.test(2, None, [1789, 37, 47, 1889], 1202161486)
    else:
        # Run the real thing.
        day13 = Day13.from_file(fname)
        print("Part 1:", day13.part1())
        print("Part 2:", day13.part2())
