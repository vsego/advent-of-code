#!/usr/bin/python3


import itertools

from intcode07 import Intcode, MissingInputError


def read_input(fname="day07.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def run_prog(mem, phase, inp):
    """
    Run the program.

    :param mem: A program (a `list` of `int` values).
    :param phase: The phase for the amplifier.
    :param inp: A single `int` input for the amplifier.
    :raise ValueError: Raised if the program is invalid.
    :return: A single `int` output from the amplifier.
    """
    out = list()
    prog = Intcode(mem[:], [phase, inp], out)
    prog.run()
    return out[0]


def prog2str(prog):
    """
    Return program as string.

    :param prog: A program (a `list` of `int` values).
    :return: A string containing the program.
    """
    if len(prog) >= 7:
        return f"{prog2str(prog[:3])},...,{prog2str(prog[-3:])}"
    else:
        return ",".join(str(v) for v in prog)


def _parallel_run_for_phases(mem, phases):
    """
    Run the program in parallel for a given list of phases.

    :param mem: A program (a `list` of `int` values).
    :param phase: A list of phases for the amplifiers.
    :return: A single `int` (the final output of the last amplifier).
    """
    inputs = [[phase] for phase in phases]
    amplifiers = [
        Intcode(mem[:], inp, out)
        for inp, out in zip(inputs, inputs[1:] + inputs[:1])
    ]
    inputs[0].append(0)
    done = False
    while not done:
        if not inputs[0]:
            # Ended with no input, so... an invalid configuration?
            # It doesn't seem to happen, but I prefer it to be fail-safe.
            return -1
        for amplifier in amplifiers:
            try:
                amplifier.run()
            except MissingInputError:
                pass
            else:
                # When one is done, there is no sense in rerunning any of them
                done = True
    return inputs[0][-1]


def solve(part, mem):
    """
    Solve part `part` of the puzzle.

    :param mem: A program (a `list` of `int` values).
    """
    phases = {1: range(5), 2: range(5, 10)}[part]
    return max(
        _parallel_run_for_phases(mem, phases)
        for phases in itertools.permutations(phases)
    )


def run_test(part, mem, correct):
    """
    Test the solution.

    :param mem: A program (a `list` of `int` values).
    """
    print(f"Testing [{prog2str(mem)}]...", end="")
    out = solve(part, mem)
    if out == correct:
        print(" OK!")
    else:
        print(f" Failed: [{out}] != [{correct}]!")


if __name__ == "__main__":
    print("Testing part 1...")
    run_test(
        1,
        [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
        43210,
    )
    run_test(
        1,
        [
            3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23,
            1, 24, 23, 23, 4, 23, 99, 0, 0,
        ],
        54321,
    )
    run_test(
        1,
        [
            3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
            1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0,
        ],
        65210,
    )
    print("Testing part 2...")
    run_test(
        2,
        [
            3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4,
            27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5,
        ],
        139629729,
    )
    run_test(
        2,
        [
            3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
            1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008,
            54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56,
            1005, 56, 6, 99, 0, 0, 0, 0, 10,
        ],
        18216,
    )
    prog = read_input()
    print("Part 1:", solve(1, prog))
    print("Part 2:", solve(2, prog))
