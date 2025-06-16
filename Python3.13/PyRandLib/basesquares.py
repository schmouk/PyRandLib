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
from typing import override

from .baserandom       import BaseRandom
from .annotation_types import SeedStateType, Numerical, StatesList
from .splitmix         import SplitMix32


#=============================================================================
class BaseSquares( BaseRandom ):
    """Definition of the base class for the Squares counter-based pseudo-random Generator.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    Squares models are based on an incremented counter and a key.  The 
    algorithm squares a combination of the counter and the key values, 
    and exchanges the upper and lower bits  of  the  combination,  the 
    whole  repeated  a number of times (4 to 5 rounds).  Output values 
    are provided on 32-bits or on 64-bits according to the model.  See 
    [9] in README.md.

    See Squares32 for a 2^64 (i.e. about 1.84e+19)  period  PRNG  with 
    low  computation  time,  medium period,  32-bits output values and 
    very good randomness characteristics.

    See Squares64 for a 2^64 (i.e. about 1.84e+19)  period  PRNG  with 
    low  computation  time,  medium period,  64-bits output values and 
    very good randomness characteristics. Caution: the 64-bits version
    should  not  pass the birthday test,  which is a randomness issue, 
    while this is not mentionned in the original  paper  (see  [9]  in
    file README.md).

    Furthermore this class is callable:
      rand = BaseSquares()# Caution: this is just used as illustrative. This base class cannot be instantiated
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
    @override
    def getstate(self) -> StatesList:
        """Returns an object capturing the current internal state of the generator.
        """
        return (self._counter, self._key)


    #-------------------------------------------------------------------------
    @override
    def seed(self, _seed: Numerical = None, /) -> None:
        """Initiates the internal state of this pseudo-random generator.
        """
        if _seed is None or isinstance(_seed, int | float):
            self._counter = 0
            if isinstance(_seed, float):
                if ( 0.0 <= _seed <= 1.0):
                    # transforms passed initial seed from float to integer
                    self._key = self._initKey( int(_seed * 0xffff_ffff_ffff_ffff) )
                else:
                    raise ValueError(f"can't set internal state with a float value outside range [0.0, 1.0] (actually is {_seed})")
            else:
                # _seed is None or an int
                self._key = self._initKey( _seed )
        else:
            raise TypeError( f"seed value must be None, an integer or a float (currently is of type {type(_seed)})" )


    #-------------------------------------------------------------------------
    @override
    def setstate(self, _state: StatesList = None, /) -> None:
        """Restores or sets the internal state of the generator.
        """
        if _state is None:
            self._counter = 0
            self._key = self._initKey()

        elif not isinstance( _state, list | tuple ):
            raise TypeError(f"initialization state must be a tuple or a list (actually is {type(_state)})")

        else:
            if len(_state) == 2:
                # each entry in _seedState MUST be a positive or null integer
                if not all(isinstance(s, int) and s >= 0 for s in _state):
                    raise ValueError(f"all values of internal state must be single non negative integers: {_state}")
                else:
                    self._counter = _state[0] & 0xffff_ffff_ffff_ffff
                    self._key     = (_state[1] & 0xffff_ffff_ffff_ffff) | 1  # Notice: key must be odd
                
            else:
                raise ValueError(f"Incorrect size for initializing state (should be 2 integers, currently is {len(_state)})")


    #-------------------------------------------------------------------------
    def _initKey(self, _seed: int = None, /) -> int:
        """Initalizes the attribute _key according to the original recommendations - see [9].
        """
    
        hexDigits = [ i for i in range(1, 16) ]
        key = 0

        initRand = SplitMix32( _seed )
        _NORMALIZE = 2.328_306_436_538_696_289_062_5e-10  # i.e. 1.0 / (1 << 32)

        # 8 high hexa digits - all different
        n = 15
        while n >= 8:
            h = hexDigits[ (k := int(n * (initRand() * _NORMALIZE))) ]
            key <<= 4
            key += h
            if k < (n := n-1):
                hexDigits[ k ] = hexDigits[ n ]
                hexDigits[ n ] = h

        # 9th hexa digit - different from the 8th one
        hexDigits[7], hexDigits[14] = hexDigits[14], hexDigits[7]
        h = hexDigits[ (k := int(14 * (initRand() * _NORMALIZE))) ]
        key <<= 4
        key += h
        hexDigits[ k ] = hexDigits[ 14 ]
        hexDigits[ 14 ] = h

        # 7 low hexa digits - all different
        n = 14
        while n >= 8:
            h = hexDigits[ (k := int(n * (initRand() * _NORMALIZE))) ]
            key <<= 4
            key += h
            if k < (n := n-1):
                hexDigits[ k ] = hexDigits[ n ]
                hexDigits[ n ] = h

        return key | 1  # Notice: key must be odd


#=====   end of module   basesquares.py   ====================================
