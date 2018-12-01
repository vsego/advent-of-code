#!/usr/bin/env python3

class Done(Exception):
    def __init__(self, loop_length):
        self.loop_length = loop_length


def redistribute(state, used):
    used[state] = len(used)
    idx = max(enumerate(state), key=lambda t: (t[1], -t[0]))[0]
    val = state[idx]
    add_to_all = val // len(state)
    last_with_extra = val % len(state)
    new_state = list(state)
    new_state[idx] = 0
    for i in range(1, len(state) + 1):
        new_state[(idx + i) % len(state)] += (
            add_to_all + int(last_with_extra >= i)
        )
    new_state = tuple(new_state)
    if new_state in used:
        raise Done(len(used) - used[new_state])
    return new_state


def count_for(state):
    used = dict()
    while True:
        try:
            state = redistribute(state, used)
        except Done as e:
            return len(used), e.loop_length


print(count_for((0, 2, 7, 0)))
print(count_for(tuple(int(x) for x in input().split("\t"))))
