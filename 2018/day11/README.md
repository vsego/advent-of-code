# Day 11: [Scilab](https://www.scilab.org/) and
[PostgreSQL](https://www.postgresql.org/) (kinda)

The problem has some tables of numbers, so it seemed like a good chance to give
PostgreSQL a shot. And it worked... kinda. The final solution takes some 5
hours to run, so it did finish during my night's sleep, but it felt a bit...
unsatisfying.

Thinking a bit more about the problem, I realised that it has a very elegant
linear algebra solution. Basically, we start with a matrix X and then search
for maximums in sum(X(ij)), where X(ij) denotes a matrix shifted by i rows and
j columns (first i rows and j columns get lost, and the ones at the end get
filled with zeros to maintain the dimensions). But that sum is trivially
computed using matrix multiplication:

![sum(X(ij)) = T X T^T](http://www.sciweavers.org/tex2img.php?eq=%5Csum_%7Bi%2Cj%3D0%7D%5Ek%20X%28i%2Cj%29%20%3D%20T%20X%20T%5ET%2C&bc=White&fc=Black&im=png&fs=12&ff=arev&edit=0)

where T (a transformation matrix) is a banded upper-triangular matrix of ones
on it's band of width k+1, i.e.,

![Tij = {1, 0&le;j - i\&le;; 0, otherwise}](http://www.sciweavers.org/tex2img.php?eq=T_%7Bi%2Cj%7D%20%3D%20%5Cbegin%7Bcases%7D%201%2C%20%26%200%20%5Cle%20j%20-%20i%20%5Cle%20k%20%5C%5C%200%2C%20%26%20%5Ctext%7Botherwise%7D.%20%5Cend%7Bcases%7D&bc=White&fc=Black&im=png&fs=12&ff=arev&edit=0)

With that in mind, Scilab (another free Matlab alternative) seemed like an
obvious choice, and it really was a good one. The code is nice and clear, it
wasn't too hard to come up with it (even though I had no prior experience with
the language), and it ran fast and smoothly.
