var test1 = [
    "/->-\\        ",
    "|   |  /----\\",
    "| /-+--+-\\  |",
    "| | |  | v  |",
    "\\-+-/  \\-+--/",
    "  \\------/   ",
]
var test2 = [
    "/>-<\\  ",
    "|   |  ",
    "| /<+-\\",
    "| | | v",
    "\\>+</ |",
    "  |   ^",
    "  \\<->/",
];

var rules = {
    "/": {
        "0,-1": [[1, 0]], "-1,0": [[0, 1]],
        "0,1": [[-1, 0]], "1,0": [[0, -1]],
    },
    "\\": {
        "0,-1": [[-1, 0]], "1,0": [[0, 1]],
        "0,1": [[1, 0]], "-1,0": [[0, -1]],
    },
    "+": {
        "0,-1": [[-1, 0], [0, -1], [1, 0]],
        "-1,0": [[0, 1], [-1, 0], [0, -1]],
        "0,1": [[1, 0], [0, 1], [-1, 0]],
        "1,0": [[0, -1], [1, 0], [0, 1]],
    },
};
var dirs = {"v": [0, 1], "^": [0, -1], "<": [-1, 0], ">": [1, 0]};

function get_track(input) {
    var track = {turns: {}, carts: []};
    for (var y = 0; y < input.length; y++) {
        for (var x = 0; x < input[y].length; x++) {
            var c = input[y].charAt(x);
            if (c in rules)
                track.turns[[x, y].toString()] = rules[c];
            else if (c in dirs)
                track.carts.push({pos: [x, y], dir: dirs[c], cross: 0});
        }
    }
    return track;
}

function solve(track, part) {
    while (true) {
        track.carts.sort(function(cart1, cart2) {
            var dy = cart1.pos[1] - cart2.pos[1];
            return dy ? dy : cart1.pos[0] - cart2.pos[0];
        });
        for (var i = 0; i < track.carts.length; i++) {
            var cart = track.carts[i];
            if (!cart) continue;
            cart.pos = [
                cart.pos[0] + cart.dir[0], cart.pos[1] + cart.dir[1],
            ];
            for (var j = 0; j < track.carts.length; j++) {
                if (
                    i != j && track.carts[j]
                    && track.carts[j].pos[0] == cart.pos[0]
                    && track.carts[j].pos[1] == cart.pos[1]
                ) {
                    track.carts[i] = track.carts[j] = null;
                    if (part == 1) return cart.pos;
                }
            }
            var turns = track.turns[cart.pos.toString()];
            if (turns) {
                var turns = turns[cart.dir.toString()];
                if (turns.length > 1) {
                    cart.dir = turns[cart.cross % turns.length];
                    cart.cross++;
                } else {
                    cart.dir = turns[0];
                }
            }
        }
        track.carts = track.carts.filter(function(value, index, arr) {
            return value !== null;
        });
        if (part == 2 && track.carts.length <= 2) {
            return track.carts[0].pos;
        }
    }
}

console.log("Test 1: " + solve(get_track(test1), 1));
console.log("Test 2: " + solve(get_track(test2), 2));

var fs = require("fs");
var input = fs.readFileSync("day13.in", "utf-8").split("\n");

console.log("Part 1: " + solve(get_track(input), 1));
console.log("Part 2: " + solve(get_track(input), 2));
