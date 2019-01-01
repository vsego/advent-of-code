# Day 20: [newLISP](http://www.newlisp.org/)

Technically, this was not my first newLISP program. It was my third one, after
failing to get [Day 9](../day09/) and [Day 14](../day14/) solutions to run in a
reasonable (or even bearable) amount of time.

Having never used any flavour of LISP, I've been curious for a while to try the
infamous language of parentheses and see what all the fuss is about. This ended
with a bit of surprise: the language is quite normal, once you get used to the
somewhat unusually syntax.

However, it is definitely not suitable for problems like those in AoC. Even
though I managed to solve this problem, I was missing sets and dictionaries,
which are quite common in modern languages, and I had to implement them myself,
with the price of some extra code and linear time execution where log time
would be a normal thing. Luckily, this turned out to be enough and this time I
didn't end up with yet another cool, but useless attempt.

I am aware of newLISP's `assoc`, but I couldn't get it to work with keys that
are lists and not simple values. Even if it is possible, `assoc` is just a
different way of searching the list, which wouldn't bring any speed
improvements (sets and dictionaries need btree mechanism to get log time), so I
went with my own (still linear) `find`-based implementation.

The problem was not too hard. It is naturally recursive, but it seemed easier
to implement the needed stacks (for local beginnings and endings of the path),
while analysing the input char-by-char. Having had the experience with two of
the older AoC problems and newLISP, this went fairly smoothly.

It's hard to imagine I'll be revisiting newLISP any time soon. I see no
benefits, and the missing functionalities are a significant problem, as is the
slow implementation of the end-of-list operations (see my comments in [Day
9](../day09/) problem).
