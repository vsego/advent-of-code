#!/usr/bin/python3


_tests = (
    {
        "wires": ("R8,U5,L5,D3", "U7,R6,D4,L4"),
        "part1": 6,
        "part2": 30,
    },
    {
        "wires": (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
        ),
        "part1": 159,
        "part2": 610,
    },
    {
        "wires": (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ),
        "part1": 135,
        "part2": 410,
    },
)


def str2wire(s):
    """
    Return wire from a string.

    :param s: One string defining a wire.
    :return: A wire, i.e., a list of 2-tuples of `int` values, representing the
        points where wires twist and turn (plus, obviously, the starting and
        the ending points).
    """
    point = (0, 0)
    wire = [point]
    for tt in s.strip().split(","):
        tt = tt.strip()
        direction = tt[0].lower()
        dist = int(tt[1:])
        if direction == "u":
            point = (point[0], point[1] - dist)
        elif direction == "r":
            point = (point[0] + dist, point[1])
        elif direction == "d":
            point = (point[0], point[1] + dist)
        elif direction == "l":
            point = (point[0] - dist, point[1])
        wire.append(point)
    return wire


def read_input(fname="day03.in"):
    """
    Read the input file and return the list of wires that it contains.

    :param fname: A string name of the file to read.
    :return: A list of wires.
    """
    result = list()
    with open(fname) as f:
        for line in f:
            result.append(str2wire(line))
        return result


def md(p1, p2):
    """
    Return Manhattan distance between two points.

    :param p1, p2: 2-tuples of `int` values, representing points.
    :return: An `int` value.
    """
    return sum(abs(v1 - v2) for v1, v2 in zip(p1, p2))


def mn(p):
    """
    Return Manhattan norm of a point.

    :param p: 2-tuple of `int` values, representing the point.
    :return: An `int` value.
    """
    return md((0, 0), p)


def find_intersection(c11, c12, c21, c22):
    """
    Return the intersection point of two chunks.

    :param c11, c12: 2-tuples of `int` values, representing the end points
        of the first chunk.
    :param c21, c22: 2-tuples of `int` values, representing the end points
        of the second chunk.
    :return: Either `None` or a 2-tuple of `int` values representing the
        intersection point..
    """
    if c11[0] == c12[0]:
        # c11-c12 is vertical
        y11 = min(c11[1], c12[1])
        y12 = max(c11[1], c12[1])
        if c21[0] == c22[0]:
            # c21-c22 is also vertical (they are parallel)
            if c11[0] == c21[0]:
                # parallel, but on the same line
                y21 = min(c21[1], c22[1])
                y22 = max(c21[1], c22[1])
                y1 = max(y11, y21)
                y2 = min(y12, y22)
                if y1 > y2:
                    return None
                elif y1 * y2 <= 0:
                    return (c11[0], 0)
                else:
                    return (c11[0], min(y1, y2, key=abs))
            else:
                # parallel, not touching
                return None
        else:
            # c21-c22 is not vertical (i.e., it is horizontal)
            x21 = min(c21[0], c22[0])
            x22 = max(c21[0], c22[0])
            if x21 <= c11[0] <= x22 and y11 <= c21[1] == c22[1] <= y12:
                return (c11[0], c21[1])
            else:
                return None
    else:
        # c11-c12 is not vertical (i.e., it is horizontal)
        assert c11[1] == c12[1]
        if c21[0] == c22[0]:
            # c21-c22 is vertical
            return find_intersection(c21, c22, c11, c12)
        else:
            # c21-c22 is not vertical (i.e., it is horizontal, so they are
            # parallel)
            assert c21[1] == c22[1]
            if c11[1] == c21[1]:
                # parallel, but on the same line
                x11 = min(c11[0], c12[0])
                x12 = max(c11[0], c12[0])
                x21 = min(c21[0], c22[0])
                x22 = max(c21[0], c22[0])
                x1 = max(x11, x21)
                x2 = min(x12, x22)
                if x1 > x2:
                    return None
                elif x1 * x2 <= 0:
                    return (0, c11[0])
                else:
                    return (min(x1, x2, key=abs), 0)
            else:
                # parallel, not touching
                return None


def part1(wire1, wire2):
    """
    Return the solution for part 1.
    """
    return min(
        mn(intersection)
        for intersection in (
            find_intersection(p1, p2, p3, p4)
            for p1, p2 in zip(wire1, wire1[1:])
            for p3, p4 in zip(wire2, wire2[1:])
            if any(p != (0, 0) for p in (p1, p3))
        )
        if intersection is not None
    )


def part2(wire1, wire2):
    """
    Return the solution for part 2.
    """
    return min(
        (
            sum(md(p1, p2) for p1, p2 in zip(wire1, wire1[1:i1]))
            + sum(md(p3, p4) for p3, p4 in zip(wire2, wire2[1:i2]))
            + md(wire1[i1 - 1], intersection)
            + md(wire2[i2 - 1], intersection)
        )
        for i1, i2, intersection in (
            (i1, i2, find_intersection(p1, p2, p3, p4))
            for i1, (p1, p2) in enumerate(zip(wire1, wire1[1:]), start=1)
            for i2, (p3, p4) in enumerate(zip(wire2, wire2[1:]), start=1)
            if any(p != (0, 0) for p in (p1, p3))
        )
        if intersection is not None
    )


def run_tests():
    """
    Run tests... d'oh.
    """
    for i, test in enumerate(_tests, start=1):
        print(f"Running test {i}...", end="")
        result1 = part1(*[str2wire(s) for s in test["wires"]])
        result2 = part2(*[str2wire(s) for s in test["wires"]])
        fails = list()
        if result1 != test["part1"]:
            fails.append(f"part 1 ({result1} != {test['part1']})")
        if result2 != test["part2"]:
            fails.append(f"part 2 ({result2} != {test['part2']})")
        if fails:
            print(f" failed: {' and '.join(fails)}")
        else:
            print(" OK!")


if __name__ == "__main__":
    run_tests()
    wires = read_input()
    print("Part 1:", part1(*wires))
    print("Part 2:", part2(*wires))
