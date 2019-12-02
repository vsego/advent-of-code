#!/usr/bin/python3


def read_input(fname="day02.in"):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: A list of `int` values contained in the firs line of the file
        (comma-separated).
    """
    with open(fname) as f:
        return [int(v.strip()) for v in next(f).split(",")]


def run_prog(prog):
    """
    Run the program.

    :param prog: A program (a `list` of `int` values).
    :raise ValueError: Raised if the program is invalid.
    """
    p = 0
    while prog[p] != 99:
        try:
            v1 = prog[prog[p + 1]]
            v2 = prog[prog[p + 2]]
            pr = prog[p + 3]
            assert 0 <= pr < len(prog)
        except IndexError:
            raise ValueError(f"encountered invalid variable position")
        except AssertionError:
            raise ValueError("encountered invalid variable position {pr}")
        if prog[p] == 1:
            prog[pr] = v1 + v2
        elif prog[p] == 2:
            prog[pr] = v1 * v2
        else:
            raise ValueError(f"encountered invalid instruction {p}")
        p += 4
        if p >= len(prog):
            raise ValueError("unexpected end of program")


def prog2str(prog):
    """
    Return program as string.

    :param prog: A program (a `list` of `int` values).
    :return: A string containing the program.
    """
    return ",".join(str(v) for v in prog)


def test_run(prog, correct):
    """
    Test if the program interpreter is running correctly.

    :param prog: A program (a `list` of `int` values).
    :param correct: A `list` containing the program as it should be after one
        run.
    """
    print(f"Testing [{prog2str(prog)}]...", end="")
    run_prog(prog)
    if prog == correct:
        print(" OK!")
    else:
        print(f" Failed: [{prog2str(prog)}] != [{prog2str(correct)}]!")


def part1():
    """
    Solve part 1 of the puzzle.
    """
    prog = read_input()
    prog[1:3] = [12, 2]
    run_prog(prog)
    print("Solution to part 1:", prog[0])


def part2():
    """
    Solve part 2 of the puzzle.
    """
    prog = read_input()
    indices = list(range(0, len(prog)))
    for noun in indices:
        for verb in indices:
            prog_tmp = prog[:]
            prog_tmp[1] = noun
            prog_tmp[2] = verb
            run_prog(prog_tmp)
            if prog_tmp[0] == 19690720:
                print("Solution to part 2:", 100 * noun + verb)
                return
    print("Part 2 has no solution (or, more likely, I've messed up).")


if __name__ == "__main__":
    print("Testing...")
    test_run([1, 0, 0, 0, 99],  [2, 0, 0, 0, 99])
    test_run([2, 3, 0, 3, 99],  [2, 3, 0, 6, 99])
    test_run([2, 4, 4, 5, 99, 0],  [2, 4, 4, 5, 99, 9801])
    test_run([1, 1, 1, 4, 99, 5, 6, 0, 99],  [30, 1, 1, 4, 2, 5, 6, 0, 99])
    part1()
    part2()
