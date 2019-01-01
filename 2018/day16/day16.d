/*

To compile and run this:

    dmd -run day16.d

*/
import std.algorithm;
import std.conv;
import std.regex;
import std.stdio;
import std.string;

void function(int[] registers, int arg1, int arg2, int arg3)[string] ops;

void init() {
    ops = [
        "addr": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] + registers[b];
        },
        "addi": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] + b;
        },
        "mulr": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] * registers[b];
        },
        "muli": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] * b;
        },
        "banr": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] & registers[b];
        },
        "bani": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] & b;
        },
        "borr": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] | registers[b];
        },
        "bori": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a] | b;
        },
        "setr": function void(int[] registers, int a, int b, int c) {
            registers[c] = registers[a];
        },
        "seti": function void(int[] registers, int a, int b, int c) {
            registers[c] = a;
        },
        "gtir": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(a > registers[b]);
        },
        "gtri": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(registers[a] > b);
        },
        "gtrr": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(registers[a] > registers[b]);
        },
        "eqir": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(a == registers[b]);
        },
        "eqri": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(registers[a] == b);
        },
        "eqrr": function void(int[] registers, int a, int b, int c) {
            registers[c] = int(registers[a] == registers[b]);
        },
    ];
}

void compute(int[] registers, string name, int arg1, int arg2, int arg3) {
    ops[name](registers, arg1, arg2, arg3);
}

void solve() {
    auto fp = File("day16.in");
    int[] registers = [0, 0, 0, 0];
    string line;
    auto re_before = ctRegex!(r"Before:\s*\[\s*(-?\d+(,\s*-?\d+)+)\s*\]");
    auto re_cmd = ctRegex!(r"(-?\d+(\s+-?\d+){3})");
    auto re_after = ctRegex!(r"After:\s*\[\s*(-?\d+(,\s*-?\d+)+)\s*\]");
    line = strip(fp.readln());
    int result1 = 0;
    string[][] code2op_candidates = new string[][](16, 16);
    foreach (i; 0..16)
        code2op_candidates[i] = ops.keys[];

    // Part 1 + getting the candidates for each opcode
    while (true) {
        auto m_before = matchFirst(line, re_before);
        if (m_before.empty) break;
        auto m_cmd = matchFirst(strip(fp.readln()), re_cmd);
        auto m_after = matchFirst(strip(fp.readln()), re_after);
        int[] before = to!(int[])(split(m_before[1], r", "));
        int[] cmd = to!(int[])(split(m_cmd[1], r" "));
        int[] after = to!(int[])(split(m_after[1], r", "));
        int cnt = 0;
        foreach (cmd_name; ops.keys) {
            registers[] = before[];
            compute(registers, cmd_name, cmd[1], cmd[2], cmd[3]);
            if (registers == after) {
                cnt++;
                if (cnt >= 3) {
                    if (cnt == 3) result1++;
                    if (code2op_candidates.length == 1) break;
                }
            } else {
                code2op_candidates[cmd[0]] = code2op_candidates[cmd[0]].remove!(name => name == cmd_name);
            }
        }
        while (true) {
            line = strip(fp.readln());
            if (!line.empty) break;
        }
    }

    // If an opcode has only one candidate, we know that this candidate
    // corresponds to it, so we can safely assign it and remove the candidate
    // from the lists of candidates of other opcodes.
    string[] code2op = new string[](16);
    bool done = false;
    while (!done) {
        done = true;
        foreach (idx, candidates; code2op_candidates) {
            if (candidates.length == 1) {
                auto cmd_name = candidates[0];
                code2op[idx] = cmd_name;
                code2op_candidates[idx] = [];
                foreach (idx2; 0..16)
                    if (code2op_candidates[idx2].length > 1)
                        code2op_candidates[idx2] = code2op_candidates[idx2].remove!(name => name == cmd_name);
                done = false;
            }
        }
    }

    // We now know the operation that each opcode corresponds to
    writeln("Conversion table:");
    foreach (i, v; code2op)
        writefln("  %s: %s", i, v);

    // We now read the rest of the file and run the program
    registers = [0, 0, 0, 0];
    while (true) {
        auto m_cmd = matchFirst(strip(line), re_cmd);
        auto cmd = to!(int[])(split(m_cmd[1], r" "));
        compute(registers, code2op[cmd[0]], cmd[1], cmd[2], cmd[3]);
        line = strip(fp.readln());
        if (line.empty) break;
    }
    writefln("Result: %s", registers);
    writeln();

    // Finally, we print the results for both parts
    writefln("Part 1: %d", result1);
    writefln("Part 2: %d", registers[0]);
}

void main() {
    init();
    solve();
}
