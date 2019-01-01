use std::{
    collections::HashMap,
    env,
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
    thread,
    time,
};

fn lines_from_file<P>(filename: P) -> Vec<String>
where
    P: AsRef<Path>,
{
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

fn new_object(map: &Vec<String>, x: usize, y: usize) -> char {
    let mut cnt1 = 0;
    let mut cnt2 = 0;
    let current = map[y].chars().nth(x).unwrap();
    for i in 0..3 {
        for j in 0..3 {
            if i == 1 && j == 1 {
                continue;
            }
            let ax = x + i;
            let ay = y + j;
            if ay <= 0 || ay > map.len() || ax <= 0 || ax > map[ay - 1].len() {
                continue;
            }
            let adjacent = map[ay - 1].chars().nth(ax - 1).unwrap();
            if (current == '.' && adjacent == '|') || (current == '|' && adjacent == '#') {
                cnt1 += 1;
            } else if current == '#' {
                if adjacent == '#' {
                    cnt1 += 1;
                }
                else if adjacent == '|' {
                    cnt2 += 1;
                }
            }
        }
    }
    if current == '.' && cnt1 >= 3 {
        return '|';
    }
    if current == '|' && cnt1 >= 3 {
        return '#';
    }
    if current == '#' && (cnt1 == 0 || cnt2 == 0) {
        return '.';
    }
    return current;
}

fn print_map(step: u32, map: &Vec<String>) -> String {
    print!("{}[{};{}H", '\x1B', 1, 1);
    let mut cnt_wood = 0;
    let mut cnt_yard = 0;
    for row in map {
        println!("{}", row);
        cnt_wood += row.matches("|").count();
        cnt_yard += row.matches("#").count();
    }
    let result = format!(
        "Current solution: {} * {} = {} [step: {}]",
        cnt_wood, cnt_yard, cnt_wood * cnt_yard, step,
    );
    println!("{}", result);
    return result;
}

fn solve(map: &Vec<String>, steps: u32) -> String {
    let mut map_curr: Vec<String> = map.to_vec();
    let mut history: HashMap<String, u32> = HashMap::new();
    for step in 0..steps {
        let key: String = map_curr.join(";");
        let old_step = history.entry(key).or_insert(step);
        if *old_step < step {
            if (steps - step) % (step - *old_step) == 0 {
                println!("Step: {}, old step: {}", step, *old_step);
                break;
            }
        }
        print_map(step, &map_curr);
        thread::sleep(time::Duration::from_millis(50));
        let mut map_new: Vec<String> = Vec::new();
        for y in 0..map_curr.len() {
            map_new.push(
                (0..map_curr[y].len()).map(
                    |x| new_object(&map_curr, x, y)
                ).collect()
            );
        }
        map_curr = map_new;
    }
    return print_map(steps, &map_curr);
}

fn main() {
    let args: Vec<_> = env::args().collect();
    let map: Vec<String>;
    if args.len() > 1 {
        map = lines_from_file(args[1].to_string());
    } else {
        map = lines_from_file("day18.in");
    }
    let part1 = solve(&map, 10);
    let part2 = solve(&map, 1000000000);
    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
}
