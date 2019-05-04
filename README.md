# PyRandLib [![Latest release](http://img.shields.io/github/release/schmouk/pyrandlib.svg)](https://github.com/schmouk/pyrandlib/releases)
Many best in class pseudo random generators grouped into one simple library.



## License
PyRandLib is distributed under the MIT license for its largest use.
If you decide to use this library,  please add the copyright notice to  your
software as stated in the LICENSE file.

```
Copyright (c) 2016-2019 Philippe Schmouker, schmouk (at) typee.ovh

Permission is hereby granted,  free of charge,  to any person obtaining a copy
of this software and associated documentation files (the "Software"),  to deal
in the Software without restriction, including  without  limitation the rights
to use,  copy,  modify,  merge,  publish,  distribute, sublicense, and/or sell
copies of the Software,  and  to  permit  persons  to  whom  the  Software  is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS",  WITHOUT WARRANTY OF ANY  KIND,  EXPRESS  OR
IMPLIED,  INCLUDING  BUT  NOT  LIMITED  TO  THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT  SHALL  THE
AUTHORS  OR  COPYRIGHT  HOLDERS  BE  LIABLE  FOR  ANY CLAIM,  DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT,  TORT OR OTHERWISE, ARISING FROM,
OUT  OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```




## Intro
This library implements some of the best-in-class pseudo  random  generators
as  evaluated  by  Pierre L'Ecuyer  and Richard Simard in their famous paper
"TestU01:  A C library for empirical testing of  random  number  generators"
(ACM Trans. Math. Softw. Vol. 33 N.4, August 2007 -  see reference [1].  The 
reader will take benefit reading L'Ecuyer & Simard's paper.

Each of the Pseudo  Random  Generator (PRG) implemented in PyRandLib is self 
documented.  Names of classes directly refer to the kind of PRG they implem-
ent augmented with some number  characterizing  their  periodicity.  All  of 
their randomness characteristics are explained in every related module.


### Why not Mersenne twister?

The Mersenne twister PRG proposed by Matsumoto and Nishimura - see [5] -  is
the  most  widely  used  PRG.  The  Random  class of module random in Python 
implements this PRG.  It is  also  implemented  in  C++  and  Java  standard 
libraries for instance.

It offers a very good period (2^19937, i.e. about 4.3e6001).  Unfortunately, 
this PRG is a little bit long to compute (up to 3 times than LCGs,  60% more 
than LFibs and a little bit less than MRGs, see below at section 'Architect-
ure overview').  Moreover, it fails 4 of the hardest TestU01 tests.  You can 
still use it as your preferred PRG but PyRandLib implements many other  PRGs
which  are  either  far  faster  or far better in terms of generated pseudo-
randomness than the Mersenne twister PRG.



## Installation
Currently, the only way to install PyRandLib is  to  download  the  .zip  or
.tar.gz archive, then to directly put sub-directory 'PyRandLib' from archive
into directory 'site-packages',  in the main directory 'Lib' of your  Python 
environment.  See https://schmouk.github.io/PyRandLib/ for an easy access to
download versions or click on  tab  **releases**  on  home  page  of  GitHub 
repository.

A distribution version (to be installed via pip or easy-install in cmd  tool
or in console) is to come.



## Randomness evaluation
In [1], every known PRG at the time of the editing has been tested according
to three different sets of tests:
* _small crush_ is a small set of simple tests that quickly  tests  some  of
the expected characteristics for a pretty good PRG;
* _crush_ is a bigger set of tests that test  more  deeply  expected  random 
characteristics;
* _big crush_ is the ultimate set of  difficult  tests  that  any  GOOD  PRG 
should definitively pass.

We give you here below a copy of the resulting table for the PRGs that  have
been  implemented  in  PyRandLib  plus the Mersenne twister one which is not
implemented in PyRabdLib, as provided in [1].

 | PyRabndLib class | TU01 generator name                | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ---------------------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | FastRand32       | LCG(2^32, 69069, 1)                |     1 x 4-bytes | 2^32    |    3.20     |     0.67     |         11       |     106     |   *too many*   |
 | FastRand63       | LCG(2^63, 9219741426499971445, 1)  |     2 x 4-bytes | 2^63    |    4.20     |     0.75     |          0       |       5     |       7        |
 | MRGRand287       | Marsa-LFIB4                        |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | MRGRand1457      | DX-47-3                            |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | MRGRand49507     | DX-1597-2-7                        | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |
 | LFibRand78       | LFib(2^64, 17, 5, +)               |    34 x 4-bytes | 2^78    |    n.a.     |     1.1      |          0       |       0     |       0        |
 | LFibRand116      | LFib(2^64, 55, 24, +)              |   110 x 4-bytes | 2^116   |    n.a.     |     1.0      |          0       |       0     |       0        |
 | LFibRand668      | LFib(2^64, 607, 273, +)            | 1,214 x 4-bytes | 2^668   |    n.a.     |     0.9      |          0       |       0     |       0        |
 | LFibRand1340     | LFib(2^64, 1279, 861, +)           | 2,558 x 4-bytes | 2^1340  |    n.a.     |     0.9      |          0       |       0     |       0        |
 | Mersenne twister | MT19937                            |     6 x 4-bytes | 2^19937 |    4.30     |     1.6      |          0       |       2     |       2        |



## Implementation
Current implementation of PyRandLib uses Python 3.x with no Cython version.

Python 2.7 could be later available,  if asked for.  Cython  implementations
could also be later available.



## Architecture overview
Each of the implemented PRG is described in an independent module. The  name
of the module is directly related to the name of the related class.


### BaseRandom  -  the base class for all PRGs

**BaseRandom** is the base  class  for  every  implemented  PRG  in  library 
**PyRandLib**.  It inherits from the Python built-in class random.Random. It 
aims at providing simple common behavior for all PRG classes of the library, 
the  most  noticeable  one  being the 'callable' nature of every implemented 
PRGs. For instance:

    rand = UBaseRandom()
    print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
    print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
    print( rand(a,b) ) # prints a uniform pseudo-random value within [a, b)

Inheriting from the  Python  built-in  class  random.Random,  **BaseRandom**
provides  access  to  many  useful  distribution  functions  as described in 
later section **Inherited Distribution Functions**.

Furthermore, every inheriting class may override methods:

* random(),
* seed(),
* getrandbits(k),
* getstate() and
* setstate().

This lets inheriting classes implement the PRGs related core methods.



### FastRand32  -  2^32 periodicity

**FastRand32** implements a  Linear  Congruential  Generator  dedicated  to  
32-bits  calculations with very short period (about 4.3e+09) but very short 
time computation.

LCG models  evaluate  pseudo-random  numbers  suites  *x(i)*  as  a  simple 
mathematical function of *x(i-1)*:

    x(i) = ( a * x(i-1) + c ) mod m 
   
The implementation of **FastRand32** is based on  (*a*=69069, *c*=1)  since 
these  two  values  have  evaluated  to  be the 'best' ones for LCGs within
TestU01 while m = 2^32.
 
Results are nevertheless considered to be poor as stated in the  evaluation
done  by  Pierre  L'Ecuyer  and  Richard  Simard.   Therefore,  it  is  not 
recommended  to  use  such pseudo-random  numbers  generators  for  serious  
simulation applications.

See FastRand63 for a 2^63 (i.e. about 9.2e+18) period LC-Generator with low 
computation time and 'better' randomness characteristics.



### FastRand63  -  2^63 periodicity

**FastRand63** implements a  Linear  Congruential  Generator  dedicated  to  
63-bits  calculations  with  a short period  (about 9.2e+18) and very short 
time computation.

LCG  models  evaluate  pseudo-random  numbers  suites *x(i)*  as  a  simple 
mathematical function of *x(i-1)*:

    x(i) = ( a * x(i-1) + c ) mod m 
   
The implementation of this LCG 63-bits model is based on (*a*=9219741426499971445, *c*=1) 
since these two values have evaluated to be the 'best' ones for LCGs within
TestU01 while *m* = 2^63.
 
Results are nevertheless considered to be poor as stated in the  evaluation
done  by  Pierre  L'Ecuyer  and  Richard  Simard.   Therefore,  it  is  not 
recommended  to  use  such  pseudo-random  numbers  generators  for serious  
simulation applications,  even if FastRandom63 fails on very far less tests 
than does FastRandom32.

See FastRand32 for a 2^32 period (i.e. about 4.3e+09) LC-Generator with 25%
lower computation time.



### MRGRand287  -  2^287 periodicity

**MRGRand287** implements a fast 32-bits Multiple Recursive Generator (MRG)
with a long period  (2^287, i.e. 2.49e+86)  and low computation time (about
twice  the  computation  time  of  above  LCGs)  but  256  integers  memory 
consumption.

Multiple  Recursive   Generators   (MRGs)   use  recurrence   to   evaluate  
pseudo-random  numbers  suites.  For  2  to  more  different values of *k*, 
recurrence is of the form:

    x(i) = A * SUM[ x(i-k) ]  mod M

MRGs offer very large periods with the best known results in the evaluation  
of their randomness, as evaluated by Pierre L'Ecuyer and Richard Simard. It 
is  therefore  strongly  recommended  to  use  such  pseudo-random  numbers  
generators rather than LCG ones for serious simulation applications.

The implementation of this MRG 32-bits model is finally based on  a  Lagged  
Fibonacci generator (LFIB), the Marsa-LFIB4 one.

Lagged Fibonacci generators *LFib( m, r, k, op)* use the recurrence

    x(i) = ( x(i-r) op (x(i-k) ) mod m

where op is an operation that can be
    + (addition),
    - (substraction),
    * (multiplication),
    ^(bitwise exclusive-or).
    
With the + or - operation, such generators are true MRGs.  They offer  very 
large periods  with  the  best  known  results  in  the evaluation of their 
randomness,  as evaluated by Pierre L'Ecuyer and  Richard Simard  in  their 
paper.

The  Marsa-LIBF4  version,  i.e. **MRGRand287**  implementation,  uses  the 
recurrence:

    x(i) = ( x(i-55) + x(i-119) + x(i-179) + x(i-256) ) mod 2^32



### MRGRand1457  -  2^1457 periodicity

**MRGRand1457** implements a fast 31-bits Multiple Recursive Generator with
a longer period than MRGRan287 (2^1457 vs. 2^287, i.e. 4.0e+438 vs. 2.5e+86)
and 80 % more computation time but with much less memory space  consumption 
(47 vs. 256 integers).
   
The  implementation  of  this  MRG  31-bits  model  is  based  on   DX-47-3  
pseudo-random   generator  proposed  by Deng and Lin, see [2].  The DX-47-3 
version uses the recurrence:

    x(i) = (2^26+2^19) * ( x(i-1) + x(i-24) + x(i-47) ) mod (2^31-1)



### MRGRand49507  -  2^49507 periodicity

**MRGRand49507** implements a fast 31-bits Multiple Recursive Generator with
the  longer  period of all of the PRGs that are implemented if **PyRandLib**
(2^49507,  i.e. 1.2e+14903)  with low computation time  also  (same  as  for
MRGRand287) but use of much more memory space (1597 integers).
     
The implementation of this MRG 31-bits model is based on the 'DX-1597-2-7' 
MRG proposed by Deng, see [3]. It uses the recurrence:

    x(i) = (-2^25-2^7) * ( x(i-7) + x(i-1597) ) mod (2^31-1)



### LFibRand78  -  2^78 periodicity

**LFibRand78** implements a fast 64-bits Lagged Fibonacci generator (LFib).
Lagged Fibonacci generators *LFib( m, r, k, op)* use the recurrence

    x(i) = ( x(i-r) op (x(i-k) ) mod m

where op is an operation that can be
    + (addition),
    - (substraction),
    * (multiplication),
    ^(bitwise exclusive-or).

With the + or - operation, such generators are MRGs.  They offer very large
periods  with the best known results in the evaluation of their randomness, 
as stated in the evaluation  done  by  Pierre L'Ecuyer  and  Richard Simard
while offering very low computation times.

The implementation of   **LFibRand78**  is  based  on  a  Lagged  Fibonacci 
generator (LFib) which uses the recurrence:

    x(i) = ( x(i-5) + x(i-17) ) mod 2^64

It offers a period of about 2^78 - i.e. 3.0e+23 - with low computation time
due  to  the use of a 2^64 modulo  (less than twice the computation time of
LCGs) and low memory consumption (17 integers).

Please notice that the TestUO1 article states that the operator  should  be 
'*'  while  George Marsaglia  in its original article [4] used the operator 
'+'. We've implemented in **PyRandLib**  the original operator '+'.



### LFibRand116  -  2^116 periodicity

**LFibRand116** implements an LFib 64-bits  generator  proposed  by  George
Marsaglia in [4]. This PRG uses the recurrence

    x(i) = ( x(i-24) + x(i-55) ) mod 2^64
    
It offers a period of about 2^116  - i.e. 8.3e+34 -  with  low  computation 
time  due to the use of a 2^64 modulo (less than twice the computation time 
of LCGs) and some memory consumption (55 integers).

Please notice that the TestUO1 article states that the operator  should  be 
'*'  while  George Marsaglia  in its original article [4] used the operator 
'+'. We've implemented in **PyRandLib**  the original operator '+'.



### LFibRand668  -  2^668 periodicity

**LFibRand668** implements an LFib 64-bits  generator  proposed  by  George
Marsaglia in [4]. This PRG uses the recurrence

    x(i) = ( x(i-273) + x(i-607) ) mod 2^64
    
It offers a period of about 2^668  - i.e. 1.2e+201 -  with low  computation 
time  due to the use of a 2^64 modulo (less than twice the computation time 
of LCGs) and much memory consumption (607 integers).

Please notice that the TestUO1 article states that the operator  should  be 
'*'  while  George Marsaglia  in its original article [4] used the operator 
'+'. We've implemented in **PyRandLib**  the original operator '+'.



### LFibRand1340

**LFibRand1340** implements an LFib 64-bits generator  proposed  by  George
Marsaglia in [4]. This PRG uses the recurrence

    x(i) = ( x(i-861) + x(i-1279) ) mod 2^64
    
It offers a period of about 2^1340 - i.e. 2.4e+403 -  with low  computation 
time  due to the use of a 2^64 modulo (less than twice the computation time 
of LCGs) and much more memory consumption (1279 integers).

Please notice that the TestUO1 article states that the operator  should  be 
'*'  while  George Marsaglia  in its original article [4] used the operator 
'+'. We've implemented in **PyRandLib**  the original operator '+'.




## Inherited Distribution and Generic Functions
(some of next explanation may be free to exact copy of Python 3.6 documentation.
See https://docs.python.org/3.6/library/random.html?highlight=random#module-random)

Since the base  class  **BaseRandom**  inherits  from  the  built-in  class 
random.Random,  every  PRG  class of **PyRandLib** gets automatic access to 
the next distribution and generic methods:


**betavariate**(self, alpha, beta)

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.


**choice**(self, seq)

Chooses a random element from a non-empty sequence.  'seq' has  to  be  non 
empty.


**choices**(population, weights=None, *, cum_weights=None, k=1)

Returns a k  sized  list  of  elements  chosen  from  the  population  with  
replacement. If the population is empty, raises IndexError.

If a weights sequence is specified,  selections are made according  to  the 
relative weights.  Alternatively,  if a cum_weights sequence is given,  the 
selections are made according to the cumulative weights  (perhaps  computed 
using   itertools.accumulate()).   For   example,   the   relative  weights 
[10, 5, 30, 5] are equivalent to the cumulative  weights  [10, 15, 45, 50]. 
Internally, the relative weights are converted to cumulative weights before 
making selections, so supplying the cumulative weights saves work.

If neither weights nor cum_weights are specified,  selections are made with 
equal probability.  If a weights sequence is supplied,  it must be the same 
length as the population sequence.  It  is  a  TypeError  to  specify  both 
weights and cum_weights.

The weights or cum_weights can use any numeric type that interoperates with 
the float values returned by random()  (that includes integers, floats, and 
fractions but excludes decimals).

Notice:  'choices'  has  been  provided  since  Python 3.6.  It  should  be 
implemented for older versions.


**expovariate**(self, lambd)

Exponential distribution.

lambd is 1.0 divided by the desired  mean.   It  should  be  nonzero.  (The 
parameter  should  be  called  "lambda",  but  this  is  a reserved word in 
Python.)  Returned values range from 0 to positive  infinity  if  lambd  is 
positive, and from negative infinity to 0 if lambd is negative.


**gammavariate**(self, alpha, beta)

Gamma distribution.  Not the gamma function!
    
Conditions on the parameters are alpha > 0 and beta > 0.


**gauss**(self, mu, sigma)

Gaussian distribution.

mu is the mean, and sigma is the standard deviation.
This is slightly faster than the normalvariate() function.

Not thread-safe without a lock around calls.


**getrandbits(self, k)**

Returns a Python integer with k random bits. Inheriting generators may also 
provide it as an optional part of their API.  When available, getrandbits() 
enables randrange() to handle arbitrarily large ranges.


**getstate**(self)

Returns internal state; can be passed to setstate() later.


**lognormvariate**(self, mu, sigma)

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a normal 
distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.


**normalvariate**(self, mu, sigma)

Normal distribution.

mu is the mean, and sigma is the standard deviation. See method gauss() for 
a faster but not thread-safe equivalent.


**paretovariate**(self, alpha)

Pareto distribution.  alpha is the shape parameter.


**randint**(self, a, b)

Returns a random integer in range [a, b], including both end points.


**randrange**(self, stop)

**randrange**(self, start, stop=None, step=1)

Returns a randomly selected element from range(start, stop, step).  This is 
equivalent  to  choice( range(start, stop, step) ) without building a range 
object.

The positional argument pattern matches that of range().  Keyword arguments 
should not be used because the function may use them in unexpected ways.


**sample**(self, population, k)

Chooses k unique random elements from a population sequence or set.

Returns a new list containing elements from the  population  while  leaving 
the  original  population  unchanged.  The  resulting  list is in selection 
order so that all sub-slices will also be valid random samples. This allows 
raffle  winners  (the sample) to be partitioned into grand prize and second 
place winners (the subslices).

Members of the population need not be hashable or unique. If the population 
contains  repeats,  then  each  occurrence  is  a possible selection in the 
sample.

To choose a sample in a range of integers, use range as an  argument.  This 
is   especially  fast  and  space  efficient  for  sampling  from  a  large 
population: sample(range(10000000), 60)


**seed**(self, a=None, version=2)

Initialize internal state from hashable object.

None or no argument seeds from current time or  from  an  operating  system 
specific randomness source if available.

For version 2 (the default), all of the bits are used  if  *a*  is  a  str,
bytes, or bytearray.  For version 1, the hash() of *a* is used instead.

If *a* is an int, all bits are used.


**setstate**(self, state)

Restores internal state from object returned by getstate().


**shuffle**(self, x, random=None)

Shuffle the sequence x in place. Returns None.

The optional argument random is a 0-argument function  returning  a  random 
float in [0.0, 1.0); by default, this is the function random().

To shuffle an immutable sequence  and  return  a  new  shuffled  list,  use 
sample(x, k=len(x)) instead.

Note that even for small len(x),  the total number of permutations of x can 
quickly grow larger than the period of most random number generators.  This 
implies that most permutations of a long sequence can never  be  generated. 
For  example,  a sequence of length 2080 is the largest that can fit within 
the period of the Mersenne Twister random number generator.


**triangular**(self, low=0.0, high=1.0, mode=None)

Triangular distribution.

Continuous distribution bounded by given lower and upper limits, and having 
a  given mode value in-between.  Returns a random floating point number *N* 
such that low <= *N* <= high and with  the  specified  mode  between  those 
bounds.  The low and high bounds default to zero and one. The mode argument 
defaults  to  the  midpoint  between  the  bounds,   giving   a   symmetric 
distribution.

http://en.wikipedia.org/wiki/Triangular_distribution


**uniform**(self, a, b)

Gets a random number in the range [a, b) or [a, b] depending on rounding.


**vonmisesvariate**(self, mu, kappa)

Circular data distribution.

mu is the mean angle, expressed in radians between 0 and 2*pi, and kappa is 
the  concentration parameter,  which must be greater than or equal to zero. 
If kappa is equal to zero,  this distribution reduces to a  uniform  random 
angle over the range 0 to 2*pi.


**weibullvariate**(self, alpha, beta)

Weibull distribution.

alpha is the scale parameter and beta is the shape parameter.



## References

**[1]** Pierre L'Ecuyer and Richard Simard. 2007. 
*TestU01: A C library for empirical testing of random number generators*. 
ACM Transaction on Mathematical Software, Vol.33 N.4, Article 22 (August 2007), 40 pages. DOI: http://dx.doi.org/10.1145/1268776.1268777

BibTex:
@article{L'Ecuyer:2007:TCL:1268776.1268777,
 author = {L'Ecuyer, Pierre and Simard, Richard},
 title = {TestU01: A C Library for Empirical Testing of Random Number Generators},
 journal = {ACM Trans. Math. Softw.},
 issue_date = {August 2007},
 volume = {33},
 number = {4},
 month = aug,
 year = {2007},
 issn = {0098-3500},
 pages = {22:1--22:40},
 articleno = {22},
 numpages = {40},
 url = {http://doi.acm.org/10.1145/1268776.1268777},
 doi = {10.1145/1268776.1268777},
 acmid = {1268777},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Statistical software, random number generators, random number tests, statistical test},
}  


**[2]** Lih-Yuan Deng  &  Dennis K. J. Lin. 2000. 
*Random number generation for the new century*. 
The American Statistician Vol.54, N.2, pp. 145–150.

BibTex:
@article{doi:10.1080/00031305.2000.10474528,
author = { Lih-Yuan   Deng  and  Dennis K. J.   Lin },
title = {Random Number Generation for the New Century},
journal = {The American Statistician},
volume = {54},
number = {2},
pages = {145-150},
year = {2000},
doi = {10.1080/00031305.2000.10474528},
URL = {ttp://amstat.tandfonline.com/doi/abs/10.1080/00031305.2000.10474528},
eprint = {http://amstat.tandfonline.com/doi/pdf/10.1080/00031305.2000.10474528}
}


**[3]** Lih-Yuan Deng. 2005.
*Efficient and portable multiple recursive generators of large order*.
ACM Transactions on Modeling and Computer. Simulation 15:1.


**[4]** Georges Marsaglia. 1985. 
*A current view of random number generators*.
In Computer Science and Statistics, Sixteenth Symposium on the Interface. Elsevier Science Publishers, North-Holland,
Amsterdam, 1985, The Netherlands. pp. 3–10.


**[5]** Makoto Matsumoto and Takuji Nishimura. 1998. 
*Mersenne twister: A 623-dimensionally equidistributed uniform pseudo-random number generator.*
In ACM Transactions on Modeling and Computer Simulation (TOMACS) - Special issue on uniform random number generation.  
Vol.8 N.1, Jan. 1998, pp. 3-30.  
