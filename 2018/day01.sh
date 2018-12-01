#!/usr/bin/bash

echo "Part 1: $(paste -sd "" day01.in | sed 's/^+//' | bc)"

nums=( $(for num in $(cat day01.in); do echo -n "$num "; done) )
declare -A sums
sum=0
while true; do
    for i in ${!nums[@]}; do
        sum=$(($sum+${nums[$i]}))
        if [ ${sums[$sum]} ]; then
            echo "Part 2: $sum"
            exit 0
        fi
        sums[$sum]=1
    done
done
