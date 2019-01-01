#!/usr/bin/env lua

-- Borrowed from https://stackoverflow.com/a/11204889/1667018
function lines_from(file)
  lines = {}
  for line in io.lines(file) do
    table.insert(lines, line)
  end
  return lines
end

local data = lines_from('day04.in')
local guard = nil
local guards = {}
table.sort(data)

-- Make guards = {guard: {night1, night2,...}}
-- where nightx = {asleep0, asleep1,..., asleep60}
-- where asleepm = true if the guard is asleep at minute m and false otherwise
for k, line in pairs(data) do
  line = string.gsub(line, "%[", "")
  line = string.gsub(line, "%]", "")
  local min, action = string.match(line, "%d*-%d*-%d* %d*:(%d*) (.+)")
  if action == "wakes up" then
    for m = tonumber(min), 60 do
        guards[guard][#guards[guard]][m] = false
    end
  elseif action == "falls asleep" then
    for m = tonumber(min), 60 do
        guards[guard][#guards[guard]][m] = true
    end
  else
    local who = string.match(action, "Guard #(%d+) begins shift")
    guard = tonumber(who)
    if not guards[guard] then
      guards[guard] = {}
    end
    table.insert(guards[guard], {})
    for m = 0, 60 do
        guards[guard][#guards[guard]][m] = false
    end
  end
end

-- Find the biggest sleeper
local max_guard = nil
local max_guard_sleep = 0
for guard, nights in pairs(guards) do
  local sleep = 0
  for n, night in pairs(nights) do
    for min, is_asleep in pairs(night) do
      if is_asleep then
        sleep = sleep + 1
      end
    end
  end
  if sleep > max_guard_sleep then
    max_guard = guard
    max_guard_sleep = sleep
  end
end

-- Find when the biggest sleeper slept the most
local max_sleeps_min = nil
local max_sleeps_min_sleeps = 0
for min = 0, 60 do
  local num_sleeps = 0
  for n, night in pairs(guards[max_guard]) do
    if night[min] then
      num_sleeps = num_sleeps + 1
    end
  end
  if num_sleeps > max_sleeps_min_sleeps then
    max_sleeps_min = min
    max_sleeps_min_sleeps = num_sleeps
  end
end

print("Part 1: " .. max_guard * max_sleeps_min)

-- Find the guard and the minute when he slept the most
part2_guard = nil
part2_min = 0
part2_max_sleeps = 0
for guard, nights in pairs(guards) do
  for min = 0, 60 do
    local num_sleeps = 0
    for n, night in pairs(nights) do
      if night[min] then
        num_sleeps = num_sleeps + 1
      end
    end
    if num_sleeps > part2_max_sleeps then
      part2_guard = guard
      part2_min = min
      part2_max_sleeps = num_sleeps
    end
  end
end

print("Part 2: " .. part2_guard * part2_min)
