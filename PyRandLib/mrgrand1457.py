"""
Copyright (c) 2016-2025 Philippe Schmouker, schmouk (at) gmail.com

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
from .basemrg import BaseMRG


#=============================================================================
class MRGRand1457( BaseMRG ):
    """
    Pseudo-random numbers generator  - Definition of a fast 31-bits Multiple Recursive
    Generator with long period (3.98e+438).
    This module is part of library PyRandLib.

    Multiple Recursive Generators (MRGs) uses  recurrence  to  evaluate  pseudo-random
    numbers suites. Recurrence is of the form:
    
       x(i) = A * SUM[ x(i-k) ]  mod M
       
    for 2 to more k different values.
    
    MRGs offer very large periods with the best known results  in  the  evaluation  of 
    their  randomness,  as  stated  in  the  evaluation  done  by  Pierre L'Ecuyer and 
    Richard Simard (Universite de Montreal)  in "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.
   
    The implementation of this MRG 31-bits model is  based  on  DX-47-3  pseudo-random
    generator  proposed  by  Deng  and  Lin.  The  DX-47-3 version uses the recurrence
    
        x(i) = (2^26+2^19) * (x(i-1) + x(i-24) + x(i-47)) mod (2^31-1)
        
    and offers a period of about 2^1457  - i.e. nearly 4.0e+438 - with low computation
    time.

    See MRGRand287 for a short period  MR-Generator (2^287,  i.e. 2.49e+86)  with  low
    computation time but 256 integers memory consumption.
    See MRGRand49507 for a far longer period  (2^49_507,  i.e. 1.2e+14_903)  with  low 
    computation  time  too  (31-bits  modulus)  but  use  of  more  memory space (1597 
    integers).
    
    Class random.Random is sub-subclassed here to use a different basic  generator  of  
    our own devising: in that case, overriden methods are:
      random(), seed(), getstate(), and setstate().
      
    Furthermore this class is callable:
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = MRGRand1457()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}


    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the MRGs  that  have  been
    implemented in PyRandLib, as provided in paper "TestU01, ..." - see file README.md.

 | PyRandLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | MRGRand287      | Marsa-LFIB4         |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | MRGRand1457     | DX-47-3             |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | MRGRand49507    | DX-1597-2-7         | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    
    #-------------------------------------------------------------------------
    # 'protected' constant
    _STATE_SIZE = 47            # this 'DX-47-3' MRG is based on a suite containing 47 integers
    _MODULO     = 2_147_483_647 # i.e. 0x7fff_ffff, or (1<<31)-1, the modulo for DX-47-3 MRG


    #-------------------------------------------------------------------------
    _NORMALIZE: float = 4.656_612_873_077_039_257_8e-10  # i.e. 1.0 / (1 << 31)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: int = 31
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # The DX-47-3 version uses the recurrence
        #   x(i) = (2^26+2^19) * (x(i-1) + x(i-24) + x(i-47)) mod (2^31-1)

        # evaluates indexes in suite for the i-1, i-24 (and i-47) -th values
        k1  = self._index-1
        if k1 < 0:
            k1 = MRGRand1457._STATE_SIZE - 1
        
        k24 = self._index-24
        if k24 < 0:
            k24 += MRGRand1457._STATE_SIZE
        
        # then evaluates current value
        myValue = (0x0408_0000 * (self._state[k1] + self._state[k24] + self._state[self._index]) ) % 2_147_483_647
        self._state[self._index] = myValue
        
        # next index
        self._index = (self._index + 1) % MRGRand1457._STATE_SIZE

        # then returns the integer generated value
        return  myValue

#=====   end of module   mrgrand1457.py   ====================================
