#!/usr/bin/env python3

import re


_tests = (
    {
        "in": [
            "9 ORE => 2 A",
            "8 ORE => 3 B",
            "7 ORE => 5 C",
            "3 A, 4 B => 1 AB",
            "5 B, 7 C => 1 BC",
            "4 C, 1 A => 1 CA",
            "2 AB, 3 BC, 4 CA => 1 FUEL",
        ],
        "part1": 165,
    },
    {
        "in": [
            "157 ORE => 5 NZVS",
            "165 ORE => 6 DCFZ",
            "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
            "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
            "179 ORE => 7 PSHF",
            "177 ORE => 5 HKGWZ",
            "7 DCFZ, 7 PSHF => 2 XJWVT",
            "165 ORE => 2 GPVTF",
            "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
        ],
        "part1": 13312,
        "part2": 82892753,
    },
    {
        "in": [
            "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
            "17 NVRVD, 3 JNWZP => 8 VPVL",
            "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
            "22 VJHF, 37 MNCFX => 5 FWMGM",
            "139 ORE => 4 NVRVD",
            "144 ORE => 7 JNWZP",
            "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
            "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
            "145 ORE => 6 MNCFX",
            "1 NVRVD => 8 CXFTF",
            "1 VJHF, 6 MNCFX => 4 RFSQX",
            "176 ORE => 6 VJHF",
        ],
        "part1": 180697,
        "part2": 5586022,
    },
    {
        "in": [
            "171 ORE => 8 CNZTR",
            "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP =>"
            " 4 PLWSL",
            "114 ORE => 4 BHXH",
            "14 VRPVC => 6 BMBT",
            "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
            "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP =>"
            " 6 FHTLT",
            "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
            "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
            "5 BMBT => 4 WPTQ",
            "189 ORE => 9 KTJDG",
            "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
            "12 VRPVC, 27 CNZTR => 2 XDBXC",
            "15 KTJDG, 12 BHXH => 5 XCVML",
            "3 BHXH, 2 VRPVC => 7 MZWV",
            "121 ORE => 7 VRPVC",
            "7 XCVML => 6 RJRHP",
            "5 BHXH, 4 VRPVC => 5 LTCX",
        ],
        "part1": 2210736,
        "part2": 460664,
    },
)


def _str2ingredient(s):
    """
    Parse one quantity/ingredient string and return it as a parsed tuple.

    :param s: A string of the form `"<quantity:int> <name:str>"`.
    :return: The components of `s` as a `(name, quantity)` tuple.
    """
    m = re.match(r"(?P<quantity>\d+)\s+(?P<name>\w+)$", s)
    if m:
        return (m.group("name"), int(m.group("quantity")))
    else:
        raise ValueError(f"{repr(s)} is not a valid ingredient")


def lines2recipe(lines):
    """
    Return recipe from a list of lines.

    :param lines: A list of strings describing the recipe.
    :return: A `dict` associating ingredients' names with their instruction,
        which is a `dict` containing keys `"in"` (a dictionary associating
        needed ingredients' names with the required quantities) and `"q"` (an
        `int` value containing the produced quantity).
    """
    result = dict()
    for line in lines:
        inp, out = line.strip().split(" => ")
        name, quantity = _str2ingredient(out)
        result[name] = {
            "in": dict(_str2ingredient(v) for v in re.split(r",\s*", inp)),
            "q": quantity,
        }
    return result


def read_input(fname="day14.in"):
    """
    Read the input file and return .

    :param fname: A string name of the file to read.
    :return: A `dict` associating ingredients' names with their instruction,
        which is a `dict` containing keys `"in"` (a dictionary associating
        needed ingredients' names with the required quantities) and `"q"` (an
        `int` value containing the produced quantity).
    """
    with open(fname) as f:
        return lines2recipe(f.readlines())


def _correct_quantity(surplus, name, quantity):
    """
    Return the correct quantity with surplus taken into account and updated.

    If `quantity` of `name` is required, but we already have some surplus of it
    from a previous reaction, then quantity can be reduced. Updating surplus,
    we may
    1. use it all up, in which case `name` is deleted from `surplus`;
    2. end up with still having some (while `quantity` drops to zero), in which
       case `surplus[name]` is updated to the new value.

    :param surplus: A `dict` associating ingredients' names with quantities
        left over from the already performed reactions.
    :param name: A string name of the ingredient.
    :param quantity: An `int` quantity required for this ingredient.
    :return: The corrected quantity.
    """
    try:
        have_quant = surplus.get(name, 0)
    except KeyError:
        pass
    else:
        if have_quant >= quantity:
            have_quant -= quantity
            if have_quant:
                surplus[name] = have_quant
        else:
            quantity -= have_quant
    return quantity


def _get_sorted_names(recipe):
    """
    Return a sorted list of ingredients' names.

    This is the core of the greedy algorithm in part 1. The names are sorted in
    such order that each of the ingredients is produced only by those after it.
    That way, when we use the ingredients in that order, we know that later
    reactions will not produce any surplus of an already used ingredient. This
    is crucial, because any reaction using some ingredient could use any
    surplus of that ingredient, so this approach avoids leftovers.

    :param recipe: A `dict` associating ingredients' names with their
        instruction, which is a `dict` containing keys `"in"` (a dictionary
        associating needed ingredients' names with the required quantities) and
        `"q"` (an `int` value containing the produced quantity).
    :return: A sorted list of ingredients' names.
    """
    result = ["ORE"]
    last_found = result[:]
    while last_found:
        new_found = list()
        for name in recipe:
            if name in result:
                continue
            if all(n in result for n in recipe[name]["in"]):
                new_found.append(name)
                result.insert(0, name)
        last_found = new_found
    return result


def part1(recipe, aim=1):
    """
    Return the solution for part 1.

    The algorithm is roughly:
    1. Take the ingredients in proper order (see `_get_sorted_names` for more
       details).
    2. Compute the required quantity.
    3. Correct this quantity with regards to old surplus of it (see
       `_correct_quantity` for more details).
    4. Add the required ingredients with correct needed quantities to the list
       of those we still need to produce.
    5. Keep repeating as long as there is anything but "ORE" in the list of
       those still needed.

    :param recipe: A `dict` associating ingredients' names with their
        instruction, which is a `dict` containing keys `"in"` (a dictionary
        associating needed ingredients' names with the required quantities) and
        `"q"` (an `int` value containing the produced quantity).
    :param aim: An `int` saying how much fuel needs to be produced.
    :return: The `int` amount of ore required for `aim` units of fuel.
    """
    needed = {"ORE": 0, "FUEL": aim}
    surplus = dict()
    sorted_names = _get_sorted_names(recipe)
    while len(needed) > 1:
        name = next(n for n in sorted_names if n != "ORE" and n in needed)
        quantity = needed.pop(name)
        quantity = _correct_quantity(surplus, name, quantity)
        instruction = recipe[name]
        mult = (quantity - 1) // instruction["q"] + 1
        for n, q in instruction["in"].items():
            q = _correct_quantity(surplus, n, q * mult)
            if q:
                needed[n] = needed.get(n, 0) + q
    return needed["ORE"]


def part2(recipe):
    """
    Return the solution for part 2.

    This is a basic greedy algorithm:
    1. Compute fuel/ore naively. This'll be too small as it ignores all the
       surplus.
    2. Recompute, aiming to get just 1 unit more than the current "price"
       suggests. This'll usually produce the fuel for less ore than expected.
    3. Repeat 2 until it gets too big total price (i.e., more than 1T of ore).
       Since one less is possible (as it was based on a previously obtained
       "price"), and the current amount is too pricey, the final solution is
       what we requested minus one.

    The algorithm converges to the solution quickly (3 steps for the input),
    because in each step it uses all of the unaccounted surplus from previous
    steps (the ore that gave ingredients unused for fuel).

    :param recipe: A `dict` associating ingredients' names with their
        instruction, which is a `dict` containing keys `"in"` (a dictionary
        associating needed ingredients' names with the required quantities) and
        `"q"` (an `int` value containing the produced quantity).
    :return: The max amount of fuel that can be obtained from a trillion units
        of ore.
    """
    ore_quantity = part1(recipe)
    result = 1000000000000 // ore_quantity
    while True:
        ore_quantity = part1(recipe, result)
        if ore_quantity > 1000000000000:
            return result - 1
        result = result * 1000000000000 // ore_quantity + 1


def run_tests():
    """
    Run tests.
    """
    def print_result(result, correct):
        if result == correct:
            print(" OK!")
        else:
            print(f" Failed ({result} != {correct})!")
    for i, test in enumerate(_tests, start=1):
        print(f"Running test {i}...")
        print("  Testing part 1...", end="")
        recipe = lines2recipe(test["in"])
        print_result(part1(recipe), test["part1"])
        try:
            correct = test["part2"]
        except KeyError:
            pass
        else:
            print("  Testing part 2...", end="")
            print_result(part2(recipe), correct)


if __name__ == "__main__":
    run_tests()
    recipe = read_input()
    print("Part 1:", part1(recipe))
    print("Part 2:", part2(recipe))
