#!/usr/bin/python3

from copy import deepcopy
import itertools
from math import gcd
import re


_tests = [
    {
        "input": [
            "<x=-1, y=0, z=2>",
            "<x=2, y=-10, z=-7>",
            "<x=4, y=-8, z=8>",
            "<x=3, y=5, z=-1>",
        ],
        "steps": 10,
        "part1": 179,
        "part2": 2772,
    },
    {
        "input": [
            "<x=-8, y=-10, z=0>",
            "<x=5, y=5, z=10>",
            "<x=2, y=-7, z=3>",
            "<x=9, y=-8, z=-3>",
        ],
        "steps": 100,
        "part1": 1940,
        "part2": 4686774924,
    },
]


def lines2moons(lines):
    """
    Return the moons map contained in a list of strings.

    :param lines: A list of strings describing moons.
    :return: A `list` of dictionaries, each containing two keys associated with
        a 3-list of `int` values. The keys are `"p"` (position) and `"v"`
        (velocity).
    """
    result = list()
    for y, line in enumerate(lines):
        m = re.match(
            r"<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>$", line.strip(),
        )
        if m:
            result.append({
                "p": [int(m.group(d)) for d in "xyz"],
                "v": [0, 0, 0],
            })
    return result


def read_input(fname="day12.in"):
    """
    Read the input file and return the list of moons it contains.

    :param fname: A string name of the file to read.
    :return: A `list` of dictionaries, each containing two keys associated with
        a 3-list of `int` values. The keys are `"p"` (position) and `"v"`
        (velocity).
    """
    with open(fname) as f:
        return lines2moons(f.readlines())


def vec2str(vec):
    """
    Return a string representation of a 3D vector.
    """
    return f"<x={vec[0]:5d}, y={vec[1]:5d}, z={vec[2]:5d}>"


def print_moon(moon):
    """
    Print one moon in a manner similar to the one in the problem.
    """
    print(f"pos={vec2str(moon['p'])}, vel={vec2str(moon['v'])}")


def print_moons(moons):
    """
    Print moons in a manner similar to the one in the problem.
    """
    for moon in moons:
        print_moon(moon)
    print()


def move_moons(moons):
    """
    Perform 1 step in moving the moons.
    """
    for first2, moon in enumerate(moons[:-1], start=1):
        for moon2 in moons[first2:]:
            for i in range(3):
                p1 = moon["p"][i]
                p2 = moon2["p"][i]
                if p1 < p2:
                    d = 1
                elif p1 > p2:
                    d = -1
                else:
                    continue
                moon["v"][i] += d
                moon2["v"][i] -= d
    for moon in moons:
        moon["p"] = [p + v for p, v in zip(moon["p"], moon["v"])]


def norm(vec):
    """
    Return the 1-norm of a vector.
    """
    return sum(abs(v) for v in vec)


def part1(moons, *, steps=1000, print_steps=None):
    """
    Return the solution for the part 1.

    :param moons: The current state of moons (a list, as returned by
        `lines2moons`).
    :param steps: Number of steps to perform.
    :param print_steps: A Boolean, defining which steps should be printed
        (every `print_steps`-th one should be). Nothing is printed if this is
        set to `None`.
    :return: Potential energy after `steps` steps.
    """
    moons = deepcopy(moons)
    for step in range(1, steps + 1):
        move_moons(moons)
        if print_steps and (step % print_steps == 0 or step == steps):
            print(f"After {step} steps:")
            print_moons(moons)
    return sum(norm(moon["p"]) * norm(moon["v"]) for moon in moons)


def _lcm(numbers):
    """
    Return the least common multiplier of a list of `int` values.
    """
    result = numbers[0]
    for number in numbers[1:]:
        result = result * number // gcd(result, number)
    return result


class Prophet:
    """
    Class to predict the solution to part 2.

    This is based on the observation that the three dimensions are completely
    independent. This means that we need to find out when do we get the repeat
    of the situation on each of those independently (so, in total 4 positions
    and 4 velocities). The number of steps that has passed is the period at
    which the situation on that dimension repeats. The final result is
    the least common multiplier of those three periods.
    """

    def __init__(self, initial):
        self._start = deepcopy(initial)
        self._history = [dict() for _ in range(3)]
        self._found = 3 * [None]

    @staticmethod
    def _key(moons, i):
        """
        Return the key for the `i`-th dimension of a state in history.
        """
        return tuple(moon[k][i] for k in "pv" for moon in moons)

    def prophecy(self, moons, step):
        """
        Return the prophecy for the current state of moons.

        :param moons: The current state of moons (a list, as returned by
            `lines2moons`).
        :param step: The step that the universe is currently on.
        """
        found = self._found
        for i in range(3):
            if found[i] is not None:
                continue
            key = self._key(moons, i)
            try:
                first = self._history[i][key]
            except KeyError:
                self._history[i][key] = step
            else:
                found[i] = step - first
        if all(f is not None for f in found):
            return _lcm(found)


def part2(moons):
    """
    Return the solution for the part 2.

    :param moons: The current state of moons (a list, as returned by
        `lines2moons`).
    """
    prophet = Prophet(moons)
    for step in itertools.count(1):
        move_moons(moons)
        prophecy = prophet.prophecy(moons, step)
        if prophecy is not None:
            return prophecy


def run_tests():
    """
    Test the above solutions.
    """
    print("Testing part 1...")
    for n, test in enumerate(_tests, start=1):
        moons = lines2moons(test["input"])
        for part in (1, 2):
            print(f"Running test {n} for part {part}...", end="")
            if part == 1:
                result = part1(moons, steps=test.get("steps", 1000))
            else:
                result = part2(moons)
            correct = test[f"part{part}"]
            if result == correct:
                print(" OK!")
            else:
                print(f" Failed ({result} != {correct})!")


if __name__ == "__main__":
    run_tests()
    moons = read_input()
    print("Part 1:", part1(moons))
    print("Part 2:", part2(moons))
