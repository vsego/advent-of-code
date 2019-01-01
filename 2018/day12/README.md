# Day 12: [PHP](http://www.php.net/)

Ah, PHP... so easy to learn, yet even easier to hate. In my Perl days my way of
picking a language to use was pretty much "PHP for simple web stuff, Perl for
anything serious". Python replaced both of them and my one significant trip
back to PHP since then didn't go well.

The language is still the same ol' I remember, with many extras that I didn't
need here, so I coded like it's 1998 (I believe it might be runnable under PHP
3; if not, then we're partying like it's 2004, when PHP 5 was released). The
major annoyances it can cause don't really show on the problems of this
magnitude, so the overall experience was pleasant.

The problem itself is simple, until one gets to the part 2. As is the case with
a certain number of AoC problems, a pattern needs to be spotted and then used
to avoid otherwise ridiculous amount of computation. For that purpose, I
introduced caching of results, which quickly noticed that the pattern is simply
moving by 1 position per cycle, thus easily jumping over all but the first few
hundred steps.
