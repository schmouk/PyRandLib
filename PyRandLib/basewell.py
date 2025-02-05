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
from .baserandom import BaseRandom
from .fastrand32 import FastRand32
from .types      import SeedStateType, StateType


#=============================================================================
class BaseWELL( BaseRandom ):
    """Definition of the base class for all WELL pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    Well-Equilibrated   Long-period   Linear   Generators    (WELLsGs)   uses   linear 
    recurrence based on primitive characteristic polynomials associated with left- and 
    right- shifts and xor operations to fastly evaluate pseudo-random numbers suites.
    
    WELLs offer large to very large periods with best known results in the  evaluation 
    of their randomness,  as stated in the evaluation  done  by  Pierre  L'Ecuyer  and 
    Richard Simard (Universite de Montreal) in  "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.
    Furthermore, WELLs have proven their great ability  to  very  fastly  escape  from 
    zeroland.
       
    See Well512a for a large period WELL-Generator (2^512,  i.e. 1.34e+154)  with  low
    computation time and 16 integers memory little consumption.
    See Well1024a for a longer period WELL-Generator  (2^1024,  i.e. 2.68e+308),  same 
    computation time and 32 integers memory consumption.
    See Well199937b for a far longer period  (2^19937,  i.e. 4.32e+6001) with  similar 
    computation time but use of more memory space (624 integers).
    See Well44497c  for a very large period (2^44497,  i.e. 15.1e+13466) with  similar 
    computation time but use of even more memory space (1,391 integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseWell()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)
    
    Inheriting classes have to define class attributes '_LIST_SIZE'.  See Well512a for 
    an example.

    Reminder:
    We give you here below a copy of the table of tests for the WELL  algorithms  that 
    have  been implemented in PyRandLib,  as provided in paper "TestU01, ..." and when 
    available.

 | PyRabndLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Well512a         | not available       |    16 x 4-bytes | 2^512   |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |
 | Well1024a        | WELL1024a           |    32 x 4-bytes | 2^1024  |    4.0      |     1.1      |          0       |       4     |       4        |
 | Well19937b (1)   | WELL19937a          |   624 x 4-bytes | 2^19937 |    4.3      |     1.3      |          0       |       2     |       2        |
 | Well44497c       | not available       | 1,391 x 4-bytes | 2^44497 |    n.a.     |     n.a.     |        n.a.      |     n.a.    |     n.a.       |

    (1)The Well19937b generator provided with library PyRandLib implements the
    Well19937a algorithm augmented with an associated tempering algorithm.

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
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
            
 
    #-------------------------------------------------------------------------
    def random(self) -> float:
        """This is the core of the pseudo-random generator.
        
        Returned values are within [0.0, 1.0).
        Inheriting classes HAVE TO IMPLEMENT this method - see Well1024a
        for an example.
        """
        raise NotImplementedError()
            
 
    #-------------------------------------------------------------------------
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the  generator.
        
        This  object  can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._LIST_SIZE integers and an index in this 
        list (index value being then in range(0,self._LIST_SIZE).
        """
        return (self._list[:], self._index)
            
 
    #-------------------------------------------------------------------------
    def setstate(self, _seedState: StateType) -> None:
        """Restores the internal state of the generator.

        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate() was called.
        About valid state:  this is a tuple containing  a   list   of  
        self._LIST_SIZE  integers (32-bits) and an index in this list 
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
                       
 
    #-------------------------------------------------------------------------
    def _initIndex(self, _index: int) -> None:
        """Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._LIST_SIZE
        except:
            self._index = 0
                       
 
    #-------------------------------------------------------------------------
    def _initList(self, _initialSeed: StateType = None) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        # feeds the list according to an initial seed and the value+1 of the modulo.
        myRand = FastRand32( _initialSeed )
        self._list = [ int(myRand(0x1_0000_0000)) for _ in range(self._LIST_SIZE) ]


    #-------------------------------------------------------------------------
    @classmethod
    def _d(s: int) -> int:
        #assert s >= 0
        #assert s < 32
        return 0xffff_ffff ^ (1 << s)

    #-------------------------------------------------------------------------
    @classmethod
    def _M0(cls, x: int = None) -> int:
        return 0
 
    #-------------------------------------------------------------------------
    @classmethod
    def _M1(cls, x: int) -> int:
        return x
 
    #-------------------------------------------------------------------------
    @classmethod
    def _M2_pos(cls, x: int, t: int) -> int:
        #assert t >= 0
        #assert t < 32
        return x >> t

    #-------------------------------------------------------------------------
    @classmethod
    def _M2_neg(cls, x: int, t: int) -> int:
        #assert t >= 0
        #assert t < 32
        return (x << t) & 0xffff_ffff
    
    #-------------------------------------------------------------------------
    @classmethod
    def _M3_pos(cls, x: int, t: int) -> int:
        #assert t >= 0
        #assert t < 32
        return x ^ (x >> t)

    #-------------------------------------------------------------------------
    @classmethod
    def _M3_neg(cls, x: int, t: int) -> int:
        #assert t >= 0
        #assert t < 32
        return x ^ ((x << t) & 0xffff_ffff)

    #-------------------------------------------------------------------------
    @classmethod
    def _M4(cls, x: int, a: int) -> int:
        return x >> 1 if x & 0x8000_0000 else x >> 1

    #-------------------------------------------------------------------------
    @classmethod
    def _M5_pos(cls, x: int, t: int, b: int) -> int:
        #assert t >= 0
        #assert t < 32
        return x ^ ((x >> t) & b)

    #-------------------------------------------------------------------------
    @classmethod
    def _M5_neg(cls, x: int, t: int, b: int) -> int:
        #assert t >= 0
        #assert t < 32
        return x ^ ((x << t) & b)

    #-------------------------------------------------------------------------
    @classmethod
    def _M6(cls, x: int, q: int, t: int, s: int, a: int) -> int:
        #assert q >= 0
        #assert q < 32
        #assert t >= 0
        #assert t < 32
        #assert s >= 0
        #assert s < 32
        y = (((x << q) & 0xffff_ffff) ^ (x >> (32 - q))) & cls._d(s)
        return y ^ a if x & 0x8000_0000 else y
    

#=====   end of module   basewell.py   =======================================
