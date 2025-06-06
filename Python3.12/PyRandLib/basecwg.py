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
from typing import override

from .baserandom       import BaseRandom
from .annotation_types import SeedStateType, StatesListAndExt


#=============================================================================
class BaseCWG( BaseRandom ):
    """Definition of the base class for all Collatz-Weyl pseudo-random Generators.
    
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
    independent streams (this text is extracted from [8], see README.md).

    The internal implementation of the CWG algorithm varies according  to  its
    implemented  version.  See  implementation  classes  to  get  their formal 
    description.
    
    See Cwg64 for a minimum  2^70  (i.e. about 1.18e+21)  period  CW-Generator 
    with low computation time, medium period,  64- bits output values and very
    good randomness characteristics.
    See Cwg128_64 for a minimum 2^71 (i.e. about 2.36e+21) period CW-Generator 
    with very low computation time,  medium period,  64-bits output values and
    very good randomness characteristics.
    See Cwg128 for a minimum 2^135 (i.e. about 4.36e+40)  period  CW-generator
    with very low computation time, medium period,  64- bits output values and 
    very good randomness characteristics.

    Furthermore this class is callable:
      rand = BaseCWG()    # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for the CWGs that have 
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
    def getstate(self) -> StatesListAndExt:
        """Returns an object capturing the current internal state of the generator.
        
        This object can be passed to setstate() to restore the state.
        For  CWG,  this  state is defined by a list of control values 
        (a, weyl and s - or a list of 4 coeffs) and an internal state 
        value,  which  are used in methods 'next() and 'setstate() of 
        every inheriting class.

        All inheriting classes MUST IMPLEMENT this method.
        """
        return (self._a, self._weyl, self._s, self._state)
   

#=====   end of module   basecwg.py   ========================================
