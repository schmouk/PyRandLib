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
from .baserandom       import BaseRandom
from .annotation_types import Numerical


#=============================================================================
class BaseCWG( BaseRandom ):
    """Definition of the base class for all  Collatz-Weyl pseudo-random Generators.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    CWG models are chaotic generators that are combined with Weyl sequences to 
    eliminate  the risk of short cycles.  They have a large period,  a uniform 
    distribution,  and the ability to generate multiple independent streams by 
    changing  their  internal  parameters  (Weyl  increment).  CWGs  owe their 
    exceptional  quality  to  the  arithmetical  dynamics   of  noninvertible,
    generalized, Collatz mappings based on the wellknown Collatz conjecture. 
    There is no jump function, but each  odd  number  of  the  Weyl  increment 
    initiates  a  new  unique  period,  which  enables quick initialization of 
    independent streams. (extract from [8], see README.md)

    The internal implementation of the CWG algorithm varies according  to  its
    implemented  version.  See  implementation  classes  to  get  their formal 
    description.
    
    See Cwg64 for a minimum  2^70  (i.e. about 1.18e+21)  period  CW-Generator 
    with very low computation time, medium period,  64- bits output values and 
    very good randomness characteristics.
    See Cwg128_64 for a minimum 2^71 (i.e. about 2.36e+21) period CW-Generator 
    with very low computation time,  medium period,  64-bits output values and
    very good randomness characteristics.
    See Cwg128 for a minimum 2^135 (i.e. about 4.36e+40)  period  CW-generator
    with very low computation time, medium period,  64- bits output values and 
    very good randomness characteristics.

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
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _seedState: Numerical = None) -> None:
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
        For LCG,  the state is defined with  a  single  integer,  'self._value',
        which  has  to  be  used  in  methods 'random() and 'setstate() of every
        inheriting class.
        """
        return self._state
 
#=====   end of module   baselcg.py   ========================================
