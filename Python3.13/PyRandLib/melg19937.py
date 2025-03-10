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
from typing import Final, override

from .basemelg import BaseMELG


#=============================================================================
class Melg19937( BaseMELG ):
    """Pseudo-random numbers generator. Definition of a 64-bits Maximally Equidistrib-
    uted Long-period Linear generator with a large period (2^19,937, i.e. 4.32e+6001).
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    Maximally  Equidistributed  Long-period  Linear  Generators  (MELG)   use   linear 
    recurrence  based  on  state  transitions  with double feedbacks and linear output 
    transformations with several memory references. See reference [11] in README.md.
    
    MELGs offer large to very large periods with best known results in the  evaluation 
    of their randomness.  They ensure a maximally equidistributed generation of pseudo 
    random numbers.  They pass all TestU01 tests and newer ones but are the slowest to
    compute ones in the base of PRNGs that have been implemented in PyRandLib.

    Notice: the implementation of this version of the MELG algorithm in  PyRandLib  is 
    not as optimized as it is in C code provided by MELG authors. It is rather derived
    from the formal description and related tables provided in paper  referenced  [11]
    in  file  README.md,  to be able to easier validate the Python code here.

    Notice also:  in the original paper [11],  in the description of  Algorithm 1,  an 
    error  (typo)  appears at the initialization of 'x'.  An bit-xor operation appears 
    in the text while it should be a bit-or operation as explaind in  plain  text.  We
    correct in in the code here.
       
    See Melg607 for a large period MELG-Generator (2^607, i.e. 5.31e+182)  with medium
    computation  time  and  the  equivalent  of  21  32-bits  integers  memory  little 
    consumption.
    See Melg44497 for a very large period (2^44,497, i.e. 15.1e+13,466)  with  similar 
    computation  time  but  use of even more memory space (equivalent of 1,393 32-bits
    integers). This is the longest period version proposed in paper [11].
    
    Furthermore, this class is callable:
      rand = Melg19937()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Notice that for simulating the roll of a dice you should program:
      diceRoll = Melg19937()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of the inherited 
    methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the  MELG  algorithms  that 
    have  been  implemented in PyRandLib, as provided in paper [11] and when available.

 | PyRandLib class | [11] generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Melg607         | melg607-64          |    21 x 4-bytes | 2^607   |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |
 | Melg19937       | melg19937-64        |   625 x 4-bytes | 2^19937 |    n.a.     |     4.21     |          0       |       0     |       0        |
 | Melg44497       | melg44497-64        | 1,393 x 4-bytes | 2^44497 |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    # 'protected' constants
    _STATE_SIZE: Final[int] = 312
    _A_COND = (0, 0x5c32_e06d_f730_fc42)  # this tuple will avoid an 'if' in method 'next()'


    #-------------------------------------------------------------------------
    @override
    def next(self) -> int:
        """This is the core of the pseudo-random generator.

        Notice: the output value is coded on 64-bits.
        """
        i = self._index
        self._index = (i_1 := (i+1) % 311)

        s311 = self._state[311]
        x = (self._state[i] & 0xffff_fffe_0000_0000) | (self._state[i_1] & 0x0000_0001_ffff_ffff)  # notice: | instead of ^ as erroneously printed in [11]
        self._state[311] = (s311 := ((x >> 1) ^ Melg19937._A_COND[x & 0x01]) ^ self._state[(i+81) % 311] ^ (s311 ^ ((s311 << 23) & 0xffff_ffff_ffff_ffff)))

        si = self._state[i] = x ^ (s311 ^ (s311 >> 33))
        return (si ^ ((si << 16) & 0xffff_ffff_ffff_ffff)) ^ ((self._state[(i + 19) % 311]) & 0x6aed_e6fd_97b3_38ec)
        

#=====   end of module   melg19937.py   ======================================
