#!/usr/bin/python3


from intcode05 import Intcode


def read_input(fname="day05.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def run_prog(mem, inp=None, out=None):
    """
    Run the program.

    :param mem: A program (a `list` of `int` values).
    :raise ValueError: Raised if the program is invalid.
    """
    if out is not None:
        out[:] = list()
    prog = Intcode(mem, inp, out)
    prog.run()
    mem[:] = prog.mem


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


def test_run(prog, correct, inp=None):
    """
    Test if the program interpreter is running correctly.

    :param prog: A program (a `list` of `int` values).
    :param correct: A `list` containing the program as it should be after one
        run.
    """
    print(f"Testing [{prog2str(prog)}] (inp={inp})...", end="")
    out = list()
    run_prog(prog, inp, out)
    if (out and out == correct) or (not out and prog == correct):
        print(" OK!")
    else:
        fail_str = prog2str(out if out else prog)
        print(f" Failed: [{fail_str}] != [{prog2str(correct)}]!")


def solution(p, id_):
    """
    Solve part `p` of the puzzle for input `id_`.
    """
    out = list()
    run_prog(read_input(), [id_], out)
    print(f"Solution to part {p}: {out[-1]}")


if __name__ == "__main__":
    print("Testing...")
    test_run([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99])
    test_run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [1], [8])
    test_run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [0], [17])
    test_run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [1], [7])
    test_run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [0], [8])
    test_run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [1], [8])
    test_run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [0], [17])
    test_run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [1], [7])
    test_run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [0], [8])
    larger = [
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99,
    ]
    test_run(larger, [999], [7])
    test_run(larger, [1000], [8])
    test_run(larger, [1001], [9])
    solution(1, 1)
    solution(2, 5)
