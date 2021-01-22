#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016-2021 Philippe Schmouker, schmouk (at) typee.ovh

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
import time

from .baselcg import BaseLCG
from .types   import Numeric


#=============================================================================
class FastRand63( BaseLCG ):
    """
    Pseudo-random numbers generator - Linear Congruential Generator dedicated  
    to  63-bits calculations with very short period (about 9.2e+18) and short
    time computation.
    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2021 Philippe Schmouker

    LCG models evaluate pseudo-random numbers suites x(i) as a simple mathem-
    atical function of 
    
        x(i-1): x(i) = (a*x(i-1) + c) mod m 
     
    Results  are  nevertheless  considered  to  be  poor  as  stated  in  the 
    evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de 
    Montreal) in 'TestU01: A C Library for Empirical Testing of Random Number 
    Generators  -  ACM  Transactions  on  Mathematical Software,  vol.33  n.4,  
    pp.22-40,  August  2007'.  It is not recommended to use such pseudo-random 
    numbers generators for serious simulation applications.
   
    The implementation of this LCG 63-bits model is based on (a=9219741426499971445, c=1)
    since  these  two  values  have  evaluated  to be the 'best' ones for LCGs 
    within TestU01 while m = 2^63.

    See FastRand32 for a 2^32 (i.e. 4.3e+9) period LC-Generator with very  low 
    computation  time  but shorter period and worse randomness characteristics
    than for FastRand63.
      
    Furthermore this class is callable:
      rand = FastRand63()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = FastRand63()
      print( int(diceRoll(1, 7)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRabndLib class | TU01 generator name                | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ---------------------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | FastRand32       | LCG(2^32, 69069, 1)                |     1 x 4-bytes | 2^32    |    3.20     |     0.67     |         11       |     106     |   *too many*   |
 | FastRand63       | LCG(2^63, 9219741426499971445, 1)  |     2 x 4-bytes | 2^63    |    4.20     |     0.75     |          0       |       5     |       7        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
 
    #------------------------------------------------------------------------=
    def random(self) -> float:
        """This is the core of the pseudo-random generator.
        
        Returned values are within [0.0, 1.0).
        """
        self._value = (9219741426499971445 * self._value + 1) & 0x7fffffffffffffff
        return self._value / 9223372036854775808.0
            
 
    #------------------------------------------------------------------------=
    def setstate(self, _state: Numeric) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call 
        to  getstate(),  and setstate() restores the internal 
        state of the generator to what it  was  at  the  time 
        setstate() was called.
        """
        if isinstance( _state, int ):
            self._value = _state & 0x7fffffffffffffff
            
        elif isinstance( _state, float ):
            # transforms passed initial seed from float to integer
            if _state < 0.0 :
                _state = -_state
            
            if _state >= 1.0:
                self._value = int(_state+0.5) & 0x7fffffffffffffff
            else:
                self._value = int(_state*0x8000000000000000) & 0x7fffffffffffffff
        
        else:
            t = int(time.time() * 1000.0)
            self._value = t & 0xffffffff
            self._value += (t & 0xff000000) <<  8
            self._value += (t & 0x00ff0000) << 24
            self._value += (t & 0x0000ff00) << 40
            self._value += (t & 0x000000fe) << 63

#=====   end of module   fastrand63.py   =====================================
