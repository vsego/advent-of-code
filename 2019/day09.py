#!/usr/bin/python3


from intcode09 import Intcode


def read_input(fname="day09.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def run_prog(mem, inp=None):
    """
    Run the program.

    :param mem: A program (a `list` of `int` values).
    :param phase: The phase for the amplifier.
    :param inp: A single `int` input for the amplifier.
    :raise ValueError: Raised if the program is invalid.
    :return: A single `int` output from the amplifier.
    """
    out = list()
    prog = Intcode(mem[:], inp, out)
    prog.run()
    return out


def solve(mem):
    """
    Solve the puzzle.

    :param mem: A program (a `list` of `int` values).
    """
    for part in (1, 2):
        print(f"Part {part}: {run_prog(mem, [part])[-1]}")


def run_tests():
    """
    Test the solution.

    :param mem: A program (a `list` of `int` values).
    """
    def print_result(is_ok, error_msg):
        if is_ok:
            print(" OK!")
        else:
            print(f" Failed: [{error_msg}]!")
    print(f"Testing Intcode...")

    print("Running test 1...", end="")
    mem = [
        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0,
        99,
    ]
    out = run_prog(mem)
    print_result(out == mem, f"{out} != {mem}")

    print("Running test 2...", end="")
    mem = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    out = run_prog(mem)
    print_result(1e15 <= out[0] < 1e16, f"len(\"{out[0]}\") != 16")

    print("Running test 3...", end="")
    large = 1125899906842624
    mem = [104, large, 99]
    out = run_prog(mem)
    print_result(out[0] == large, f"{out[0]} != {large}")


if __name__ == "__main__":
    run_tests()
    solve(read_input())
