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
from .baserandom       import BaseRandom
from .annotation_types import Numerical, SeedStateType


#=============================================================================
class BasePCG( BaseRandom ):
    """Definition of the base class for all Permuted Congruential Generator pseudo-random generators.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    As LCGs do, PCG models evaluate pseudo-random numbers  suites  x(i)  as  a 
    simple mathematical function of x(i-1):
 
       x(i) = (a * x(i-1) + c) mod m

    PCGs associate to this recurrence a permutation of a subpart o f the  bits 
    of  the internal state of the PRNG.  The output of PCGs is this permutated
    subpart of its internal state,  leading to a very large enhancement of the
    randomness of these algorithms compared with the LCGs one.
 
    These PRNGs have been tested with TestU01 and have shown to pass all tests
    (Pierre  L'Ecuyer and Richard Simard (Universite de Montreal) in 'TestU01: 
    A C Library for Empirical  Testing  of  Random  Number  Generators  -  ACM 
    Transactions on Mathematical Software, vol.33 n.4, pp.22-40, August 2007')

    PCGs are very fast generators, with low memory usage except for a very few 
    of them and medium to very large periods.  They offer jump ahead and multi
    streams features for most of them. They are difficult to very difficult to
    invert and to predict.

    See Pcg64_32 for a 2^64 (i.e. 1.84e+19) period PC-Generator with very  low 
    computation  time  and  medium period, with 2 32-bits word integers memory 
    consumption. Output values are returned on 32 bits.

    See Pcg128_64 for a 2^128 (i.e. about 3.40e+38) period  PC-Generator  with  
    low  computation  time also and a longer period than for Pcg64_32,  with 4 
    32-bits word integers memory consumption.  Output values are  returned  on 
    64 bits.
   
    See Pcg1024_32 for a 2^32,830 (i.e. about 6.53e+9882) period  PC-Generator
    with low computation time also and a very large period,  but 1,026 32-bits
    word integers memory consumption. Output values are returned on 32 bits.

    Furthermore this class is callable:
      rand = BasePCG()    # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for the PCGs that have 
    been  implemented  in  PyRandLib,  as provided by the author of PCGs - see
    reference [7] in file README.md.

 | PyRandLib class | initial PCG algo name       | Memory Usage   | Period   | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | --------------------------- | -------------- | -------- | ------------ | ---------------- | ----------- | -------------- |
 | Pcg64_32        | PCG XSH RS 64/32 (LCG)      |    2 x 4-bytes | 2^64     |     0.79     |          0       |       0     |       0        |
 | Pcg128_64       | PCG XSL RR 128/64 (LCG)     |    4 x 4-bytes | 2^128    |     1.70     |          0       |       0     |       0        |
 | Pcg1024_32      | PCG XSH RS 64/32 (EXT 1024) | 1026 x 4-bytes | 2^32,830 |     0.78     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _seedState: Numerical = None, /) -> None:  # type: ignore
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
    def getstate(self) -> SeedStateType:  # type: ignore
        """Returns an object capturing the current internal state of the generator.
        
        This object can be passed to setstate() to restore the state.
        For LCG,  the state is defined with  a  single  integer,  'self._value',
        which  has  to  be  used  in  methods 'random() and 'setstate() of every
        inheriting class.
        """
        return self._state  # notice: attribute _state MUST be initialized in inheriting classes  # type: ignore


#=====   end of module   basepcg.py   ========================================
