/*

To install Kotlin, run as an ordinary user:
    curl -s "https://get.sdkman.io" | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    sdk version
    sdk install kotlin

To compile and run:
    kotlinc day19.kt -include-runtime -d day19.jar && java -jar day19.jar

*/
package Day19

import java.io.File
import java.util.Arrays

// From https://stackoverflow.com/a/46402113/1667018
fun Boolean.toInt() = if (this) 1 else 0

fun calc(registers: IntArray, cmd: String, a: Int, b: Int, c: Int): Unit {
    when (cmd) {
        "addr" -> registers[c] = registers[a] + registers[b]
        "addi" -> registers[c] = registers[a] + b
        "mulr" -> registers[c] = registers[a] * registers[b]
        "muli" -> registers[c] = registers[a] * b
        "banr" -> registers[c] = registers[a] and registers[b]
        "bani" -> registers[c] = registers[a] and b
        "borr" -> registers[c] = registers[a] or registers[b]
        "bori" -> registers[c] = registers[a] or b
        "setr" -> registers[c] = registers[a]
        "seti" -> registers[c] = a
        "gtir" -> registers[c] = (a > registers[b]).toInt()
        "gtri" -> registers[c] = (registers[a] > b).toInt()
        "gtrr" -> registers[c] = (registers[a] > registers[b]).toInt()
        "eqir" -> registers[c] = (a == registers[b]).toInt()
        "eqri" -> registers[c] = (registers[a] == b).toInt()
        "eqrr" -> registers[c] = (registers[a] == registers[b]).toInt()
    }
}

fun read_file(fname: String): List<String> {
    return File(fname).readLines()
}

fun run_line(registers: IntArray, ip: Int, line: String): Int {
    if (line.startsWith("#ip ")) {
        var new_ip: Int = line.takeLast(line.length - 4).toInt()
        registers[new_ip]--
        return new_ip
    } else {
        val code: List<String> = line.split(" ")
        calc(
            registers,
            code[0], code[1].toInt(), code[2].toInt(), code[3].toInt()
        )
        return ip
    }
}

fun run(registers: IntArray, prog: List<String>): Unit {
    var ip: Int = 0
    var idx: Int = 0
    while (idx < prog.size) {
        ip = run_line(registers, ip, prog[idx])
        // println("> ${Arrays.toString(registers)}")
        idx = (++registers[ip]) + 1
    }
}

fun part1(prog: List<String>): Int {
    val registers: IntArray = intArrayOf(0, 0, 0, 0, 0, 0)
    run(registers, prog)
    return registers[0]
}

fun cmd_as_str(idx: Int, cmd: String, a: Int, b: Int, c: Int): String {
    val registers: List<String> = listOf("a", "b", "c", "d", "e", "f")
    val line_num: String = "%2d".format(idx - 1)
    when (cmd) {
        "addr" -> return "${line_num}: ${registers[c]} = ${registers[a]} + ${registers[b]}"
        "addi" -> return "${line_num}: ${registers[c]} = ${registers[a]} + ${b}"
        "mulr" -> return "${line_num}: ${registers[c]} = ${registers[a]} * ${registers[b]}"
        "muli" -> return "${line_num}: ${registers[c]} = ${registers[a]} * ${b}"
        "banr" -> return "${line_num}: ${registers[c]} = ${registers[a]} and ${registers[b]}"
        "bani" -> return "${line_num}: ${registers[c]} = ${registers[a]} and ${b}"
        "borr" -> return "${line_num}: ${registers[c]} = ${registers[a]} or ${registers[b]}"
        "bori" -> return "${line_num}: ${registers[c]} = ${registers[a]} or ${b}"
        "setr" -> return "${line_num}: ${registers[c]} = ${registers[a]}"
        "seti" -> return "${line_num}: ${registers[c]} = ${a}"
        "gtir" -> return "${line_num}: ${registers[c]} = (${a} > ${registers[b]} ? 1 : 0)"
        "gtri" -> return "${line_num}: ${registers[c]} = (${registers[a]} > ${b} ? 1 : 0)"
        "gtrr" -> return "${line_num}: ${registers[c]} = (${registers[a]} > ${registers[b]} ? 1 : 0)"
        "eqir" -> return "${line_num}: ${registers[c]} = (${a} == ${registers[b]} ? 1 : 0)"
        "eqri" -> return "${line_num}: ${registers[c]} = (${registers[a]} == ${b} ? 1 : 0)"
        "eqrr" -> return "${line_num}: ${registers[c]} = (${registers[a]} == ${registers[b]} ? 1 : 0)"
    }
    return ""
}

fun interpret_line(idx: Int, ip: Int, line: String): Int {
    if (line.startsWith("#ip ")) {
        return line.takeLast(line.length - 4).toInt()
    } else {
        val code: List<String> = line.split(" ")
        var result = cmd_as_str(
            idx, code[0], code[1].toInt(), code[2].toInt(), code[3].toInt()
        )
        if (ip == code[3].toInt()) {
            result += " !!!"
        }
        println(result)
        return ip
    }
}

fun interpret(registers: IntArray, prog: List<String>): Unit {
    var ip: Int = 0
    var idx: Int = 0
    print("a = ${registers[0]}; b = ${registers[1]}; c = ${registers[2]}; ")
    println("d = ${registers[3]}; e = ${registers[4]}; f = ${registers[5]}")
    prog.forEach {
        line -> ip = interpret_line(idx++, ip, line)
    }
}

fun part2(prog: List<String>): Unit {
    val registers: IntArray = intArrayOf(1, 0, 0, 0, 0, 0)
    println("Decoded program:")
    interpret(registers, prog)
}

fun main(args: Array<String>) {
    val fname: String = if (args.size > 0) args[0] else "day19.in"
    val prog: List<String> = read_file(fname)

    println("Part 1: ${part1(prog)}")
    part2(prog)
}
