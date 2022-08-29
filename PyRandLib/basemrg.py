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
from .fastrand32 import FastRand32
from .types      import SeedStateType, StateType


#=============================================================================
class BaseMRG( BaseRandom ):
    """Definition of the base class for all MRG pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2021 Philippe Schmouker

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
       
    See MRGRand287 for a short period  MR-Generator (2^287,  i.e. 2.49e+86)  with  low
    computation time but 256 integers memory consumption.
    See MRGRand1457 for a  longer  period  MR-Generator  (2^1457,  i.e. 4.0e+438)  and 
    longer  computation  time  (2^31-1  modulus  calculations)  but  less memory space 
    consumption (47 integers).
    See MRGRand49507 for a far longer period  (2^49507,  i.e. 1.2e+14903)  with  lower 
    computation  time  too  (32-bits  modulus)  but  use  of  more  memory space (1597 
    integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseMRG()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)
    
    Inheriting classes have to define class attributes '_LIST_SIZE' and '_MODULO'. See 
    MRGRand287 for an example.

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
    
    #------------------------------------------------------------------------=
    def __init__(self, _seedState: SeedStateType = None) -> None:
        """Constructor.
        
        _seedState is either a valid state, an integer, a float or None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._LIST_SIZE integers and  an index in this list (index  value 
        being  then  in range(0,self._LIST_SIZE)).  Should _seedState be 
        a  sole  integer  or  float  then  it is used as initial seed for 
        the  random  filling  of  the  internal  list  of self._LIST_SIZE  
        integers.  Should _seedState  be anything else (e.g. None)  then  
        the  shuffling of the local current time value is used as such an 
        initial seed.
        """
        super().__init__( _seedState )
            # this  call  creates  the  two  attributes
            # self._list and self._index, and sets them
            # since it internally calls self.setstate().
            
 
    #------------------------------------------------------------------------=
    def random(self) -> float:
        """This is the core of the pseudo-random generator.
        
        Returned values are within [0.0, 1.0).
        Inheriting classes HAVE TO IMPLEMENT this method - see MRGRand287
        for an example.
        """
        raise NotImplementedError()
            
 
    #------------------------------------------------------------------------=
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the  generator.
        
        This  object  can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._LIST_SIZE integers and an 
        index in this list (index value being then in range(0,self._LIST_SIZE).
        """
        return (self._list[:], self._index)
            
 
    #------------------------------------------------------------------------=
    def setstate(self, _seedState: StateType) -> None:
        """Restores the internal state of the generator.

        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate() was called.
        About valid state:  this is a tuple containing  a   list   of  
        self._LIST_SIZE  integers (31-bits) and an index in this list 
        (index value being then in range(0,self._LIST_SIZE)).  Should 
        _seedState  be  a  sole  integer  or float then it is used as 
        initial seed for the random filling of the internal  list  of  
        self._LIST_SIZE integers.  Should _seedState be anything else
        (e.g. None) then the shuffling  of  the  local  current  time
        value is used as such an initial seed.
        """
        try:
            count = len( _seedState )
            
            if count == 0:
                self._initIndex( 0 )
                self._initList()
                
            elif count == 1:
                self._initIndex( 0 )
                self._initList( _seedState[0] )
                
            else:
                self._initIndex( _seedState[1] )
                self._list = _seedState[0][:]
                
        except:
            self._initIndex( 0 )
            self._initList( _seedState )
                       
 
    #------------------------------------------------------------------------=
    def _initIndex(self, _index: int) -> None:
        """Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._LIST_SIZE
        except:
            self._index = 0
                       
 
    #------------------------------------------------------------------------=
    def _initList(self, _initialSeed: StateType = None) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        # feeds the list according to an initial seed and the value+1 of the modulo.
        myRand = FastRand32( _initialSeed )
        self._list = [ int(myRand(self._MODULO+1)) for _ in range(self._LIST_SIZE) ]

 
#=====   end of module   basemrg.py   ========================================
