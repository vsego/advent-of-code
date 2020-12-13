"""
Parent class for solutions.
"""

import sys


class AoCSolution:
    """
    Parent class for solutions.
    """

    tests = list()

    @classmethod
    def from_values(cls, *args, **kwargs):
        """
        Return a class instance initialised from arguments.
        """
        result = cls()
        result.init_from_values(*args, **kwargs)
        return result

    @classmethod
    def from_file(cls, fname):
        """
        Return a class instance initialised from the text file `fname`.
        """
        result = cls()
        with open(fname) as f:
            result.init_from_file(f)
        return result

    def init_from_values(self, *args, **kwargs):
        """
        Initialise the object from arguments.
        """
        raise NotImplementedError()

    def init_from_file(self, f):
        """
        Initialise the object from the text file `f`.
        """
        raise NotImplementedError()

    def part1(self):
        """
        Return the solution for part 1.
        """
        raise NotImplementedError()

    def part2(self):
        """
        Return the solution for part 2.
        """
        raise NotImplementedError()

    @classmethod
    def _run_test(cls, part, test_idx, expected, *args, **kwargs):
        """
        Return the solution for part 2.
        """
        print(f"Running test #{test_idx + 1} for part {part}...", end="")
        result = getattr(cls.from_values(*args, **kwargs), f"part{part}")()
        if result == expected:
            print(" Ok.")
        else:
            print(f" Failed, with {result} != {expected}.")

    @classmethod
    def run_tests(cls):
        for idx, test_data in enumerate(cls.tests):
            for part, expected in test_data["results"].items():
                cls._run_test(
                    part,
                    idx,
                    expected,
                    *test_data.get("args", list()),
                    **test_data.get("kwargs", dict()),
                )


def main(solution_class):
    try:
        fname = sys.argv[1]
    except IndexError:
        # Run tests.
        solution_class.run_tests()
    else:
        # Run the real thing.
        solution = solution_class.from_file(fname)
        print("Part 1:", solution.part1())
        try:
            print("Part 2:", solution.part2())
        except NotImplementedError:
            print("Part 2: <not implemented yet>")
