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
from .baserandom import BaseRandom
from .fastrand63 import FastRand63


#=============================================================================
class BaseLFib64( BaseRandom ):
    """
    Definition of the base class for all LFib pseudo-random generators based
    on 64-bits generated numbers.
    This module is part of library PyRandLib.
    
    Copyright (c) 2017-2018 Philippe Schmouker


    Lagged Fibonacci generators LFib( m, r, k, op) use the recurrence
    
        x(i) = (x(i-r) op (x(i-k)) mod m
    
    where op is an operation that can be:
        + (addition),
        - (substraction),
        * (multiplication),
        ^(bitwise exclusive-or).
    
    With the + or - operation, such generators are in fact MRGs. They offer very large
    periods  with  the  best  known  results in the evaluation of their randomness, as
    stated in the evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de
    Montreal)  in  "TestU01:  A  C  Library  for Empirical Testing  of  Random  Number  
    Generators - ACM Transactions  on  Mathematical  Software,  vol.33 n.4,  pp.22-40, 
    August 2007".  It  is  recommended  to  use  such pseudo-random numbers generators 
    rather than LCG ones for serious simulation applications.
       
    See LFib78,  LFib116,  LFib668 and LFib1340 for long period LFib generators (resp. 
    2^78,  2^116,  2^668 and 2^1340 periods, i.e. resp. 3.0e+23, 8.3e+34, 1.2e+201 and 
    2.4e+403 periods) while same computation time and far  higher  precision  (64-bits  
    calculations)  then  MRGs,  but  memory  consumption  (resp. 17,  55, 607 and 1279 
    integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseLFib()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)
    
    Inheriting classes have to define class attribute '_LIST_SIZE'.  See LFib78 for an
    example.

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRabndLib class | TU01 generator name      | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ------------------------ | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | LFibRand78       | LFib(2^64, 17, 5, +)     |    34 x 4-bytes | 2^78    |    n.a.     |     1.1      |          0       |       0     |       0        |
 | LFibRand116      | LFib(2^64, 55, 24, +)    |   110 x 4-bytes | 2^116   |    n.a.     |     1.0      |          0       |       0     |       0        |
 | LFibRand668      | LFib(2^64, 607, 273, +)  | 1,214 x 4-bytes | 2^668   |    n.a.     |     0.9      |          0       |       0     |       0        |
 | LFibRand1340     | LFib(2^64, 1279, 861, +) | 2,558 x 4-bytes | 2^1340  |    n.a.     |     0.9      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    #=========================================================================
    def __init__(self, _seedState=None):
        """
        Constructor.
        _seedState is either a valid state, an integer,  a float or None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._LIST_SIZE integers and  an index in this list (index  value 
        being  then  in range (0,self._LIST_SIZE)).  Should _seedState be 
        a sole integer or float then it  is  used  as  initial  seed  for 
        the  random  filling  of  the  internal  list  of self._LIST_SIZE  
        integers.  Should _seedState be anything else  (e.g.  None)  then  
        the  shuffling of the local current time value is used as such an 
        initial seed.
        """
        super().__init__( _seedState )
            # this  call  creates  the  two  attributes
            # self._list and self._index, and sets them
            # since it internally calls self.setstate().
            
 
    #=========================================================================
    def random(self):
        """
        This is the core of the pseudo-random generator.
        Returned values are within [0.0, 1.0).
        Inheriting classes HAVE TO IMPLEMENT this method - see LFib78
        for an example.
        """
        raise NotImplementedError
            
 
    #=========================================================================
    def getstate(self):
        """
        Return an object capturing the current internal state of the  generator.
        This  object  can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._LIST_SIZE integers and an 
        index in this list (index value being then in range(0,self._LIST_SIZE).
        """
        return (self._list[:], self._index)
            
 
    #=========================================================================
    def setstate(self, _seedState):
        """
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
        if not isinstance( _seedState, tuple ):
            self._initIndex( 0 )
            self._initList( _seedState )
            
        elif len( _seedState ) < 2:
            self._initIndex( 0 )
            self._initList( _seedState[0] )
            
        else:
            self._initIndex( _seedState[1] )
            self._list = _seedState[0][:]
                       

    #=========================================================================
    def _initIndex(self, _index):
        """
        Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._LIST_SIZE
        except:
            self._index = 0
                       
 
    #=========================================================================
    def _initList(self, _initialSeed=None):
        """
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        myRand = FastRand63( _initialSeed )
        #-----------------------------------------------------------------
        def _getValue( _dummy ):
            myRand()
            v = myRand._value << 1
            return v + (1 if myRand() >= 0.5 else 0)
        #-----------------------------------------------------------------
        self._list = list( map( _getValue, range(self._LIST_SIZE) ) )

 
#=====   end of module   baselfib64.py   =====================================

