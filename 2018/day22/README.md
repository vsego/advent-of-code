# Day 22: [Python](https://www.python.org/)

Ooh, a recursive problem! I know: Erlang! After spending quite a while trying
to figure out how to do caching of the results (to avoid exponential number of
recursive calls), I gave up and went with a safe bet instead: Python, the
language in which I earn my living and which I use for personal programming.
Obviously, I prefer it to other languages. :-)

The problems here are a simple recursion with two recursive calls and a fairly
straightforward graph search algorithm, with a minor twist that locally
shortest parts wouldn't necessarily lead to the optimal solution. It is
possible to go through some point with a bit longer path and still end up with
an optimal solution if that so-far-longer path leads to fewer item changes.
