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

from .basecwg          import BaseCWG
from .annotation_types import SeedStateType
from .splitmix         import SplitMix64


#=============================================================================
class Cwg128( BaseCWG ):
    """
    Pseudo-random numbers generator  -  Collatz-Weyl pseudo-random  Generators
    dedicated  to  128-bits calculations and 128-bits output values with large
    period (min 2^135, i.e. 4.36e+40) but  short  computation  time.  All  CWG 
    algorithms offer multi streams features, by simply using different initial 
    settings for control value 's' - see below.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    This CWG model evaluates pseudo-random numbers suites  x(i)  as  a  simple
    mathematical function of 
    
        x(i+1) = (x(i) >> 1) * ((a += x(i)) | 1) ^ (weyl += s) 

    and returns as the output value the xored shifted: a >> 96 ^ x(i+1)

    where a, weyl and s are the control values and x the internal state of the
    PRNG.  's' must be initally odd.  'a', 'weyl' and initial state 'x' may be 
    initialized each with any 64-bits value.

    Notice: in the original paper,  four control value c[0] to c[3] are  used. 
    It appears that these value are used just are 's' for c[0],  'x' for c[1],
    'a' for c[2] and 'weyl' for c[3] in the other versions of the algorithm.
    
    See Cwg64 for a minimum  2^70  (i.e. about 1.18e+21)  period  CW-Generator 
    with very low computation time, medium period,  64- bits output values and 
    very good randomness characteristics.
    See Cwg128_64 for a minimum 2^71 (i.e. about 2.36e+21) period CW-Generator 
    with very low computation time,  medium period,  64-bits output values and
    very good randomness characteristics.

    Furthermore this class is callable:
      rand = Cwg128()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for  the  CWGs  that  have 
    been implemented in PyRandLib, as presented in paper [8] - see file README.md.

 | PyRandLib class | [8] generator name | Memory Usage  | Period   | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------ | ------------- | -------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Cwg64           | CWG64              |   8 x 4-bytes | >= 2^70  |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Cwg128_64       | CWG128_64          |  10 x 4-bytes | >= 2^71  |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Cwg128          | CWG128             |  16 x 4-bytes | >= 2^135 |    n.a.     |     n.a.     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    

    #-------------------------------------------------------------------------
    _NORMALIZE: Final[float] = 2.938_735_877_055_718_769_921_8e-39  # i.e. 1.0 / (1 << 128)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: Final[int] = 128
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    _MODULO: Final[int] = (1 << 128) - 1  # notice: optimization on modulo computations


    #-------------------------------------------------------------------------
    def __init__(self, _seedState: SeedStateType = None, /) -> None:
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
        self._a = (self._a + self._state) & self._MODULO
        self._weyl = (self._weyl + self._s) & self._MODULO
        self._state = (((self._state >> 1) * (self._a | 1)) ^ self._weyl) & self._MODULO
        # returns the xored-shifted output value
        return self._state ^ (self._a >> 96)


    #-------------------------------------------------------------------------
    def setstate(self, _state: SeedStateType = None, /) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called. If None, the local system time
        is used instead.
        """
        if _state is None or isinstance(_state, int) or isinstance(_state, float):
            initRand = SplitMix64( _state )
            self._a = self._weyl = 0
            self._s = (initRand() << 64) | initRand() | 1   # Notice: s must be odd
            self._state = (initRand() << 64) | initRand()   # Notice: in the original paper, this seems to be erroneously initialized on sole 64 lowest bits
                            
        else:
            try:
                self._a     =  _state[0] & self._MODULO
                self._weyl  =  _state[1] & self._MODULO
                self._s     = (_state[2] & self._MODULO) | 1  # Notice: s must be odd
                self._state =  _state[3] & self._MODULO

            except:
                # uses local time as initial seed
                self.setstate()


#=====   end of module   cwg128.py   =========================================
