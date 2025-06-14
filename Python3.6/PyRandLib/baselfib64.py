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
from typing import Final

from .listindexstate   import ListIndexState
from .annotation_types import Numerical, SeedStateType, StateType
from .splitmix         import SplitMix64


#=============================================================================
class BaseLFib64( ListIndexState ):
    """The base class for all LFib PRNG based on 64-bits numbers.
    
    Definition of the base class for all LFib pseudo-random generators based
    on 64-bits generated numbers.

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
       
    See LFib78,  LFib116,  LFib668 and LFib1340 for long period LFib generators (resp. 
    2^78,  2^116,  2^668 and 2^1340 periods, i.e. resp. 3.0e+23, 8.3e+34, 1.2e+201 and 
    2.4e+403 periods) while same computation time and far  higher  precision  (64-bits  
    calculations) than MRGs,  but more memory consumption (resp. 17,  55, 607 and 1279 
    integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseLFib()   # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attribute '_STATE_SIZE'. See LFib78 for an
    example.

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
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
    _NORMALIZE: Final[float] = 5.421_010_862_427_522_170_037_3e-20  # i.e. 1.0 / (1 << 64)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: Final[int] = 64
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    #-------------------------------------------------------------------------
    def __init__(self, _stateSize: int, _seedState: SeedStateType = None) -> None:
        """Constructor.
        
        _stateSize is the size of the internal state list of integers.
        _seedState is either a valid state, an integer,  a float or None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._STATE_SIZE  64-bits  integers  and  an  index  in this list 
        (index value being  then  in range (0,self._STATE_SIZE)).  Should 
        _seedState be a sole integer or float then it is used as  initial
        seed for the random filling of the internal list of self._STATE_SIZE  
        integers.  Should _seedState be anything else  (e.g.  None)  then  
        the  shuffling of the local current time value is used as such an 
        initial seed.
        """
        super().__init__( SplitMix64, _stateSize, _seedState )
            # this  call  creates  the  two   attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().


    #-------------------------------------------------------------------------
    def seed(self, _seed: Numerical) -> None:
        super().seed( _seed )


    #-------------------------------------------------------------------------
    def setstate(self, _state: StateType) -> None:
        super().setstate(_state)


#=====   end of module   baselfib64.py   =====================================
