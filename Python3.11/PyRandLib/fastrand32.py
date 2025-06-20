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
from .baselcg          import BaseLCG
from .annotation_types import Numerical
from .splitmix         import SplitMix32


#=============================================================================
class FastRand32( BaseLCG ):
    """
    Pseudo-random numbers generator - Linear Congruential Generator dedicated  
    to  32-bits  calculations with very short period (about 4.3e+09) but very 
    short time computation.

    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

    LCG models evaluate pseudo-random numbers suites x(i) as a simple mathem-
    atical function of 
    
        x(i) = (a * x(i-1) + c) mod m 
     
    Results  are  nevertheless  considered  to  be  poor  as  stated  in  the 
    evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de 
    Montreal) in 'TestU01: A C Library for Empirical Testing of Random Number 
    Generators  -  ACM  Transactions  on Mathematical Software,  vol.33  n.4,  
    pp.22-40,  August 2007'.  It is not recommended to use such pseudo-random 
    numbers generators for serious simulation applications.
   
    The implementation of this LCG 32-bits model is based  on  (a=69069, c=1) 
    since  these  two  values  have  evaluated to be the 'best' ones for LCGs 
    within TestU01 while m = 2^32.

    See FastRand63 for a 2^63 (i.e. about 9.2e+18) period  LC-Generator  with  
    low  computation  time  also,  longer  period and quite better randomness 
    characteristics than for FastRand32.
      
    Furthermore this class is callable:
      rand = FastRand32()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = FastRand32()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

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
    def __init__(self, _seed: Numerical = None, /) -> None:  # type: ignore
        """Constructor.
        
        Should _seed be None or not a numerical then the local 
        time is used (with its shuffled value) as a seed.
        """
        super().__init__( _seed ) # this call creates attribute self._state and sets it


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        self._state = (0x1_0dcd * self._state + 1) & 0xffff_ffff
        return self._state


    #-------------------------------------------------------------------------
    def seed(self, _seed: Numerical = None, /) -> None:  # type: ignore
        """Initiates the internal state of this pseudo-random generator.
        """
        if _seed is None or isinstance(_seed, (int, float)):
            if isinstance(_seed, float) and not (0.0 <= _seed <= 1.0):
                raise ValueError(f"Float seeds must be in range [0.0, 1.0] (currently is {_seed})")
            else:
                self._state = SplitMix32( _seed )()
        else:
            raise TypeError(f"Seeding value must be None, an int or a float (currently is {type(_seed)})")


    #-------------------------------------------------------------------------
    def setstate(self, _state: Numerical = None, /) -> None:  # type: ignore
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called. If None, the local system time
        is used instead.
        """
        if _state is None:
            self.seed()
        elif isinstance(_state, int):
            self._state = SplitMix32( _state )()
        else:
            raise TypeError(f"initialization state must be None or an integer (actually is {type(_state)})")


#=====   end of module   fastrand32.py   =====================================
