#!/usr/bin/env julia

function int(s)
    return parse(Int64, s)
end

function load_points(lines)
    result = []
    for line in lines
        m = match(r"\s*position=<\s*(-?\d+),\s*(-?\d+)>\s*velocity=<\s*(-?\d+),\s*(-?\d+)>\s*", line)
        push!(result, Dict("px"=>int(m[1]), "py"=>int(m[2]), "vx"=>int(m[3]), "vy"=>int(m[4])))
    end
    return result
end

function get_px(point, t)
    return point["px"] + t * point["vx"]
end

function get_py(point, t)
    return point["py"] + t * point["vy"]
end

function get_box(points, t)
    left = right = get_px(points[1], t)
    top = bottom = get_py(points[1], t)
    for point in points
        x = get_px(point, t)
        y = get_py(point, t)
        if x < left
            left = x
        end
        if x > right
            right = x
        end
        if y < top
            top = y
        end
        if y > bottom
            bottom = y
        end
    end
    return left, top, right - left + 1, bottom - top + 1
end

function get_size(points, t)
    left, top, width, height = get_box(points, t)
    return width, height
end

function find_min(points)
    t = 0
    while true
        width, height = get_size(points, t)
        size = max(width, height)
        if t == 0 || size < min_size
            min_size = size
        elseif size >= min_size
            return t - 1
        end
        t += 1
    end
end

function paint(points, t)
    left, top, width, height = get_box(points, t)
    canvas = [["." for _ in 1:width] for _ in 1:height]
    for point in points
        canvas[get_py(point, t) - top + 1][get_px(point, t) - left + 1] = "#"
    end
    println()
    println("t = ", t)
    for row in canvas
        println(join(row))
    end
end

function solve(points)
    t0 = find_min(points)
    delta = 0
    while true
        for sign in (0 < delta <= t0 ? (-1, 1) : 1)
            t = t0 + sign * delta
            paint(points, t)
            print("Happy? ")
            yn = chomp(readline())
            if yn == "y"
                return
            end
        end
        delta += 1
    end
end

test = [
    "position=< 9,  1> velocity=< 0,  2>",
    "position=< 7,  0> velocity=<-1,  0>",
    "position=< 3, -2> velocity=<-1,  1>",
    "position=< 6, 10> velocity=<-2, -1>",
    "position=< 2, -4> velocity=< 2,  2>",
    "position=<-6, 10> velocity=< 2, -2>",
    "position=< 1,  8> velocity=< 1, -1>",
    "position=< 1,  7> velocity=< 1,  0>",
    "position=<-3, 11> velocity=< 1, -2>",
    "position=< 7,  6> velocity=<-1, -1>",
    "position=<-2,  3> velocity=< 1,  0>",
    "position=<-4,  3> velocity=< 2,  0>",
    "position=<10, -3> velocity=<-1,  1>",
    "position=< 5, 11> velocity=< 1, -2>",
    "position=< 4,  7> velocity=< 0, -1>",
    "position=< 8, -2> velocity=< 0,  1>",
    "position=<15,  0> velocity=<-2,  0>",
    "position=< 1,  6> velocity=< 1,  0>",
    "position=< 8,  9> velocity=< 0, -1>",
    "position=< 3,  3> velocity=<-1,  1>",
    "position=< 0,  5> velocity=< 0, -1>",
    "position=<-2,  2> velocity=< 2,  0>",
    "position=< 5, -2> velocity=< 1,  2>",
    "position=< 1,  4> velocity=< 2,  1>",
    "position=<-2,  7> velocity=< 2, -2>",
    "position=< 3,  6> velocity=<-1, -1>",
    "position=< 5,  0> velocity=< 1,  0>",
    "position=<-6,  0> velocity=< 2,  0>",
    "position=< 5,  9> velocity=< 1, -2>",
    "position=<14,  7> velocity=<-2,  0>",
    "position=<-3,  6> velocity=< 2, -1>",
]

points = load_points(test)
solve(points)

open("day10.in") do f
    points = load_points(readlines(f))
    solve(points)
end

