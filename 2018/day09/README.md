# Day 9: [C++](https://en.wikipedia.org/wiki/C%2B%2B)

Oh, boy, I used to hate C++. It was always competing with Java as my least
favourite language. :-) This experience, however, was not at all bad. Sure,
strong typing and weird templates' syntax still make it a bit unpleasant,
compared to non-compiled languages like Python, but that's the expected price
of compiling your code.

I was nicely surprised that regexes are a part of the language now, as I didn't
want to install (and, thus, require) any non-standard libraries. This removed
the biggest hurdle of C/C++ programming: string manipulation.

The problem itself is simple enough, until one gets to the second part, which
is ridiculously (in a good way) bloated and required good support for
[double-ended queues](https://en.wikipedia.org/wiki/Double-ended_queue) which
C++ provides through `std:deque` template.

I wrote the first version of this in [newLISP](http://www.newlisp.org/). Of
course, my first version was way too slow because it was working with indexes.
However, the second version used `rotate`, `push`, and `pop` at the beginning
and at the end of a list. As per [newLISP
manual](http://www.newlisp.org/newlisp_manual.html#push), "Repeatedly using
push to the end of a list using -1 as the int-index is optimized and as fast as
pushing to the front of a list with no index at all. This can be used to
efficiently grow a list". This would imply that the dequeue approach should be
fast, but it wasn't so. It seems that working with the ends of lists is much
slower than with beginnings and the program simply ran forever.
