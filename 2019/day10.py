#!/usr/bin/python3

import math


_tests = [
    {
        "input": (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##",
        ),
        "part1": 8,
    },
    {
        "input": (
            "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####",
        ),
        "part1": 33,
    },
    {
        "input": (
            "#.#...#.#.",
            ".###....#.",
            ".#....#...",
            "##.#.#.#.#",
            "....#.#.#.",
            ".##..###.#",
            "..#...##..",
            "..##....##",
            "......#...",
            ".####.###.",
        ),
        "part1": 35,
    },
    {
        "input": (
            ".#..#..###",
            "####.###.#",
            "....###.#.",
            "..###.##.#",
            "##.##.#.#.",
            "....###..#",
            "..#.#..#.#",
            "#..#.#.###",
            ".##...##.#",
            ".....#.#..",
        ),
        "part1": 41,
    },
    {
        "input": (
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##",
        ),
        "part1": 210,
        "part2": 802,
    },
]


def lines2map(lines):
    """
    Return the asteroid map contained in list of strings.

    :param lines: A list of strings from the map.
    :return: A `list` of `(x, y)` tuples (a `set` would make more sense, but
        we'll need to iterate through this).
    """
    result = list()
    for y, line in enumerate(lines):
        line = line.strip()
        result.extend(
            (x, y) for x, spot in enumerate(line) if spot == "#"
        )
    return result


def read_input(fname="day10.in"):
    """
    Read the input file and return the asteroid map that it contains.

    :param fname: A string name of the file to read.
    :return: A `dict` with fields `width` (an `int`), `height` (and `int`) and
        `map` (a `set` of `(x, y)` tuples).
    """
    with open(fname) as f:
        return lines2map(f.readlines())


def _not_hidden(a, b, c):
    """
    Return `True` if either `b` is not hidden from `a` by `c`.
    """
    if (a[0] - b[0]) * (a[1] - c[1]) != (a[0] - c[0]) * (a[1] - b[1]):
        # `a`, `b`, and `c` are not colinear
        return True
    for idx in (0, 1):
        if (a[idx] < b[idx]) != (a[idx] < c[idx]):
            # `b` and `c` are on the opposite sides of `a`
            return True
    return False


def _count_visible(asteroids, asteroid):
    """
    Return how many `asteroids` is visible from `asteroid`.
    """
    return sum(
        1
        for first3, asteroid2 in enumerate(asteroids, start=1)
        if asteroid2 != asteroid and all(
            _not_hidden(asteroid, asteroid2, asteroid3)
            for asteroid3 in asteroids[first3:]
            if asteroid3 not in {asteroid, asteroid2}
        )
    )


def _make_polar_map(asteroid, asteroids):
    """
    Return asteroids arranged in a sorted list of sorted lists.

    :param asteroid: A 2-tuple containing the location of the reference
        asteroid (the one from which we observe all the others).
    :param asteroids: A list of asteroids, as returned by `lines2map`.
    :return: A list of lists of asteroids. Each sublist contains asteroids in
        the same line of sight from `asteroid`, sorted by their distance. The
        outer list is sorted by the angle (0 = upwards).
    """
    polar_map = dict()
    for asteroid2 in asteroids:
        if asteroid2 == asteroid:
            continue
        d = tuple(reversed([v1 - v2 for v1, v2 in zip(asteroid, asteroid2)]))
        gcd = math.gcd(*d)
        d = tuple(v // gcd for v in d)
        polar_map.setdefault(d, list()).append((gcd, asteroid2))
    return [
        line_of_sight
        for angle, line_of_sight in sorted(
            (
                (math.atan2(*d) + 3 * math.pi / 2) % (2 * math.pi),
                [asteroid for gcd, asteroid in sorted(line_of_sight)],
            )
            for d, line_of_sight in polar_map.items()
        )
    ]


def solve(asteroids):
    """
    Solve both parts of the problem.

    :param asteroids: A list of asteroids, as returned by `lines2map`.
    :return: A tuple of solutions for parts 1 and 2.
    """
    # Part 1
    cnt, asteroid = max(
        (_count_visible(asteroids, asteroid), asteroid)
        for asteroid in asteroids
    )

    # Part 2
    polar_map = _make_polar_map(asteroid, asteroids)
    left_to_kill = 199
    while polar_map and len(polar_map) <= left_to_kill:
        left_to_kill -= len(polar_map)
        for line_of_sight in polar_map:
            line_of_sight.pop(0)
        polar_map = [
            line_of_sight for line_of_sight in polar_map if line_of_sight
        ]
    try:
        asteroid_200 = polar_map[left_to_kill][0]
    except IndexError:
        which_asteroid = None
    else:
        which_asteroid = 100 * asteroid_200[0] + asteroid_200[1]

    return cnt, which_asteroid


def run_tests():
    """
    Run all the tests.
    """
    for i, test in enumerate(_tests, start=1):
        print(f"Running test #{i}...", end="")
        result = solve(lines2map(test["input"]))
        errors = list()
        if result[0] != test["part1"]:
            errors.append(f"  Part 1 failed ({result[0]} != {test['part1']})!")
        try:
            part2_correct = test["part2"]
        except KeyError:
            pass
        else:
            if result[1] != part2_correct:
                errors.append(
                    f"  Part 2 failed ({result[1]} != {test['part2']})!",
                )
        if errors:
            errors_str = "\n".join(errors)
            print(f"\n{errors_str}")
        else:
            print(" OK!")


if __name__ == "__main__":
    run_tests()
    asteroids = read_input()
    for part, sol in enumerate(solve(asteroids), start=1):
        print(f"Part {part}:", sol)
