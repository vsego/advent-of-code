#!/usr/bin/env python3

test_cases = (
    (
        ("1122", 3), ("1111", 4), ("1234", 0), ("91212129", 9),
    ),
    (
        ("1212", 6), ("1221", 0), ("123425", 4), ("123123", 12),
        ("12131415", 4),
    ),
)

def solve(num, d=1):
    if d is None:
        d = len(num) // 2
    return sum(int(c1) for c1, c2 in zip(num, num[d:] + num[:d]) if c1 == c2)


for tid, tests in enumerate(test_cases, start=1):
    print("Test %d:" % tid)
    for test, test_res in tests:
        res = solve(test, (1 if tid == 1 else None))
        print("  Testing: %d == %d?" % (res, test_res))
        assert res == test_res

data = input()
print("Solutions:")
print("  Part 1:", solve(data))
print("  Part 2:", solve(data, None))
