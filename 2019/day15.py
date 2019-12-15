#!/usr/bin/env python3

from intcode09 import Intcode, MissingInputError


def read_input(fname="day15.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


class Solver:
    """
    The solver class for day 15.
    """

    _moves = [None, (0, -1), (0, 1), (-1, 0), (1, 0)]
    reverse_moves = [None, 2, 1, 4, 3]
    _chars = {None: " ", 0: "\u2588", 1: ".", 2: "O"}

    def __init__(self, mem):
        self.inp = list()
        self.out = list()
        self.prog = Intcode(mem, self.inp, self.out)
        self._area = {(0, 0): 1}
        self.droid_pos = (0, 0)
        self.os_pos = None

    @staticmethod
    def _new_pos(pos, dpos):
        """
        Return the sum of two 2-tuples.

        :param pos, dpos: 2-tuples of numbers (intended as a position and
            delta-position, i.e., movement).
        :return: A 2-tuple os sums of corresponding coordinates in `pos` and
            `dpos` (i.e., the new position).
        """
        return tuple(p + d for p, d in zip(pos, dpos))

    def _new_droid_pos(self, cmd):
        """
        Return droid's potential new position after executing command `cmd`.

        This method only returns where the droid would have moved if given the
        instruction `cmd`. It doesn't check what's there, i.e., whether thes
        droid will actually move.

        :param cmd: Either 1, 2, 3, or 4.
        :return: A 2-tuple of `int` values.
        """
        return self._new_pos(self.droid_pos, self._moves[cmd])

    def execute_command(self, cmd):
        """
        Execute a command and return droid's response.

        :param cmd: Either 1, 2, 3, or 4.
        :return: Robot's response to the command `cmd`.
        """
        self.inp.append(cmd)
        try:
            self.prog.run()
        except MissingInputError:
            pass
        new_pos = self._new_droid_pos(cmd)
        response = self.out.pop(0)
        self._area[new_pos] = response
        if response in {1, 2}:
            self.droid_pos = new_pos
        return response

    def draw(self):
        """
        Draw the current state of the system.
        """
        minx, maxx, miny, maxy = tuple(
            f(coords[i] for coords in self._area.keys())
            for i in (0, 1)
            for f in (min, max)
        )
        for y in range(maxy, miny - 1, -1):
            print(
                "".join(
                    (
                        "\u263a"
                        if (x, y) == self.droid_pos else
                        self._chars[self._area.get((x, y))]
                    )
                    for x in range(minx, maxx + 1)
                )
            )

    def part1(self, way_back=None, dist=0):
        """
        Analyze the area and return the solution for part 1.

        :param way_back: A command to undo the last move. This is used to avoid
            making a new move in the direction from which the droid just came.
            In theory, the droid could still end up running in circles (as we
            don't keep the history of previous positions), but the area given
            in the problem has no spots where this could happen, so we're
            keeping it simple.
        :param dist: The current best `int` distance from the starting point.
        :return: The solution for part 1.
        """
        result = None
        dist += 1
        for cmd in range(1, 5):
            if cmd == way_back:
                continue
            response = self.execute(cmd)
            if response in {1, 2}:
                if response == 2:
                    result = dist
                    self.os_pos = self.droid_pos
                rd = self.reverse_moves[cmd]
                res = self.part1(rd, dist)
                if res is not None:
                    result = res
                self.execute(rd)
        return result

    def part2(self):
        """
        Return solution for part 2 (the longest distance from oxygen system).
        """
        dist = 0
        last_run = [self.os_pos]
        oxigenated = set(last_run)
        while True:
            new_run = list()
            for pos in last_run:
                for dpos in self._moves[1:]:
                    p = self._new_pos(pos, dpos)
                    if p not in oxigenated and self._area[p] == 1:
                        new_run.append(p)
            if not new_run:
                return dist
            oxigenated |= set(new_run)
            dist += 1
            last_run = new_run


def solve(mem):
    """
    Solve the problem, d'oh.
    """
    solver = Solver(mem)
    part1 = solver.part1()
    solver.draw()
    print("Part 1:", part1)
    print("Part 2:", solver.part2())


if __name__ == "__main__":
    solve(read_input())
