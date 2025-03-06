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
from typing import Tuple, Union

from .basexoroshiro    import BaseXoroshiro
from .annotation_types import Numerical, StatesList
from .splitmix         import SplitMix64


#=============================================================================
class Xoroshiro512( BaseXoroshiro ):
    """The base class for all xoroshiro PRNGs.
    
    Pseudo-random numbers generator  -  implements  the  xoroshiro512**  pseudo-random 
    generator,  the  four 64-bits integers state array version of the Scrambled Linear 
    Pseudorandom Number Generators. It provides 64-bits pseudo random values, a medium 
    period  2^512 (i.e. about 1.34e+154),  jump ahead feature,  very short escape from 
    zeroland (30 iterations only) and passes TestU01 tests.

    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    The base xoroshiro linear transformation  is  obtained  combining  a  rotation,  a 
    shift,  and  again  a  rotation.  An  additional  scrambling  method  based on two 
    multiplications is also computed for this version xoroshiro512** of the algorithm.
    
    See Xoroshiro256 for a large 2^256 period (i.e. about  1.16e+77)  scramble  linear 
    PRNG,  with  low  computation  time,  64-bits  output  values  and good randomness
    characteristics.
    See Xoroshiro1024 for a large 2^1024 period (i.e. about 1.80e+308) scramble linear 
    PRNG,  with  low computation time,  64-bits output values and very good randomness
    characteristics.

    Furthermore this class is callable:
      rand = Xoroshiro512()
      print( rand() )        # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )       # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) )    # prints a list of n pseudo-random values each within [0, a)
    
    Reminder:
    We give you here below a copy of the table of tests for the xoroshiros  that  have
    been  implemented  in PyRandLib,  as  described  by the authors of xoroshiro - see 
    reference [10] in file README.md.

 | PyRandLib class | initial xoroshiro algo name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | --------------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Xoroshiro256    | xoroshiro256**              |    16 x 4-bytes | 2^256   |    n.a.     |     0.84     |          0       |       0     |       0        |
 | Xoroshiro512    | xoroshiro512**              |    32 x 4-bytes | 2^512   |    n.a.     |     0.99     |          0       |       0     |       0        |
 | Xoroshiro1024   | xoroshiro1024**             |    64 x 4-bytes | 2^1,024 |    n.a.     |     1.17     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    def __init__(self, _seedState: Union[Numerical, StatesList] = None) -> None:
        """Constructor.
        
        _seedState is either a valid state, an integer,  a float or None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._STATE_SIZE integers and  an index in this list (index  value 
        being  then  in range (0,self._STATE_SIZE)).  Should _seedState be 
        a sole integer or float then it  is  used  as  initial  seed  for 
        the  random  filling  of  the  internal  list  of self._STATE_SIZE  
        integers.  Should _seedState be anything else  (e.g.  None)  then  
        the  shuffling of the local current time value is used as such an 
        initial seed.
        """
        super().__init__( _seedState )
            # this  call  creates  the  two   attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator. It returns the next pseudo random integer value generated by the inheriting generator.
        """
        currentS1 = self._state[1]
        # advances the internal state of the PRNG
        self._state[2] ^= self._state[0]
        self._state[5] ^= self._state[1]
        self._state[1] ^= self._state[2]
        self._state[7] ^= self._state[3]
        self._state[3] ^= self._state[4]
        self._state[4] ^= self._state[5]
        self._state[0] ^= self._state[6]
        self._state[6] ^= self._state[7]
        self._state[6] ^= (currentS1 << 11) & self._MODULO
        self._state[7] = self._rotleft( self._state[7], 21 )
        # returns the output value
        return (self._rotleft( currentS1 * 5, 7) * 9) & self._MODULO


    #-------------------------------------------------------------------------
    def getstate(self) -> Tuple[ int ]:
        """Returns an object capturing the current internal state of the  generator.
        
        This object can be passed to setstate() to restore the state. 
        It is a tuple containing a list of self._STATE_SIZE integers.
        """
        return (self._s0, self._s1, self._s2, self._s3)


    #-------------------------------------------------------------------------
    def setstate(self, _seedState: Union[ Numerical, StatesList ] = None) -> None:
        """Restores the internal state of the generator.
        
        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate()  was  called.
        About  valid  state:  this  is  a  list  of  self._STATE_SIZE 
        integers (64-bits). Should _seedState be a  sole  integer  or 
        float  then it is used as initial seed for the random filling 
        of the internal list  of  self._STATE_SIZE  integers.  Should 
        _seedState be anything else (e.g. None) then the shuffling of 
        the local current time value is used as such an initial seed.
        """
        try:
            count = len( _seedState )
            
            if count == 0:
                self._initstate()
                
            elif count == 1:
                self._initstate( _seedState[0] )
                
            else:
                if (len(_seedState[0]) == self._STATE_SIZE):
                    self._state = _seedState[:]    # Notice: all entries MUST BE integers and not all zero
                else:
                    self._initstate( _seedState[0] )
                
        except:
            self._initstate( _seedState )


    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: Numerical = None) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        initRand = SplitMix64( _initialSeed )
        self._state = [ initRand() for _ in range(8) ]


#=====   end of module   xoroshiro512.py   ===================================

