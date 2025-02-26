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
from .basewell import BaseWELL

#=============================================================================
class Well512a( BaseWELL ):
    """
    Pseudo-random numbers generator - Definition of a fast  32-bits  Well-Equilibrated 
    Long-period Linear generator with a large period (2^512, i.e. 1.34e+154).

    This module is part of library PyRandLib.
        
    Copyright (c) 2025 Philippe Schmouker

    Well-Equilibrated Long-period Linear Generators (WELL) use linear recurrence based 
    on  primitive  characteristic  polynomials associated with left- and right- shifts 
    and xor operations to fastly evaluate pseudo-random numbers suites.
    
    WELLs offer large to very large periods with best known results in the  evaluation 
    of their randomness,  as stated in the evaluation  done  by  Pierre  L'Ecuyer  and 
    Richard Simard (Universite de Montreal) in  "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.
    Furthermore, WELLs have proven their great ability  to  very  fastly  escape  from 
    zeroland.

    Notice: the algorithm in its Well512a version has been  coded  here  as  a  direct 
    implementation  of  its  descriptions in the initial paper:  "Improved Long-Period
    Generators Based on Linear Recurrences Modulo 2",  François  PANNETON  and  Pierre 
    L'ECUYER (Université de Montréal) and Makoto MATSUMOTO (Hiroshima University),  in
    ACM Transactions on Mathematical Software, Vol. 32, No. 1, March 2006, Pages 1-16.
    (see https://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf).
    As such,  only minimalist optimization has been coded,  with the aim at easing the 
    verification of its proper implementation.
       
    See Well512a for a large period WELL-Generator (2^512,  i.e. 1.34e+154)  with  low
    computation time and 16 integers memory consumption.
    See Well1024a for a longer period WELL-Generator  (2^1024,  i.e. 2.68e+308),  same 
    computation time and 32 integers memory consumption.
    See Well199937b for a far longer period  (2^19937,  i.e. 4.32e+6001) with  similar 
    computation time but use of more memory space (624 integers).
    See Well44497c for a very large period (2^44497,  i.e. 1.51e+13466)  with  similar 
    computation time but use of even more memory space (1,391 integers).
    
    Furthermore, this class is callable:
      rand = Well512a()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = Well512a()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}


    Such a programming is an accelerated while still robust emulation of the inherited 
    methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the WELL  algorithms  that 
    have  been implemented in PyRandLib,  as provided in paper "TestU01, ..." and when 
    available.

 | PyRandLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Well512a        | not available       |    16 x 4-bytes | 2^512   |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |
 | Well1024a       | WELL1024a           |    32 x 4-bytes | 2^1024  |    4.0      |     1.1      |          0       |       4     |       4        |
 | Well19937c (1)  | WELL19937a          |   624 x 4-bytes | 2^19937 |    4.3      |     1.3      |          0       |       2     |       2        |
 | Well44497b      | not available       | 1,391 x 4-bytes | 2^44497 |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |

    (1)The Well19937c generator provided with library PyRandLib implements the
    Well19937a  algorithm  augmented  with  an associated tempering algorithm.
    This should very slightly slow down its CPU  performance  while  enhancing 
    its pseudo-randomness quality, as measured by TestU01.

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    # 'protected' constant
    _STATE_SIZE = 16  # this Well512a PRNG internal state is based on a suite containing 16 integers (32-bits wide each)


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        i = self._index
        i_1 = (i - 1) & 0xf

        z0 = self._state[i_1]
            # notice:  all blocks of bits in the internal state are 32 bits wide, which leads to a great 
            # simplification for the implementation of the generic WELL algorithm when evaluating z0.
        z1 = self._M3_neg(self._state[i], 16) ^ self._M3_neg(self._state[(i + 13) & 0x0f], 15)
        z2 = self._M3_pos(self._state[(i + 9) & 0x0f], 11)
            # notice: the last term of the above equation in the WELL generic algorithm is, for its Well512a
            # version, the zero matrix _M0 which we suppress here for calculations optimization purpose
        z3 = z1 ^ z2

        self._state[i] = z3
        self._state[i_1] = self._M3_neg(z0, 2) ^ self._M3_neg(z1, 18) ^ self._M2_neg(z2, 28) ^ self._M5_neg(z3, 5, self._a1)

        self._index = i_1
        return z3

#=====   end of module   well512a.py   =======================================
