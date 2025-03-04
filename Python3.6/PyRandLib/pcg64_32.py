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
from .basepcg          import BasePCG
from .annotation_types import Numerical
from .splitmix         import SplitMix64


#=============================================================================
class Pcg64_32( BasePCG ):
    """
    Pseudo-random  numbers  generator  -  Permutated  Congruential  Generator 
    dedicated  to  64-bits calculations and 32-bits output with medium period 
    (about 1.84e+19) but very  short  time  computation.  The  PCG  algorithm 
    offers jump ahead and multi streams features.

    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    PCG models evaluate pseudo-random numbers suites x(i) as a simple mathem-
    atical function of 
    
        x(i) = (a * x(i-1) + c) mod m 

    as are LCGs, but associated with a permutation of a subpart of the bits of 
    the  internal  state  of  the PRNG.  The output of PCGs is this permutated 
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

    The Pcg64_32 class implements the "PCG XSH RS 64/32 (LCG)" version of  the
    PCG  algorithm,  as  specified  in  the related paper (see [7] in document 
    README.md), so with a = 6364136223846793005, c = 1442695040888963407,  the
    modulo m = 2^64 and the additional permutation  output  function  directly
    implemented in method 'next()'.

    See Pcg128_64 for a 2^128 (i.e. about 3.40e+38) period  PC-Generator  with  
    low  computation  time also and a longer period than for Pcg64_32,  with 4 
    32-bits word integers memory consumption.  Output values are  returned  on 
    64 bits.

    See Pcg1024_32 for a 2^32,830 (i.e. about 6.53e+9882) period  PC-Generator
    with low computation time also and a very large period,  but 1,026 32-bits
    word integers memory consumption. Output values are returned on 32 bits.
      
    Furthermore this class is callable:
      rand = Pcg64_32()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = Pcg64_32()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Reminder:
    We give you here below a copy of the table of tests for the PCGs that have 
    been  implemented  in  PyRandLib,  as provided by the author of PCGs - see
    reference [7] in file README.md.

 | PyRandLib class | initial PCG algo name       | Memory Usage    | Period   | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | --------------------------- | --------------- | -------- | ------------ | ---------------- | ----------- | -------------- |
 | Pcg64_32        | PCG XSH RS 64/32 (LCG)      |     2 x 4-bytes | 2^64     |     0.79     |          0       |       0     |       0        |
 | Pcg128_64       | PCG XSL RR 128/64 (LCG)     |     4 x 4-bytes | 2^128    |     1.70     |          0       |       0     |       0        |
 | Pcg1024_32      | PCG XSH RS 64/32 (EXT 1024) | 1,026 x 4-bytes | 2^32,830 |     0.78     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    def __init__(self, _seed: Numerical = None) -> None:
        """Constructor.
        
        Should _seed be None or not a numerical then the local 
        time is used (with its shuffled value) as a seed.
        """
        super().__init__( _seed ) # this call creates attribute self._state and sets it


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # evaluates next internal state
        current_state = self._state
        self._state = (0x5851_F42D_4C95_7F2D * current_state + 0x1405_7B7E_F767_814F) & 0xffff_ffff_ffff_ffff
        # the permutated output is then computed
        random_shift = (current_state >> 61) & 0x07  # random shift is set with the 3 upper bits of internal state
        current_state ^= current_state >> 22         # fixed shift XOR is then evaluated
        return (current_state >> (22 + random_shift)) & 0xffff_ffff


    #-------------------------------------------------------------------------
    def setstate(self, _state: Numerical) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called.
        """
        if isinstance( _state, int ):
            # passed initial seed is an integer, just uses it
            self._state = _state & 0xffff_ffff_ffff_ffff
            
        elif isinstance( _state, float ):
            # transforms passed initial seed from float to integer
            if _state < 0.0 :
                _state = -_state
            if _state >= 1.0:
                self._state = int( _state + 0.5 ) & 0xffff_ffff_ffff_ffff
            else:
                self._state = int( _state * 0x1_0000_0000_0000_0000) & 0xffff_ffff_ffff_ffff
                
        else:
            # uses local time as initial seed
            initRand = SplitMix64()
            self._state = initRand()


#=====   end of module   pcg64_32.py   =======================================
