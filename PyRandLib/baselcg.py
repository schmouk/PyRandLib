#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016-2022 Philippe Schmouker, schmouk (at) gmail.com

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
from .baserandom import BaseRandom


#=============================================================================
class BaseLCG( BaseRandom ):
    """Definition of the base class for all LCG pseudo-random generators.
    
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

    See FastRand32 for a 2^32 (i.e. 4.3e+9) period LC-Generator with very  low 
    computation  time  but shorter period and worse randomness characteristics
    than for FastRand63.
    See FastRand63 for a 2^63 (i.e. about 9.2e+18)  period  LC-Generator  with  
    low  computation  time  also,  longer  period  and quite better randomness 
    characteristics than for FastRand32.

    Furthermore this class is callable:
      rand = BaseLCG()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)

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
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    #------------------------------------------------------------------------=
    def __init__(self, _seedState: int = None) -> None:
        """Constructor. 
        
        Should inSeed be None or not an integer then the local 
        time is used (with its shuffled value) as a seed.
        """
        super().__init__( _seedState ) # this call creates attribute self._value and sets it
            
 
    #------------------------------------------------------------------------=
    def random(self) -> float:
        """This is the core of the pseudo-random generator.
        
        Returned values are within [0.0, 1.0).
        Inheriting classes HAVE TO IMPLEMENT this method  -  see FastRand32
        for an example. It should use and initialize attribute self._value.
        """
        raise NotImplementedError()
            
 
    #------------------------------------------------------------------------=
    def getstate(self) -> int:
        """Returns an object capturing the current internal state of the generator.
        
        This object can be passed to setstate() to restore the state.
        For LCG,  the state is defined with  a  single  integer,  'self._value',
        which  has  to  be  used  in  methods 'random() and 'setstate() of every
        inheriting class.
        """
        return self._value
            
 
    #------------------------------------------------------------------------=
    def setstate(self, _state: int) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call to getstate(),
        and  setstate() restores the internal state of the generator to what
        it was at the time setstate() was called.
        Inheriting classes HAVE TO IMPLEMENT this method  -  see  FastRand32
        for an example. It should initialize attribute self._value.
        """
        raise NotImplementedError()

 
#=====   end of module   baselcg.py   ========================================
