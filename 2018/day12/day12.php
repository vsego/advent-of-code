<?php

$test = [
    "init" => "#..#.#..##......###...###",
    "trans" => [
        "...##" => "#",
        "..#.." => "#",
        ".#..." => "#",
        ".#.#." => "#",
        ".#.##" => "#",
        ".##.." => "#",
        ".####" => "#",
        "#.#.#" => "#",
        "#.###" => "#",
        "##.#." => "#",
        "##.##" => "#",
        "###.." => "#",
        "###.#" => "#",
        "####." => "#",
    ],
];
$history = array();

function init(&$input) {
    global $history;
    $history = array();
    $input["state"] = array();
    for ($i = 0; $i < strlen($input["init"]); $i++)
        if ($input["init"][$i] == "#")
            $input["state"][$i] = true;
}

function init_from_file($fname) {
    $fp = fopen($fname, "rt");
    $input = [
        "init" => substr(fgets($fp), 15),
        "trans" => array(),
    ];
    while ($line = fgets($fp))
        if (preg_match("/^\s*([#.]{5})\s*=>\s*([#.])\s*$/", $line, $re_out))
            $input["trans"][$re_out[1]] = $re_out[2];
    init($input);
    return $input;
}

function state_to_string(&$data, $from=null, $to=null) {
    if (is_null($from))
        $from = min(array_keys($data["state"]));
    if (is_null($to))
        $to = max(array_keys($data["state"]));
    $res = "";
    for ($pos = $from; $pos <= $to; $pos++)
        $res .= (array_key_exists($pos, $data["state"]) ? "#" : ".");
    return array($from, $to, $res);
}

function get_or_stash(&$data, $remaining_steps) {
    global $history;
    list($from, $to, $key) = state_to_string($data);
    if (array_key_exists($key, $history)) {
        $old = $history[$key];
        $steps_delta = $old["rsteps"] - $remaining_steps;
        $cycles = intdiv($remaining_steps, $steps_delta);
        $delta = ($from - $old["from"]) * $cycles;
        $state = array();
        foreach ($data["state"] as $pos => $true)
            $state[$pos + $delta] = true;
        $data["state"] = $state;
        return $remaining_steps - $cycles * $steps_delta;
    } else {
        $history[$key] = array(
            "from" => $from,
            "rsteps" => $remaining_steps,
        );
        return $remaining_steps;
    }
}

function print_state(&$data, $from=null, $to=null) {
    list($from, $to, $str) = state_to_string($data, $from, $to);
    echo "State $from-$to\n$str\n";
}

function char_at(&$data, $pos) {
    return (array_key_exists($pos, $data["state"]) ? "#" : ".");
}

function one_step(&$data) {
    $new_state = array();
    $min_pos = min(array_keys($data["state"]));
    $max_pos = max(array_keys($data["state"]));
    $key = "";
    for ($pos = $min_pos - 2; $pos <= $max_pos + 2; $pos++) {
        if ($key)
            $key = substr($key, 1) . char_at($data, $pos + 2);
        else
            for ($i = $pos - 2; $i <= $pos + 2; $i++)
                $key .= char_at($data, $i);
        if (isset($data["trans"][$key]) && $data["trans"][$key] == "#")
            $new_state[$pos] = true;
    }
    $data["state"] = $new_state;
}

function solve(&$data, $steps = 20) {
    while ($steps) {
        one_step($data);
        $steps--;
        $steps = get_or_stash($data, $steps);
    }
    $res = 0;
    foreach ($data["state"] as $pos => $true)
        $res += $pos;
    return $res;
}

init($test);
echo "Test 1: ", solve($test), "\n";

$data = init_from_file("day12.in");
echo "Part 1: ", solve($data), "\n";

$data = init_from_file("day12.in");
$res = solve($data, 50000000000);
echo "Part 2: $res\n";

?>
