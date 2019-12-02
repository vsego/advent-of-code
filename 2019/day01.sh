#!/usr/bin/bash

function mass2fuel1() {
    echo $(($1/3-2))
}


function check() {
    ctype="$1"
    mass="$2"
    correct="$3"
    echo -n "Checking for mass $mass of type $ctype..."
    result="$(mass2fuel$ctype "$mass")"
    if [ "$result" -eq "$correct" ]; then
        echo " OK."
    else
        echo "Wrong: $result != $correct!"
    fi
}


function mass2fuel2() {
    result=0
    last="$(mass2fuel1 "$1")"
    while [ "$last" -ge 0 ]; do
        result="$(($result+$last))"
        last="$(mass2fuel1 "$last")"
    done
    echo "$result"
}


function solution() {
    ctype="$1"
    ( cat day01.in | while read line; do mass2fuel$ctype "$line"; done | tr "\n" +; echo 0 ) | bc
}


echo "Testing part 1..."
check 1 12 2
check 1 14 2
check 1 1969 654
check 1 100756 33583

echo "Testing part 2..."
check 2 12 2
check 2 1969 966
check 2 100756 50346

for i in 1 2; do
    echo -n "Part $i: "
    solution $i
done
