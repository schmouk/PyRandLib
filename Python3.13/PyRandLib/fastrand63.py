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
from typing import Final, override

from .baselcg          import BaseLCG
from .annotation_types import Numerical
from .splitmix         import SplitMix63


#=============================================================================
class FastRand63( BaseLCG ):
    """
    Pseudo-random numbers generator - Linear Congruential Generator dedicated  
    to  63-bits calculations with very short period (about 9.2e+18) and short
    time computation.

    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

    LCG models evaluate pseudo-random numbers suites x(i) as a simple mathem-
    atical function of 
    
        x(i-1): x(i) = (a*x(i-1) + c) mod m 
     
    Results  are  nevertheless  considered  to  be  poor  as  stated  in  the 
    evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de 
    Montreal) in 'TestU01: A C Library for Empirical Testing of Random Number 
    Generators  -  ACM  Transactions  on  Mathematical Software,  vol.33  n.4,  
    pp.22-40,  August  2007'.  It is not recommended to use such pseudo-random 
    numbers generators for serious simulation applications.
   
    The implementation of this LCG 63-bits model is based on (a=9219741426499971445, c=1)
    since  these  two  values  have  evaluated  to be the 'best' ones for LCGs 
    within TestU01 while m = 2^63.

    See FastRand32 for a 2^32 (i.e. 4.3e+9) period LC-Generator with very  low 
    computation  time  but shorter period and worse randomness characteristics
    than for FastRand63.
      
    Furthermore this class is callable:
      rand = FastRand63()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = FastRand63()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRandLib class | TU01 generator name                | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ---------------------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | FastRand32      | LCG(2^32, 69069, 1)                |     1 x 4-bytes | 2^32    |    3.20     |     0.67     |         11       |     106     |   *too many*   |
 | FastRand63      | LCG(2^63, 9219741426499971445, 1)  |     2 x 4-bytes | 2^63    |    4.20     |     0.75     |          0       |       5     |       7        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """


    #-------------------------------------------------------------------------
    _NORMALIZE: Final[float] = 1.084_202_172_485_504_434_007_453e-19  # i.e. 1.0 / (1 << 63)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: Final[int] = 63
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    #-------------------------------------------------------------------------
    @override
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        self._state = (0x7ff3_19fa_a77b_e975 * self._state + 1) & 0x7fff_ffff_ffff_ffff
        return self._state


    #-------------------------------------------------------------------------
    @override
    def seed(self, _seed: Numerical = None, /) -> None:
        """Initiates the internal state of this pseudo-random generator.
        """
        if _seed is None or isinstance(_seed, int | float):
            if isinstance(_seed, float) and not (0.0 <= _seed <= 1.0):
                raise ValueError(f"Float seeds must be in range [0.0, 1.0] (currently is {_seed})")
            else:
                self._state = SplitMix32( _seed )()
        else:
            raise TypeError(f"Seeding value must be None, an int or a float (currently is {type(_seed)})")


    #-------------------------------------------------------------------------
    @override
    def setstate(self, _state: Numerical, /) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called.
        """
        if isinstance(_state, int):
            self._state = SplitMix63( _state )()
        else:
            raise TypeError(f"initialization state must be an integer (actually is {type(_state)})")


#=====   end of module   fastrand63.py   =====================================
