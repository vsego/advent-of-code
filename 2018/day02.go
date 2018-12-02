package main

import (
    "bufio"
    "fmt"
    "os"
)

// Borrowed from https://stackoverflow.com/a/18479916/1667018
func readLines(path string) ([]string, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    var lines []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }
    return lines, scanner.Err()
}

// Borrowed from https://stackoverflow.com/a/27516559/1667018
func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func part1(lines []string) {
    twos := 0
    threes := 0
    for _, line := range lines {
        chars := make(map[string]int)
        for _, r := range line {
            c := string(r)
            chars[c] += 1
        }
        has_twos := false
        has_threes := false
        for _, r := range chars {
            if int(r) == 2 {
                has_twos = true
            } else if int(r) == 3 {
                has_threes = true
            }
        }
        if has_twos {
            twos++
        }
        if has_threes {
            threes++
        }
    }
    fmt.Println("Part 1:", twos * threes)
}

func part2(lines []string) {
    for idx1, line1 := range lines {
        for _, line2 := range lines[idx1 + 1:] {
            diff_cnt := 0
            same := ""
            for i := 0; i < min(len(line1), len(line2)); i++ {
                if line1[i] == line2[i] {
                    same += string(line1[i])
                } else {
                    diff_cnt++
                    if diff_cnt > 1 {
                        break
                    }
                }
            }
            if diff_cnt == 1 {
                fmt.Println("Part 2:", same)
            }
        }
    }
}

func main() {
    lines, _ := readLines("day02.in")
    part1(lines)
    part2(lines)
}
