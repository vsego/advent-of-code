public static void clearScreen() {
    // From https://stackoverflow.com/a/40041221/1667018
    System.out.print("\033\143");
}

def load_map(fname) {
    def map = []
    def units = []
    File fp = new File(fname)
    def lines = fp.readLines()
    lines.eachWithIndex { line, y ->
        map << line.collect { c -> c }.indexed().collect { x, c ->
            if ( c == "G" || c == "E" ) {
                units << [type: c, hp: 200, x: x, y: y]
            }
            c
        }
    }
    return [map, units]
}

def find_origin(visited, pos) {
    while (visited[pos[1]][pos[0]]["dist"] > 1) {
        pos = visited[pos[1]][pos[0]]["prev"]
    }
    return pos
}

def enemies(type1, type2) {
    return (type1 == "E" && type2 == "G") || (type1 == "G" && type2 == "E")
}

def pos2unit(units, x, y) {
    return units.find { unit -> unit["x"] == x && unit["y"] == y }
}

def find_closest(map, origin, targets) {
    def default_dist = map.size() + map[0].size() - 1;
    def visited = []
    map.size().times { y ->
        visited[y] = []
        map[y].size().times { x ->
            visited[y][x] = [dist: default_dist, prev: null]
        }
    }
    visited[origin[1]][origin[0]]["dist"] = 0
    def found = []
    def last_visited = [ [origin[0], origin[1]] ]
    def dist = 0
    while (last_visited && !found) {
        dist++
        def new_visited = [];
        last_visited.each { x, y ->
            [ [0, -1], [-1, 0], [1, 0], [0, 1] ].each { dx, dy ->
                def nx = x + dx
                def ny = y + dy
                if (targets.contains([nx, ny])) {
                    found << [x, y]
                } else if (
                    ".*".contains(map[ny][nx])
                    && dist < visited[ny][nx]["dist"]
                ) {
                    visited[ny][nx] = [dist: dist, prev: [x, y]]
                    new_visited << [nx, ny]
                }
            }
        }
        last_visited = new_visited
    }
    if (dist <= 1) return null;
    found.sort { a, b -> a[1] - b[1] ?: a[0] - b[0] }
    return found[0]
}

def enemy_type(unit) {
    return (unit["type"] == "E" ? "G" : "E");
}

def move_towards_closest(map, units, unit) {
    def enemy_type = enemy_type(unit)
    def enemies_pos = units.findAll { unit2 ->
        unit2["type"] == enemy_type && unit2["hp"] > 0
    }.collect { enemy ->
        [enemy["x"], enemy["y"]]
    }
    def ox = unit["x"], oy = unit["y"]
    target = find_closest(map, [ox, oy], enemies_pos)
    if (target) {
        next_field = find_closest(map, target, [ [ox, oy] ])
        if (!next_field) next_field = target
        map[oy][ox] = "."
        unit["x"] = next_field[0]
        unit["y"] = next_field[1]
        map[unit["y"]][unit["x"]] = unit["type"]
    }
}

def solve(elf_power) {
    (map, units) = load_map(args ? args[0] : "day15.in")
    def part = (elf_power == 3 ? 1 : 2)
    def elf_dead = false
    def full_rounds = 0
    while (true) {
        units.sort { a, b -> a["y"] - b["y"] ?: a["x"] - b["x"] }
        def done = units.find { unit ->
            if (unit["hp"] > 0) {
                if (!units.find{ unit2 ->
                    unit2["type"] != unit["type"] && unit2["hp"] > 0
                }) return true
                move_towards_closest(map, units, unit);
                // Time to fight
                // (well, hit a defenseless enemy who'll hit back later)
                def enemy_type = enemy_type(unit)
                def to_hit = [
                    [0, -1], [-1, 0], [1, 0], [0, 1]
                ].collect { dx, dy ->
                    [unit["x"] + dx, unit["y"] + dy]
                }.findAll {
                    nx, ny -> map[ny][nx] == enemy_type
                }.collect {
                    nx, ny -> pos2unit(units, nx, ny)
                }.findAll {
                    enemy -> enemy["hp"] > 0
                }.sort {
                    enemy1, enemy2 ->
                    enemy1["hp"] - enemy2["hp"] ?:
                    enemy1["y"] - enemy2["y"] ?:
                    enemy1["x"] - enemy2["x"]
                }
                if (to_hit) {
                    enemy = to_hit[0]
                    enemy["hp"] -= [G: 3, E: elf_power][unit["type"]]
                    if (enemy["hp"] <= 0) {
                        if (enemy["type"] == "E") elf_dead = true
                        map[enemy["y"]][enemy["x"]] = "*"
                    }
                }
            }
            return false
        }
        if (part == 2 && elf_dead) return null
        units.removeIf { unit -> unit["hp"] <= 0 }
        clearScreen();
        print_map(map, part, elf_power)
        for (row in map)
            for (c in 0..row.size())
                if (row[c] == "*") row[c] = "."
        if (done) break;
        full_rounds++
        sleep(50)
    }
    sum = 0
    hps = []
    units.each { unit ->
        hps << unit["hp"]
        sum += unit["hp"]
    }
    return sprintf(
        "Part %d:\n"
        + "  Full rounds: %d\n"
        + "  Remaining hit points: %d (=%s)\n"
        + "  Result: %d\n",
        part, full_rounds, sum, hps.join("+"), sum * full_rounds
    )
}

def part1() {
    return solve(3)
}

def part2() {
    def elf_power = 3
    def res2 = null
    while (res2 == null) res2 = solve(++elf_power)
    return res2
}

def print_map(map, part, elf_power) {
    println(sprintf("Part %d (elf power: %d)", part, elf_power))
    for (row in map)
        println row.join("")
}

res1 = part1()
res2 = part2()
print res1
print res2
