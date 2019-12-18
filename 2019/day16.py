#!/usr/bin/env python3

_tests = [
    {
        "in": "12345678",
        "phases1": 4,
        "part1": "01029498",
    },
    {
        "in": "80871224585914546619083218645595",
        "part1": "24176176",
    },
    {
        "in": "19617804207202209144916044189917",
        "part1": "73745418",
    },
    {
        "in": "69317163492948606335995924319873",
        "part1": "52432133",
    },
    {
        "in": "03036732577212944063491565474664",
        "part2": "84462026",
    },
    {
        "in": "02935109699940807407585447034323",
        "part2": "78725270",
    },
    {
        "in": "03081770884921959731165446850517",
        "part2": "53553731",
    },
]


def line2ints(line):
    """
    Return a list of `int` digits contained in the string `line`.
    """
    return [int(d) for d in line.strip()]


def read_input(fname="day16.in"):
    """
    Read the input file and return .

    :param fname: A string name of the file to read.
    :return: A list of `int` digits read from the file.
    """
    with open(fname) as f:
        return line2ints(f.read())


def _one_pass(nums):
    """
    Return the result of one pass in processing the signal.
    """
    pattern = [0, 1, 0, -1]
    return [
        int(str(sum(
            v * pattern[(i // n) % len(pattern)]
            for i, v in enumerate(nums, start=1)
        ))[-1])
        for n in range(1, len(nums) + 1)
    ]


def part1(nums, steps=100):
    """
    Return the solution for part 1 as a string.
    """
    for _ in range(steps):
        nums = _one_pass(nums)
    return "".join(str(d) for d in nums[:8])


def part2(nums, steps=100):
    """
    Return the solution for part 2 as a string.

    As far as I can see, there is no "nice" solution, apart from abusing the
    fact that the offset puts us (both in tests and in the official input)
    in the second half of the list, where the rule is quite simple:
    1. The last number is never changed.
    2. Every previous number is the modulo 2 sum of its former self and its
       successor (the last computed number).
    The code below uses that in the `if` block, but also leaves the slow
    computing code for other offsets in the `else` block.
    """
    nums *= 10000
    offset = int("".join(str(d) for d in nums[:7]))
    if offset > len(nums) // 2:
        nums = nums[offset:]
        for _ in range(steps):
            for i, num in reversed(list(enumerate(nums[:-1]))):
                nums[i] = (num + nums[i + 1]) % 10
        return "".join(str(d) for d in nums[:8])
    else:
        for _ in range(steps):
            nums = _one_pass(nums)
        return "".join(str(d) for d in nums[offset:offset + 8])


def run_tests():
    """
    Run all the tests.
    """
    def print_result(result, correct):
        if result == correct:
            print(" OK!")
        else:
            print(f" Failed ({result} != {correct})!")
    for n, test in enumerate(_tests, start=1):
        print(f"Running test {n}...")
        nums = line2ints(test["in"])
        try:
            correct = test["part1"]
        except KeyError:
            pass
        else:
            print("  Testing part 1...", end="")
            result = part1(nums, steps=test.get("phases1", 100))
            print_result(result, correct)
        try:
            correct = test["part2"]
        except KeyError:
            pass
        else:
            print("  Testing part 2...", end="")
            result = part2(nums, steps=test.get("phases2", 100))
            print_result(result, correct)


if __name__ == "__main__":
    run_tests()
    inp = read_input()
    print("Part 1:", part1(inp))
    print("Part 2:", part2(inp))
