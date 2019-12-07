#!/usr/bin/python3


def lines2graph(lines):
    """
    Return a graph representing the given list of orbits.

    :param lines: A list of lines describing orbits.
    :return: A `dict` of nodes, each associated with the list of the object
        orbiting it directly.
    """
    orbits = [line.strip().split(")") for line in lines]
    result = {orbit[i]: list() for orbit in orbits for i in (0, 1)}
    trace_from = {"COM"}
    while trace_from:
        new_trace_from = set()
        for center, orbiter in orbits:
            # Not checking if we already traced center, as that would imply
            # a loop (illegal case which would lead to an infinite loop)
            if center in trace_from:
                result[center].append(orbiter)
                new_trace_from.add(orbiter)
        trace_from = new_trace_from
    return result


def read_input(fname="day06.in"):
    """
    Read the input file and return the graph of orbits.

    :param fname: A string name of the file to read.
    :return: A `dict` of nodes, each associated with the list of the object
        orbiting it directly.
    """
    with open(fname) as f:
        return lines2graph(f.readlines())


def analyze(graph, paths=None, node="COM", depth=0, path=None):
    """
    Analyze a graph.

    :param graph: The graph to analyze, as returned by `lines2graph`.
    :param paths: A dictionary in which to store
    """
    result = depth
    depth += 1
    if path is None:
        path = list()
    path.append(node)
    for child in graph[node]:
        paths[child] = path[:]
        result += analyze(graph, paths, child, depth, path)
    path.pop()
    return result


def solve(graph):
    """
    Return solutions for both parts as a 2-tuple of `int` values.
    """
    paths = dict()
    checksum = analyze(graph, paths)
    try:
        path1 = paths["YOU"]
        path2 = paths["SAN"]
    except KeyError:
        dist = -1
    else:
        idx = next(
            idx
            for idx, (cent1, cent2) in enumerate(zip(path1, path2))
            if cent1 != cent2
        )
        dist = len(path1) + len(path2) - 2 * idx
    return checksum, dist


def run_tests():
    """
    Run test examples from the problem text.
    """
    graph = lines2graph([
        "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K",
        "K)L",
    ])
    print("Analyzing graph 1 to test part 1...", end="")
    part1, _ = solve(graph)
    if part1 == 42:
        print(" OK!")
    else:
        print(f" Failed: {part1} != 42.")
    graph = lines2graph([
        "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K",
        "K)L", "K)YOU", "I)SAN",
    ])
    print("Analyzing graph 2 to test part 2...", end="")
    _, part2 = solve(graph)
    if part2 == 4:
        print(" OK!")
    else:
        print(f" Failed: {part2} != 4.")


if __name__ == "__main__":
    run_tests()
    part1, part2 = solve(read_input())
    print("Part 1:", part1)
    print("Part 2:", part2)
