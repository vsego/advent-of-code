#!/usr/bin/env python3

import os
from time import sleep

from intcode09 import Intcode, MissingInputError


def read_input(fname="day13.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def part1(mem):
    """
    Return the solution of part 1.
    """
    out = list()
    Intcode(mem, None, out).run()
    return sum(1 for tile_id in out[2::3] if tile_id == 2)


# Taken from https://stackoverflow.com/a/44740224/1667018 and modified
def reset_screen(clear=False, numlines=100):
    """
    Clear the console.

    :param numlines: An optional argument used only as a fall-back via printing
        that many empty lines.
    """
    # Thanks to Steven D'Aprano, http://www.velocityreviews.com/forums

    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        if clear:
            print("\033c", end="")
        else:
            print("\033[0;0H", end="")
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print("\n" * numlines)


class Analyzer:
    """
    Class for analyzing game's output.
    """

    t2c = {0: " ", 1: "\u2588", 2: "\u2591", 3: "\u2583", 4: "\u2022"}

    def __init__(self, *, draw_board=False):
        self.ball_pos = None
        self.pad_pos = None
        self.score = 0
        self.tiles = dict()
        self.draw_board = draw_board

    def analyze_output(self, out):
        """
        Analyze output.

        :param out: A list of `int` values containing the game's output.
        """
        for x, y, tile_id in zip(out[::3], out[1::3], out[2::3]):
            if self.draw_board:
                if (x, y) == (-1, 0):
                    self.score = tile_id
                    continue
                self.tiles[(x, y)] = tile_id
            if tile_id == 3:
                if self.pad_pos is not None:
                    self.tiles[self.pad_pos] = 0
                self.pad_pos = (x, y)
            elif tile_id == 4:
                if self.ball_pos is not None:
                    self.tiles[self.ball_pos] = 0
                self.ball_pos = (x, y)
        if self.draw_board:
            reset_screen()
            minx, maxx, miny, maxy = tuple(
                f(coords[i] for coords in self.tiles.keys())
                for i in (0, 1)
                for f in (min, max)
            )
            for y in range(miny, maxy + 1):
                for x in range(minx, maxx + 1):
                    print(self.t2c[self.tiles.get((x, y), 0)], end="")
                print()
            print("Score:", self.score)
            sleep(0.05)


def part2(mem, *, animate=False):
    """
    Return the solution of part 2.
    """
    mem = [2] + mem[1:]
    inp = list()
    out = list()
    analyzer = Analyzer(draw_board=animate)
    prog = Intcode(mem, inp, out)
    old_ball_x = None
    done = False
    if animate:
        reset_screen(True)
    while True:
        out[:] = list()
        try:
            prog.run()
        except MissingInputError:
            pass
        else:
            done = True
        analyzer.analyze_output(out)
        if done:
            return analyzer.score
        inp[:] = [0]
        if old_ball_x is not None:
            if old_ball_x < analyzer.ball_pos[0]:
                dx = 1
            else:
                dx = -1
            dx = 0
            if analyzer.pad_pos[0] < analyzer.ball_pos[0] + dx:
                inp[:] = [1]
            elif analyzer.pad_pos[0] > analyzer.ball_pos[0] + dx:
                inp[:] = [-1]
        old_ball_x = analyzer.ball_pos[0]


if __name__ == "__main__":
    mem = read_input()
    res1 = part1(mem)
    res2 = part2(mem, animate=True)
    print()
    print("Part 1:", res1)
    print("Part 2:", res2)
