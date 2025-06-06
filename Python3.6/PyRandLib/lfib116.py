"""
Copyright (c) 2016-2025 Philippe Schmouker, ph (dot) schmouker (at) gmail.com

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
from .baselfib64       import BaseLFib64
from .annotation_types import SeedStateType


#=============================================================================
class LFib116( BaseLFib64 ):
    """
    Pseudo-random numbers generator  -  Definition of a fast 64-bits Lagged  Fibonacci 
    Generator with quite short period (8.3e+34).

    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

    Lagged Fibonacci generators LFib( m, r, k, op) use the recurrence
    
        x(i) = (x(i-r) op (x(i-k)) mod m
    
    where op is an operation that can be:
        + (addition),
        - (substraction),
        * (multiplication),
        ^ (bitwise exclusive-or).
    
    With the + or - operation, such generators are in fact MRGs. They offer very large
    periods  with  the  best  known  results in the evaluation of their randomness, as
    stated in the evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de
    Montreal)  in  "TestU01:  A  C  Library  for Empirical Testing  of  Random  Number  
    Generators - ACM Transactions  on  Mathematical  Software,  vol.33 n.4,  pp.22-40, 
    August 2007".  It  is  recommended  to  use  such pseudo-random numbers generators 
    rather than LCG ones for serious simulation applications.

    The implementation of this LFib 64-bits model  is  based  on  a  Lagged  Fibonacci 
    generator (LFIB) that uses the recurrence
    
        x(i) = (x(i-24) + x(i-55)) mod 2^64
    
    and offers a period of about 2^116 - i.e. 8.3e+34 - with low computation time  due
    to  the  use  of a 2^64 modulo and little memory space consumption (55 long integ-
    ers).
    
    Please notice that the TestUO1 article states that  the  operator  should  be  '*' 
    while Mascagni & Srinivasan  in their original article stated that the operator is 
    '+'.  We've implemented here the original operator: '+'.
       
    See LFib78,  LFib668 and LFib1340 for long period  LFib  generators  (resp.  2^78,  
    2^668  and  2^1340  periods,  i.e. resp. 3.0e+23,  1.2e+201  and 2.4e+403 periods) 
    while same computation time and far higher precision (64-bits  calculations)  than  
    MRGs,  but memory consumption (resp. 17, 607 and 1279 integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = LFib116()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = LFib116()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LFibs that have 
    been implemented in PyRandLib,  as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRandLib class | TU01 generator name      | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------------ | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | LFib78          | LFib(2^64, 17, 5, +)     |    34 x 4-bytes | 2^78    |    n.a.     |     1.1      |          0       |       0     |       0        |
 | LFib116         | LFib(2^64, 55, 24, +)    |   110 x 4-bytes | 2^116   |    n.a.     |     1.0      |          0       |       0     |       0        |
 | LFib668         | LFib(2^64, 607, 273, +)  | 1,214 x 4-bytes | 2^668   |    n.a.     |     0.9      |          0       |       0     |       0        |
 | LFib1340        | LFib(2^64, 1279, 861, +) | 2,558 x 4-bytes | 2^1340  |    n.a.     |     0.9      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    def __init__(self, _seed: SeedStateType = None,) -> None:
        """Constructor.
        
        Should _seed be None or not a number then the local time is used
        (with its shuffled value) as a seed.
        """
        # this 'LFib(2^64, 55, 24, +)' generator is based on a suite containing 55 integers
        super().__init__( 55, _seed )


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # evaluates indexes in suite for the i-24 and i-55 -th values
        if (k24 := self._index-24) < 0:
            k24 += self._STATE_SIZE  # notice: attribute _STATE_SIZE is set in base class
        
        # then evaluates current value
        self._state[self._index] = (myValue := (self._state[k24] + self._state[self._index]) & 0xffff_ffff_ffff_ffff)
        
        # next index
        self._index = (self._index+1) % self._STATE_SIZE

        return myValue


#=====   end of module   lfib116.py   ========================================
