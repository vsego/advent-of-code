#!/usr/bin/env python3

import re
from sys import argv


class Cave:
    """
    Class that represents the cave in AoC 2018, day 22 problem.
    """

    def __init__(self, tx, ty, depth):
        self._mx = self.tx = tx
        self._my = self.ty = ty
        self.depth = depth
        self._map = dict()

    def __getitem__(self, pos):
        """
        Return details for the given position.

        If the data was not yet computed, compute it and cache it.

        :param pos: An `(x, y)` tuple of non-negative `int`s.
        :return: A `dict` with keys `erosion` and `risk`.
        """
        try:
            return self._map[pos]
        except KeyError:
            x, y = pos
            if x == self.tx and y == self.ty:
                geo = 0
            elif x == 0:
                geo = y * 48271
            elif y == 0:
                geo = x * 16807
            else:
                geo = (
                    self[(x - 1, y)]["erosion"]
                    * self[(x, y - 1)]["erosion"]
                )
            erosion = (geo + self.depth) % 20183
            self._map[(x, y)] = {
                "erosion": erosion, "risk": erosion % 3,
            }
            return self._map[pos]

    @classmethod
    def from_file(cls, fname):
        """
        Create and return a new instance of `Cave` based on a data in a file.

        :param fname: A string path to the file to be used. The file is
            expected to have the format `depth: <int>\ntarget: <int>,<int>`.
        :return: A `Cave` instance.
        """
        with open(fname, "rt") as f:
            m = re.match(
                r"depth: (?P<depth>\d+)\ntarget: (?P<tx>\d+),(?P<ty>\d+)",
                f.read(),
            )
            if m:
                return cls(
                    int(m.group("tx")),
                    int(m.group("ty")),
                    int(m.group("depth")),
                )
            raise ValueError("invalid file")

    @classmethod
    def from_argv(cls):
        """
        Create and return a new instance of `Cave` based on command line args.

        Determine which file to read from command line arguments, and create a
        new instance of `Cave` from it.

        :return: A `Cave` instance.
        """
        try:
            return cls.from_file(argv[1])
        except (IndexError, ValueError):
            return cls.from_file(argv[0].replace(".py", ".in"))

    def total_risk(self):
        """
        Return total risk (the answer for part 1).
        """
        return sum(
            self[(x, y)]["risk"]
            for x in range(self.tx + 1)
            for y in range(self.ty + 1)
        )

    def min_time(self):
        """
        Return minimal time needed to reach the target (the answer for part 2).
        """
        def d(x=0, y=0, item="t", time=0):
            return (
                time
                + abs(x - self.tx)
                + abs(y - self.ty)
                + 7 * int(item != "t")
            )
        equipment = [{"cg", "t"}, {"cg", "n"}, {"t", "n"}]
        target_pos = (self.tx, self.ty)
        last_visited = {d(): {(0, 0)}}
        times = {(0, 0): {"t": 0}}
        target_time = None
        while True:
            min_estimate = min(last_visited.keys())
            # print([max(v[k] for v in times.keys()) for k in (0, 1)])
            if target_time is not None and min_estimate >= target_time:
                break
            curr_pos = last_visited[min_estimate].pop()
            if not last_visited[min_estimate]:
                del last_visited[min_estimate]
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                x, y = new_pos = (curr_pos[0] + dx, curr_pos[1] + dy)
                if x < 0 or y < 0:
                    continue
                new_items = equipment[self[new_pos]["risk"]]
                for curr_item, curr_time in times[curr_pos].items():
                    curr_items = equipment[self[curr_pos]["risk"]]
                    new_time = curr_time + 1
                    if curr_item in new_items:
                        new_item = curr_item
                    else:
                        new_item = (new_items & curr_items).pop()
                        new_time += 7
                    if new_pos == target_pos and new_item != "t":
                        new_item = "t"
                        new_time += 7
                    try:
                        if new_time < times[new_pos][new_item]:
                            raise KeyError()
                    except KeyError:
                        times.setdefault(new_pos, dict())
                        times[new_pos][new_item] = new_time
                        lv_key = d(x, y, new_item, new_time)
                        try:
                            last_visited[lv_key].add(new_pos)
                        except KeyError:
                            last_visited[lv_key] = {new_pos}
                        if new_pos == target_pos:
                            new_tt = new_time
                            if target_time is None or new_tt < target_time:
                                target_time = new_tt
        return target_time


if __name__ == "__main__":
    cave = Cave.from_argv()
    print("Part 1:", cave.total_risk())
    print("Part 2:", cave.min_time())
