# Day 14: [Java](https://www.java.com/)

Another one that I first tried in newLISP, but couldn't get it to perform in
reasonable time, so I went with a different language. This time: Java.

This is the first Java program I wrote since I had to do it for a university
class, some 20 years ago. Like C++, I hated it then and, also like C++, Java
turned out to be a much more pleasant experience than I expected.

This problem is another case of "simple to design, but a bit of a challenge to
implement". The main thing to notice is that it cannot be done with dequeue,
but the moving in the list is done by a small number of steps, making linked
list a natural choice of a data structure.

The only snag I've hit was the fact that adding stuff to linked lists while
iterating them is not possible, which doesn't make much sense to me (I would
understand the inability to delete, but not to add stuff).

Since Java's `LinkedList` didn't meet my needs, I implemented my own, something
I also haven't done for many years. The result is quite satisfying. Maybe not
super-fast, but fast enough, finishing in some 8 seconds on my old desktop.
