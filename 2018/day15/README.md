# [Apache Groovy](http://groovy-lang.org/)

I have never heard of Groovy before and I wouldn't have found it if I wasn't
looking for more languages for this challenge. It's like an extension of Java,
but a really pleasant one and I thoroughly enjoyed it. Since it compiles to JVM
bytecode, I wonder if it could serve as a really _groovy_ replacement for Java
(`java day15` fails after I compile it). Definitely one of the two most
pleasant surprises among the new languages I've dealt with in this challenge!

The problem itself was not an enjoyable one and I'm happy I've picked a
language that made up for that. It's not so much that the problem is hard, but
it is (has to be) too precisely defined. A very minor change in logic, one that
would make sense in a "program your units" type of problem, ruins everything
here and I missed details several times until getting the right behaviour.

On the bright side, the extra need to debug stuff resulted in a nicely animated
battle sequences. Hollywood, here I come! :-D

## An attempt to optimize the algorithm

Part 2 was fairly straightforward (replay the battle with linearly increased
Elves' power), but I wanted to go for more, so I also did a variation that
basically doubles their strength and then, once they win without losses, uses
bisection to find the correct solution more quickly.

Somewhat surprisingly, this does not work: my input's solution is found for
power 19, yet at the power 24 the Elves have losses again, so my bisection
ended in the range 25-48, with no hope of finding the correct solution.

I assume that this is happening because more power means that some Elf finishes
his battle more quickly, but then engages another goblin and, in his weakened
state, gets killed. A weaker Elf would've stayed in the first battle long
enough for the second Goblin to get killed by a stronger Elf.
