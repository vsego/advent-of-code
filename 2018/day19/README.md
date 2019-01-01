Day 19: [Kotlin](https://kotlinlang.org/)

Another first for me, Kotlin is quite similar to Groovy: an upgrade to Java
meant to make it more pleasant and safe. Being a very new language (it is only
at its version 1.3 at the moment), it has no RPM, so I found compiler binary,
downloaded it, and started using it. It _kinda_ worked, but it didn't really,
because dependencies were breaking down and I couldn't do much with it. The
proper way to install this is to use [SDKMAN](https://sdkman.io/):

    curl -s "https://get.sdkman.io" | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    sdk version
    sdk install kotlin

This is done for the user that wants to use it (i.e., no root privileges
needed) and the stuff ends up in your home's `.sdkman` directory, making it
easy to remove it.

Once I did it this way, it was pretty straightforward. A bit of trouble stems
from the fact that it's a new language, so not as many resources out there as
for more established languages, but it's a pleasant one and I had not
significant trouble with it.

The problem itself is a typical reverse engineering problem. Part 1 is "just do
what it says, no challenge whatsoever" type of problem. Part 2 can be done in
the same way, but the computation would've lasted a few decades, if not more.

For that, I modified the calculation part to produce a human readable code,
dumped it to a text file, and then analysed it and chopped it up until it was
clear that it's really just a sum of divisors of a big number, computed in a
really anti-optimised way. To keep as Kotliny as possible, I did this as
[`day19part2.kt`](day19part2.kt), in `log`-time just to play a bit with
Kotlin's basic math functions.

The reverse engineering part is very similar to one problem from a previous
AoC, which was fun the first time around, but not very interesting to do it
again. All in all, the pleasantness of Kotlin saved the day on this one.
