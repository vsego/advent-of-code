#!/usr/bin/python3

import re


def read_input(fname="day04.in"):
    """
    Read the input file and return a tuple of `int` value.

    :param fname: A string name of the file to read.
    :return: A tuple `(low, high)`.
    """
    with open(fname) as f:
        m = re.match(r"^\s*(?P<low>\d{6})\s*-\s*(?P<high>\d{6})\s*$", next(f))
    if m:
        return tuple(int(m.group(name)) for name in ("low", "high"))
    else:
        raise ValueError("invalid file content")


def passwd_ok(part, passwd):
    """
    Return `True` if `passwd` is ok; otherwise, return `False`.

    :param part: Which part of the problem is this for?
    :param passwd: Password to check.
    """
    passwd_str = str(passwd)
    if list(passwd_str) != sorted(passwd_str):
        return False
    if part == 2:
        passwd_str = re.sub(r"(\d)\1{2,}", "", passwd_str)
    if all(d1 != d2 for d1, d2 in zip(passwd_str, passwd_str[1:])):
        return False
    return True


def solve(part, low, high):
    """
    Return the number of possible passwords between `low` and `high`.

    Lazy algorithm: just check them all.

    :param part: Which part of the problem is this for?
    :param low, high: `int` values denoting the low and the high bound.
    :return: The number of possible passwords between `low` and `high`
        (an `int` value).
    """
    return sum(1 for passwd in range(low, high + 1) if passwd_ok(part, passwd))


def test_passwd_ok(part, passwd, correct):
    """
    Test `passwd_ok`.

    :param part: Which part of the problem is this for?
    :param passwd: Password to test for.
    :param correct: The correct (expected) result.
    """
    print(f"Testing passwd_ok({passwd})...", end="")
    if passwd_ok(part, passwd) is correct:
        print(" OK!")
    else:
        print(" Whoopsie! \U0001F622")


def run_tests():
    """
    Run all tests.
    """
    print("Testing part 1...")
    test_passwd_ok(1, 111111, True)
    test_passwd_ok(1, 223450, False)
    test_passwd_ok(1, 123789, False)
    print("Testing part 2...")
    test_passwd_ok(2, 112233, True)
    test_passwd_ok(2, 123444, False)
    test_passwd_ok(2, 111122, True)


if __name__ == "__main__":
    run_tests()
    low, high = read_input()
    print("Part 1:", solve(1, low, high))
    print("Part 2:", solve(2, low, high))
