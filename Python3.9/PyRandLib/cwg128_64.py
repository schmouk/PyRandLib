"""
Copyright (c) 2025 Philippe Schmouker, ph (dot) schmouker (at) gmail.com

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

from .basecwg          import BaseCWG
from .annotation_types import Numerical, SeedStateType, StateType
from .splitmix         import SplitMix64


#=============================================================================
class Cwg128_64( BaseCWG ):
    """
    Pseudo-random numbers  generator  -  Collatz-Weyl  pseudorandom  Generator
    dedicated  to  128-bits  calculations and 64-bits output values with small
    period (min 2^64, i.e. 1.84e+19)  but  short  computation  time.  All  CWG
    algorithms offer multi streams features, by simply using different initial
    settings for control value 's' - see below.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

*   This CWG model evaluates pseudo-random numbers suites  x(i)  as  a  simple
*   mathematical function of
    
        x(i+1) = (x(i) | 1) * ((a += x(i)) >> 1) ^ (weyl += s) 

    and returns as the output value the xored shifted: a >> 48 ^ x(i+1)

    where a, weyl and s are the control values and x the internal state of the
    PRNG.  's' must be initally odd.  'a', 'weyl' and initial state 'x' may be 
    initialized each with any 64-bits value.
    
    See Cwg64 for a minimum  2^64  (i.e. about 1.84e+19)  period  CW-Generator 
    with  very low computation time, medium period,  64 bits output values and 
    very good randomness characteristics.
    
    See Cwg128 for a minimum 2^128 (i.e. about 6.81e+38)  period  CW-generator
    with very low computation time, medium period,  128 bits output values and 
    very good randomness characteristics.

    Furthermore this class is callable:
      rand = Cwg128_64()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for  the  CWGs  that  have 
    been implemented in PyRandLib, as presented in paper [8] - see file README.md.

 | PyRandLib class | [8] generator name | Memory Usage  | Period   | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------ | ------------- | -------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Cwg64           | CWG64              |   8 x 4-bytes | >= 2^64  |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Cwg128_64       | CWG128_64          |  10 x 4-bytes | >= 2^64  |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Cwg128          | CWG128             |  16 x 4-bytes | >= 2^128 |    n.a.     |     n.a.     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    

    #-------------------------------------------------------------------------
    _NORMALIZE: Final[float] = 5.421_010_862_427_522_170_037_3e-20  # i.e. 1.0 / (1 << 64)  # type: ignore
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: Final[int] = 64  # type: ignore
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    #-------------------------------------------------------------------------
    def __init__(self, _seedState: SeedStateType = None, /) -> None:  # type: ignore
        """Constructor. 
        
        Should _seedState be None then the local time is used as a seed  (with 
        its shuffled value).
        """
        super().__init__( _seedState )  # this internally calls 'setstate()'  which
                                        # MUST be implemented in inheriting classes


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # evaluates next internal state
        self._a = (self._a + self._state) & 0xffff_ffff_ffff_ffff
        self._weyl = (self._weyl + self._s) & 0xffff_ffff_ffff_ffff
        self._state = (((self._state | 1) * (self._a >> 1)) ^ self._weyl) & 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff
        # returns the xored-shifted output value
        return self._state ^ (self._a >> 48)


    #-------------------------------------------------------------------------
    def seed(self, _seed: Numerical = None, /) -> None:  # type: ignore
        """Initiates the internal state of this pseudo-random generator.
        """
        if _seed is None:
            self._seed()

        elif isinstance(_seed, int):
            self._seed(_seed)

        elif isinstance(_seed, float):
            if 0.0 <= _seed <= 1.0:
                self._seed( int(_seed * 0xffff_ffff_ffff_ffff) )
            else:
                raise ValueError(f"Float seeds must be in range [0.0, 1.0] (currently is {_seed})")

        else:
            raise TypeError(f"Seeding value must be None, an int or a float (currently is {type(_seed)})")


    #-------------------------------------------------------------------------
    def _seed(self, s: int = None, /) -> None:  # type: ignore
        """Sets the internal state of this pseudo-random generator.
        """
        if s is None or abs(s) < (1 << 64):
            initRand = SplitMix64( s )
            self._a = self._weyl = 0
            self._s = initRand() | 1                        # Notice: s must be odd
            self._state = (initRand() << 64) | initRand()   # Notice: coded on 128 bits
        
        else:
            initRandLo = SplitMix64( s & 0xffff_ffff_ffff_ffff )
            initRandHi = SplitMix64( (s >> 64) & 0xffff_ffff_ffff_ffff )
            self._a = self._weyl = 0
            self._s = initRandLo() | 1                          # Notice: s must be odd
            self._state = (initRandHi() << 64) | initRandLo()   # Notice: coded on 128 bits


    #-------------------------------------------------------------------------
    def setstate(self, _state: StateType = None, /) -> None:  # type: ignore
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called. If None, the local system time
        is used instead.
        """
        if _state is None:
            self.seed()

        elif not isinstance( _state, (list, tuple) ):
            raise TypeError(f"initialization state must be a tuple or a list (actually is {type(_state)})")
                
        elif len(_state) == 4:
            # each entry in _seedState MUST be a positive or null integer
            if not all(isinstance(s, int) and s >= 0 for s in _state):
                raise ValueError(f"all values of internal state must be single non negative integers: {_state}")
            else:
                self._a     =  _state[0] & 0xffff_ffff_ffff_ffff
                self._weyl  =  _state[1] & 0xffff_ffff_ffff_ffff
                self._s     = (_state[2] & 0xffff_ffff_ffff_ffff) | 1  # Notice: must be odd
                self._state =  _state[3] & ((1 << 128) - 1)            # Notice: coded on 128 bits
            
        else:
            raise ValueError(f"Incorrect size for initializing state (should be 4 integers, currently is {len(_state)})")


#=====   end of module   cwg128_64.py   ======================================
