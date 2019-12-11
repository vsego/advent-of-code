#!/usr/bin/python3

import itertools

from intcode09 import Intcode, MissingInputError


def read_input(fname="day11.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def paint_panels(mem, init_col):
    """
    Pain the panels.

    :param mem: A program (a `list` of `int` values).
    :param init_col: The initial color of the first panel.
    :return: Painted panels, as a `dict` associating `(x, y)` positions to
        their colors.
    """
    result = dict()
    inp = list()
    out = list()
    prog = Intcode(mem[:], inp, out)

    # Directions
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    # Direction index (i.e., index in `dirs`)
    di = 0
    # Current position
    pos = (0, 0)

    for i in itertools.count(0):
        inp.append(result.get(pos, 0 if i else init_col))
        try:
            prog.run()
        except MissingInputError:
            pass
        else:
            break
        finally:
            result[pos] = out.pop(0)
            di = (di - 1 + 2 * out.pop(0)) % len(dirs)
            pos = tuple(p + d for p, d in zip(pos, dirs[di]))
    return result


def part1(mem):
    """
    Solve part 1 of the puzzle for the given program.
    """
    return len(paint_panels(mem, 0))


def part2(mem):
    """
    Solve part 2 of the puzzle for the given program.
    """
    panels = paint_panels(mem, 1)
    min_x, min_y, max_x, max_y = tuple(
        f(k[i] for k in panels.keys()) for f in (min, max) for i in (0, 1)
    )
    drawing = [[" "] * (max_x - min_x + 1) for _ in range(min_y, max_y + 1)]
    for (x, y), col in panels.items():
        if col:
            drawing[y][x] = "\u2588"
    return "\n".join(f"  {''.join(line)}" for line in drawing)


if __name__ == "__main__":
    mem = read_input()
    print("Part 1:", part1(mem))
    print("Part 2:", part2(mem), sep="\n")
