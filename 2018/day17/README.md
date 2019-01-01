Day 17: [Gambas](http://gambas.sourceforge.net/)

"Gambas" is a recursive acronym for "Gambas Almost Means Basic", a free
language/IDE similar to Visual Basic. I picked it by looking for _any_ Basic
that would install via `dnf`, and I was wondering what I'd come up with. I did
_try_ Visual Basic a very, very long time ago, when it was so inferior to
Delphi that I had  hard time understanding why it even existed, and I never
went back to it.

So, the first step was the usual one: "Hello World". Looking into that, I
realised that a command line program has the same level of complexity as a
full-blown GUI app, needing a project with a bunch of directories and files,
and being quite dependent on IDE. I don't like that (I prefer vim-editable
scripts), but since I decided to give Gambas a go, I went full GUI, something
which I did only 2 or 3 times since my Delphi days.

Overall impression: quite pleasant. The way to build GUI is simple and, save
from trying to find a good way to resize the window, I had no problem with it.
Writing the algorithm was also fairly simple, as always, with some help from
Google and Stackoverflow.

The problem itself was not too hard, but it required some effort and precision.
The worst part was not reading carefully, so my part 2 ended up with the value
off by 2 from the correct solution (I took some solution on the internet to
compare what is wrong, since my generate picture looked perfect to me). After
lots of eyeballing, I ended up using `diff` and realising that my solution
**is** indeed correct. The only problem was "within the range of y values in
your scan?". I applied that to bottom, but not to the top (as it makes no sense
to me), thus counting 2 tiles that were higher than the highest piece of clay.
Bummer.

Overall, if I ever need to make a GUI app, Gambas might be a way to go. It
would be nice to have Gampy... :-)
