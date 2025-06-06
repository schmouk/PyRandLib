"""
Copyright (c) 2016-2025 Philippe Schmouker, schmouk (at) gmail.com

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
"""

#=============================================================================
from typing import override

from .basemrg          import BaseMRG
from .annotation_types import SeedStateType
from .splitmix         import SplitMix32


#=============================================================================
class Mrg287( BaseMRG ):
    """
    Pseudo-random numbers generator  - Definition of a fast 32-bits Multiple Recursive
    Generator with a long period (2.49e+86).

    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

    Multiple Recursive Generators (MRGs)  use  recurrence  to  evaluate  pseudo-random
    numbers suites. Recurrence is of the form:
    
       x(i) = A * SUM[ x(i-k) ]  mod M
    
    for 2 to more k different values.

    MRGs offer very large periods with the best known results  in  the  evaluation  of 
    their  randomness,  as  stated  in  the  evaluation  done  by  Pierre L'Ecuyer and 
    Richard Simard (Universite de Montreal)  in "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.

    The implementation of this MRG 32-bits  model  is  based  on  a  Lagged  Fibonacci 
    generator (LFIB), the Marsa-LFIB4 one.
    Lagged Fibonacci generators LFib( m, r, k, op) use the recurrence
    
        x(i) = (x(i-r) op (x(i-k)) mod m
    
    where op is an operation that can be
        + (addition),
        - (substraction),
        * (multiplication),
        ^ (bitwise exclusive-or).
    
    With the + or - operation, such generators are in fact MRGs. They offer very large
    periods  with  the  best  known  results in the evaluation of their randomness, as
    stated in the evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de
    Montreal) paper.
    
    The Marsa-LIBF4 version uses the recurrence
    
        x(i) = (x(i-55) + x(i-119) + x(i-179) + x(i-256)) mod 2^32
    
    and offers a period of about 2^287 - i.e. 2.49e+86 - with low computation time due
    to the use of a 2^32 modulo.
    
    See Mrg1457 for a longer period MR-Generator  (2^1457,  i.e. 4.0e+438)  and longer
    computation  time  (2^31-1 modulus calculations) but less memory space consumption 
    (47 integers).
    See Mrg49507 for  a  far  longer  period  (2^49507,  i.e. 1.2e+14903)  with  lower 
    computation  time  too  (31-bits  modulus)  but  use  of  more memory space (1_597 
    integers).
      
    Furthermore, this class is callable:
      rand = Mrg287()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = Mrg287()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of the inherited 
    methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the MRGs  that  have  been
    implemented in PyRandLib, as provided in paper "TestU01, ..." - see file README.md.

 | PyRandLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Mrg287          | Marsa-LFIB4         |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | Mrg1457         | DX-47-3             |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | Mrg49507        | DX-1597-2-7         | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    def __init__(self, _seed: SeedStateType = None, /) -> None:
        """Constructor.
        
        Should _seed be None or not a number then the local time is used
        (with its shuffled value) as a seed.
        """
        # this 'Marsa-LIBF4' generator is based on a suite containing 256 integers
        super().__init__( SplitMix32, 256, _seed )


    #-------------------------------------------------------------------------
    @override
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # The Marsa-LIBF4 version uses the recurrence
        #    x(i) = (x(i-55) + x(i-119) + x(i-179) + x(i-256)) mod 2^32

        # evaluates indexes in suite for the i-55, i-119, i-179 (and i-256) -th values
        if (k55 := self._index-55) < 0:
            k55 += self._STATE_SIZE  # notice: attribute _STATE_SIZE is set in base class
        
        if (k119 := self._index-119) < 0:
            k119 += self._STATE_SIZE
        
        if (k179 := self._index-179) < 0:
            k179 += self._STATE_SIZE
        
        # then evaluates current value
        self._state[self._index] = (myValue := (self._state[k55] + self._state[k119] + self._state[k179] + self._state[self._index]) & 0xffff_ffff)
        
        # next index
        self._index = (self._index + 1) % self._STATE_SIZE
        
        # then returns the integer generated value
        return  myValue


#=====   end of module   mrgrand287.py   ==================================
