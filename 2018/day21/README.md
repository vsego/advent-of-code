# Day 21: [Nim](https://nim-lang.org/)

Nim is a 12 years old programming language that's currently at version 0.19.2
(I used the version 0.18.0). At some point, I needed a list comprehension
(actually, I only wanted to convert an iterator to a list, the equivalent of
`list(something)` in Python) and I found a post from 2015. saying that I can
use `lc` from `future` package. It is the beginning of 2019 now and `lc` is
still in `future`. IMO, not very promising speed of development.

While Nim community provides extensive documentation and some examples, finding
something as simple as "read a text file as a `seq`/`array` of lines" proved to
be a mission impossible. There is a "read a file line by line" example, for
example on [RosettaCode](http://rosettacode.org/wiki/File_input/output#Nim),
just not the "dump it to something list-like" part.

The syntax is OK. Nothing to excite me or annoy me. It's just OK, and since it
feels unfinished and as if it stopped developing (it obviously did not, since
the latest version was released only 3 days ago), I'd chuck it under the
"what's purpose of this language?" category. Of course, as with the other
similar languages in this challenge, solving one problem using that language
is certainly not enough to give it a full, fair review.

The problem itself was far from thrilling. Implementing the same interpreter
for the third time was annoying, but that's the problem that came from using
different languages for all different problems. If I did it all in the same
one, I would've made and used a shared library/package. Luckily, redoing it in
Nim was not much work: copy/paste from [Kotlin](../day19/) + some vim editing.

The solution to the first part of the problem is straightforward after a minor
input analysis: the third line from the bottom is the only one using register
0, and it basically says `if register[0] == register[2] then halt`, which means
that part 1 is equivalent to replacing that command with
`print register[2]; halt`.

For part 2, one needs to find the last unique value that occurs in register 2.
After they start repeating, having one of those values would only end the
running of the program faster. I'm sure this was meant to be done with some
reverse engineering and/or optimization, but - as I mentioned before - I grew
tired of that, so I just ran it as described and got my answer in 2.5 hours.
Anything shorter that one night of sleep is, IMO, acceptable, making this
another problem solved without (too) much effort.
