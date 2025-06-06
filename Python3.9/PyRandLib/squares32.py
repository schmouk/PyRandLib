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
from .basesquares      import BaseSquares
from .annotation_types import SeedStateType, StatesList


#=============================================================================
class Squares32( BaseSquares ):
    """
    Pseudo-random numbers generator - Squares pseudo-random Generators 
    dedicated  to  64-bits calculations and 32-bits output values with 
    small period (min 2^64, i.e. 1.84e+19) but short computation time. 
    All  Squares  algorithms  offer multi streams features,  by simply 
    using different initial settings for control value 'key'.

    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    This Squares models is based on a  four  rounds  of  squaring  and 
    exchanging of upper and lower bits of the successive combinations.
    Output values are provided on 32-bits or on 64-bits  according  to 
    the model. See [9] in README.md.

    See Squares64 for a 2^64 (i.e. about 1.84e+19)  period  PRNG  with 
    low  computation  time,  medium period,  64-bits output values and 
    very good randomness characteristics.

    Furthermore this class is callable:
      rand = Squares32()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for the Squares 
    that have been implemented in PyRandLib,  as presented in paper [9]
    - see file README.md.

 | PyRandLib class | [9] generator name | Memory Usage  | Period   | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------ | ------------- | -------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Squares32       | squares32          |  4 x 4-bytes  |   2^64   |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Squares64       | squares64          |  4 x 4-bytes  |   2^64   |    n.a.     |     n.a.     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _seedState: SeedStateType = None, /) -> None:
        """Constructor. 
        
        Should _seedState be None then the local time is used as a seed  (with 
        its shuffled value).
        Notice: method setstate() is not implemented in base class BaseRandom.
        So,  it  must be implemented in classes inheriting BaseLCG and it must
        initialize attribute self._state.
        """
        super().__init__( _seedState )  # this internally calls 'setstate()'  which
                                        # MUST be implemented in inheriting classes


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.

        Return a 32-bits value.
        """
        self._counter = (self._counter + 1) & 0xffff_ffff_ffff_ffff
        
        y = x = (self._counter * self._key) & 0xffff_ffff_ffff_ffff
        z = (y + self._key) & 0xffff_ffff_ffff_ffff
        # round 1
        x = (x * x + y) & 0xffff_ffff_ffff_ffff
        x = (x >> 32) | ((x & 0xffff_ffff) << 32)
        # round 2
        x = (x * x + z) & 0xffff_ffff_ffff_ffff
        x = (x >> 32) | ((x & 0xffff_ffff) << 32)
        # round 3
        x = (x * x + y) & 0xffff_ffff_ffff_ffff
        x = (x >> 32) | ((x & 0xffff_ffff) << 32)
        # round 4
        return ((x * x + z) & 0xffff_ffff_ffff_ffff) >> 32


#=====   end of module   squares32.py   ======================================
