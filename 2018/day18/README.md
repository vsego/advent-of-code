# Day 18: [Rust](https://www.rust-lang.org/)

Rust turned out to be a pain. I understand that it's focused on safety and
concurrency, but for a one-time non-concurrent use, the concept of variables'
ownership and borrowing, as well as (too) strong typing was just too much. I
tried it with several other problems before and always gave up due to weird
compiling errors that I was unable to resolve.

Also, some constructs are plain weird and, even that has a good justification,
shortcuts for often used expressions should exist. For example, practically
every language will provide the `i`-th character of string `s` as `s[i]`, but
in Rust you need to do `s.chars().nth(i).unwrap()`. This wasn't hard to find,
but it took some Googling to accept that this is really how it's _meant_ to be
done.

I don't think I'll be revisiting this one.

The problem itself was a fairly routine one, with part 2 yet again obviously
requiring caching and skipping almost all of the one billion of required steps.

I expected this too look nicely when animated, so I did that too, and it really
looks pretty. The only issue was how to properly clear the screen, but this is
not the problem of the language itself. The version I went with works nicely as
long as the whole display fits in the screen. If the console has fewer lines,
they won't be cleared, but that doesn't affect the animation, so I'm happy.
