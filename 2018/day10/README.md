# Day 10: [Julia](https://julialang.org/)

I've heard quite a lot about sheer awesomeness of Julia while in academia, but
it always left an impression of a hot air balloon with very little true
substance. Due to that impression, I never tried it myself, making this a good
opportunity.

The whole impression was less than thrilling. I may be prejudiced about it, but
the impression of "Python-like language that tries too hard to not be Python" I
had before persists. Like with Go, I simply see no benefits in having yet
another language that - seemingly - doesn't bring much to the table.

Some might argue that JIT makes it much faster, but it's not like Python
doesn't support JIT itself (for example, [Numba](https://numba.pydata.org/),
but there are other solutions as well). Maybe doing just this one example (or
this one in particular) was just too little to appreciate it.

The problem itself was a fun one. The first impression it leaves is that one
needs to OCR an ASCII drawing, which is not impossible, but quite hard, given
that we're not given the "font" in use. However, some consideration made this
quite simple in the end. One just needs to notice that the linear movement of
lights means that the message should appear when the last are closest to each
other or near it. So, my solution here was to find that time, and then query
the user for it and, if unhappy, go for the second before, then second after,
then 2 seconds before, etc. until the user says that they're happy.
