#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2016-2019 Philippe Schmouker, schmouk (at) typee.ovh

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
class MRGRand49507( BaseMRG ):
    """
    Pseudo-random numbers generator  - Definition of a fast 31-bits Multiple Recursive 
    Generator with a very long period (1.17e+14_903).
    This module is part of library PyRandLib.

    Multiple Recursive Generators (MRGs) uses  recurrence  to  evaluate  pseudo-random
    numbers suites. Recurrence is of the form:
    
       x(i) = A * SUM[ x(i-k) ]  mod M
       
    for 2 to more k different values.

    MRGs offer very large periods with the best known results  in  the  evaluation  of 
    their  randomness,  as  stated  in  the  evaluation  done  by  Pierre L'Ecuyer and 
    Richard Simard (Universite de  Montreal) in "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.

    The implementation of this MRG 31-bits model is based on the 'DX-1597-2-7' MRG. It
    uses the recurrence
    
        x(i) = (-2^25-2^7) * (x(i-7) + x(i-1597)) mod (2^31-1)
        
    and offers a  period  of  about  2^49_507  -  i.e. nearly 1.2e+14_903  -  with low 
    computation time.

    See MRGRand287 for a short period  MR-Generator (2^287,  i.e. 2.49e+86)  with  low
    computation time but 256 integers memory consumption.
    See MRGRand1457 for a  longer  period  MR-Generator  (2^1457,  i.e. 4.0e+438)  and 
    longer  computation  time  (2^31-1  modulus  calculations)  but  less memory space 
    consumption (47 integers).
    
    Class random.Random is sub-subclassed here to use a different basic  generator  of  
    our own devising: in that case, overriden methods are:
      random(), seed(), getstate(), and setstate().
      
    Furthermore this class is callable:
      rand = MRGRand49507()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = MRGRand49507()
      print( int(diceRoll(1, 7)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRabndLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | MRGRand287       | Marsa-LFIB4         |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | MRGRand1457      | DX-47-3             |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | MRGRand49507     | DX-1597-2-7         | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """    
    
    #=========================================================================
    # 'protected' constant
    _LIST_SIZE = 1597       # this 'DX-1597-2-7' MRG is based on a suite containing 1597 integers
    _MODULO    = 2147483647 # i.e. 0x7fffffff, or (1<<31)-1, the modulo for DX-1597-2-7 MRG
            
 
    #=========================================================================
    def random(self) -> float:
        """
        This is the core of the pseudo-random generator.
        Returned values are within [0.0, 1.0).
        """
        # evaluates indexes in suite for the i-7, i-1597 -th values
        k7 = self._index-7
        if k7 < 0:
            k7 += MRGRand49507._LIST_SIZE
        
        # then evaluates current value
        myValue = (-67108992 * (self._list[k7] + self._list[self._index])) % 2147483647
        self._list[self._index] = myValue
        
        # next index
        self._index = (self._index+1) % MRGRand49507._LIST_SIZE
        
        # then returns float value within [0.0, 1.0)
        return  myValue / 2147483647.0
 
#=====   end of module   mrgrand49507.py   ===================================
