"""
Copyright (c) 2025 Philippe Schmouker, schmouk (at) gmail.com

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
from .annotation_types import SeedStateType
from .splitmix         import SplitMix32


#=============================================================================
class BaseWELL( ListIndexState ):
    """Definition of the base class for all WELL pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    Well-Equidistributed Long-period Linear Generators (WELL)  use  linear  recurrence 
    based  on  primitive  characteristic  polynomials associated with left- and right- 
    shifts and xor operations to fastly evaluate pseudo-random numbers suites.
    
    WELLs offer large to very large periods with best known results in the  evaluation 
    of their randomness,  as stated in the evaluation  done  by  Pierre  L'Ecuyer  and 
    Richard Simard (Universite de Montreal) in  "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.
    Furthermore, WELLs have proven their great ability  to  very  fastly  escape  from 
    zeroland.

    Notice: the algorithm in the 4 different versions implemented here has been  coded 
    here  as  a  direct  implementation  of  their  descriptions  in the initial paper 
    "Improved Long-Period Generators Based on Linear Recurrences  Modulo 2",  François  
    PANNETON  and  Pierre  L’ECUYER  (Université  de  Montréal)  and  Makoto MATSUMOTO 
    (Hiroshima University),  in ACM Transactions on  Mathematical  Software,  Vol. 32, 
    No. 1, March 2006, Pages 1–16.
    (see https://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf).
    So,  only minimalist optimization has been coded,  with  the  aim  at  easing  the 
    verification of its proper implementation.
       
    See Well512a for a large period WELL-Generator (2^512,  i.e. 1.34e+154)  with  low
    computation time and 16 integers memory little consumption.
    See Well1024a for a longer period WELL-Generator  (2^1024,  i.e. 2.68e+308),  same 
    computation time and 32 integers memory consumption.
    See Well199937b for a far longer period  (2^19937,  i.e. 4.32e+6001) with  similar 
    computation time but use of more memory space (624 integers).
    See Well44497c for a very large period (2^44497,  i.e. 15.1e+13466)  with  similar 
    computation time but use of even more memory space (1,391 integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseWell()   # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attributes '_STATE_SIZE'. See Well512a for 
    an example.

    Reminder:
    We give you here below a copy of the table of tests for the WELL  algorithms  that 
    have  been implemented in PyRandLib,  as provided in paper "TestU01, ..." and when 
    available.

 | PyRandLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Well512a        | not available       |    16 x 4-bytes | 2^512   |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |
 | Well1024a       | WELL1024a           |    32 x 4-bytes | 2^1024  |    4.0      |     1.1      |          0       |       4     |       4        |
 | Well19937b (1)  | WELL19937a          |   624 x 4-bytes | 2^19937 |    4.3      |     1.3      |          0       |       2     |       2        |
 | Well44497c      | not available       | 1,391 x 4-bytes | 2^44497 |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |

    (1)The Well19937b generator provided with library PyRandLib implements the
    Well19937a algorithm augmented with an associated tempering algorithm.

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _stateSize: int, _seedState: SeedStateType = None, /) -> None:
        """Constructor.
        
        _stateSize is the size of the internal state list of integers.
        _seedState is either a valid state, an integer, a float or  None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._STATE_SIZE integers and an index in this list (index  value 
        being  then  in range(0,self._STATE_SIZE)).  Should _seedState be 
        a sole integer or float then it is used as initial seed  for  the 
        random filling of the internal list of self._STATE_SIZE integers. 
        Should _seedState be anything else (e.g. None) then the shuffling 
        of the local current time value is used as such an initial seed.

        """
        super().__init__( SplitMix32, _stateSize, _seedState )
            # this  call  creates  the  two  attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().


    #-------------------------------------------------------------------------
    @classmethod
    def _M0(cls, x: int = None, /) -> int:
        return 0
 
    #-------------------------------------------------------------------------
    @classmethod
    def _M1(cls, x: int, /) -> int:
        return x
 
    #-------------------------------------------------------------------------
    @classmethod
    def _M2_pos(cls, x: int, t: int, /) -> int:
        #assert 0 <= t < 32
        return x >> t

    #-------------------------------------------------------------------------
    @classmethod
    def _M2_neg(cls, x: int, t: int, /) -> int:
        #assert 0 <= t < 32
        return (x << t) & 0xffff_ffff
    
    #-------------------------------------------------------------------------
    @classmethod
    def _M3_pos(cls, x: int, t: int, /) -> int:
        #assert 0 <= t < 32
        return x ^ (x >> t)

    #-------------------------------------------------------------------------
    @classmethod
    def _M3_neg(cls, x: int, t: int, /) -> int:
        #assert 0 <= t < 32
        return x ^ ((x << t) & 0xffff_ffff)

    #-------------------------------------------------------------------------
    @classmethod
    def _M4(cls, x: int, a: int, /) -> int:
        #assert 0 <= a <= 0xffff_ffff
        return (x >> 1) ^ a if x & 0x8000_0000 else x >> 1

    #-------------------------------------------------------------------------
    @classmethod
    def _M5_pos(cls, x: int, t: int, a: int, /) -> int:
        #assert 0 <= t < 32
        #assert 0 <= b <= 0xffff_ffff
        return x ^ ((x >> t) & a)

    #-------------------------------------------------------------------------
    @classmethod
    def _M5_neg(cls, x: int, t: int, a: int, /) -> int:
        #assert 0 <= t < 32
        #assert 0 <= a <= 0xffff_ffff
        return x ^ (((x << t) & 0xffff_ffff) & a)

    #-------------------------------------------------------------------------
    @classmethod
    def _M6(cls, x: int, q: int, t: int, s: int, a: int, /) -> int:
        #assert 0 <= q < 32
        #assert 0 <= t < 32
        #assert 0 <= s < 32
        #assert 0 <= a <= 0xffff_ffff
        y = (((x << q) & 0xffff_ffff) ^ (x >> (32 - q))) & cls._d(s)
        return (y ^ a) if (x & (1<<t)) else y
    
    #-------------------------------------------------------------------------
    @classmethod
    def _d(cls, s: int, /) -> int:
        #assert 0 <= s < 32
        return 0xffff_ffff ^ (1 << s)

    #-------------------------------------------------------------------------
    @classmethod
    def _tempering(cls, x: int, b: int, c: int, /) -> int:
        #assert 0 <= b <= 0xffff_ffff
        #assert 0 <= c <= 0xffff_ffff
        # notice: the generic algorithm truncs x on w-bits. All of the implemented
        # ones in PyRandLib are set on 32-bits. So, no truncation takes place here 
        x = x ^ (((x << 7) & 0xffff_ffff) & b)
        return x ^ (((x << 15) & 0xffff_ffff) & c)

    #-------------------------------------------------------------------------
    # definition of algorithm constants
    _a1: Final[int] = 0xda44_2d24
    _a2: Final[int] = 0xd3e4_3ffd
    _a3: Final[int] = 0x8bdc_b91e
    _a4: Final[int] = 0x86a9_d87e
    _a5: Final[int] = 0xa8c2_96d1
    _a6: Final[int] = 0x5d6b_45cc
    _a7: Final[int] = 0xb729_fcec
    

#=====   end of module   basewell.py   =======================================
