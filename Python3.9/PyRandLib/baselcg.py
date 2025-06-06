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
from .baserandom       import BaseRandom
from .annotation_types import Numerical


#=============================================================================
class BaseLCG( BaseRandom ):
    """Definition of the base class for all LCG pseudo-random generators.
    
    This module is part of library PyRandLib.

    Copyright (c) 2016-2025 Philippe Schmouker

    LCG models evaluate pseudo-random numbers suites x(i) as a simple mathem-
    atical function of 
    
        x(i-1): x(i) = (a*x(i-1) + c) mod m 
     
    Results are nevertheless considered to be poor as stated in the evaluation
    done  by  Pierre  L'Ecuyer  and Richard Simard (Universite de Montreal) in
    'TestU01: A C Library for Empirical Testing of Random Number Generators  -
    ACM Transactions on Mathematical Software,  vol.33  n.4,  pp.22-40, August 
    2007'.  It is not recommended to use such pseudo-random numbers generators 
    for serious simulation applications.

    See FastRand32 for a 2^32 (i.e. 4.3e+9) period LC-Generator with very  low 
    computation  time  but shorter period and worse randomness characteristics
    than for FastRand63.
    See FastRand63 for a 2^63 (i.e. about 9.2e+18)  period  LC-Generator  with  
    low  computation  time  also,  longer  period  and quite better randomness 
    characteristics than for FastRand32.

    Furthermore this class is callable:
      rand = BaseLCG()    # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

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
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _seedState: Numerical = None, /) -> None:
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
    def getstate(self) -> int:
        """Returns an object capturing the current internal state of the generator.
        
        This object can be passed to setstate() to restore the state.
        For LCG,  the state is defined with a single  integer,  'self._state',
        which  has  to  be  used  in  methods 'next() and 'setstate() of every
        inheriting class.
        """
        return self._state
 

#=====   end of module   baselcg.py   ========================================
