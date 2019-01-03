# To compile and run:
#     nim c -r day21.nim

import future
import re
import sequtils
import strutils

var
  reFirstLine = re"#ip\s+(\d)"
  reCmdLine = re"(\w+)\s+(\d+)\s+(\d+)\s+(\d+)"

proc calc(registers: var array[6, int], cmd: string, a: int, b: int, c: int) =
  case cmd:
    of "addr": registers[c] = registers[a] + registers[b]
    of "addi": registers[c] = registers[a] + b
    of "mulr": registers[c] = registers[a] * registers[b]
    of "muli": registers[c] = registers[a] * b
    of "banr": registers[c] = registers[a] and registers[b]
    of "bani": registers[c] = registers[a] and b
    of "borr": registers[c] = registers[a] or registers[b]
    of "bori": registers[c] = registers[a] or b
    of "setr": registers[c] = registers[a]
    of "seti": registers[c] = a
    of "gtir": registers[c] = if a > registers[b]: 1 else: 0
    of "gtri": registers[c] = if registers[a] > b: 1 else: 0
    of "gtrr": registers[c] = if registers[a] > registers[b]: 1 else: 0
    of "eqir": registers[c] = if a == registers[b]: 1 else: 0
    of "eqri": registers[c] = if registers[a] == b: 1 else: 0
    of "eqrr": registers[c] = if registers[a] == registers[b]: 1 else: 0

proc solve(prog: seq[string]) =
  var
    registers: array[6, int] = [0, 0, 0, 0, 0, 0]
    idx: int = 0
    matches: array[4, string]
    ip: int = 0
    history: seq[int] = @[]
  while true:
    if match(prog[idx], reFirstLine, matches):
      ip = parseInt(matches[0])
      inc idx
    elif match(prog[idx], reCmdLine, matches):
      registers[ip] = idx - 1
      if (idx == 29):
        # Mimic always "false"
        registers[parseInt(matches[3])] = 0
        if (history.len == 0):
          echo "Part 1: ", registers[2]
        if contains(history, registers[2]):
          echo "Part 2: ", history[history.len - 1]
          break
        history.add(registers[2])
      else:
        calc(
          registers,
          matches[0],
          parseInt(matches[1]), parseInt(matches[2]), parseInt(matches[3]),
        )
      idx = registers[ip] + 2
      if idx >= prog.len:
        break

var
  prog = lc[line | (line <- lines("day21.in")), string]

solve(prog)
