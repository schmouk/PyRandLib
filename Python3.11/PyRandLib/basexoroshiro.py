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
from typing import Final

from .baserandom       import BaseRandom
from .annotation_types import Numerical, StatesList, StateType
from .splitmix         import SplitMix64


#=============================================================================
class BaseXoroshiro( BaseRandom ):
    """The base class for all xoroshiro PRNGs.
    
    Definitiion of the base class for all versions of the xoroshiro algorithm
    implemented in PyRandLib.

    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    The xoroshiro algorithm is a version of the Scrambled Linear  Pseudorandom  Number
    Generators.  The xoroshiro linear transformation updates cyclically two words of a 
    larger state array. The base xoroshiro linear transformation is obtained combining 
    a rotation, a shift, and again a rotation.
    (extracted from the original paper, see [10] in file README.md)

    An addition or a multiplication operation is internally applied also to the  state 
    of  the  PRNGs.  Doubling the same operation has proven to enhance then randomness 
    quality of the PRNG.  This is the model of the algorithms that  is  implemeted  in
    PyRandLib.

    The implemented algorithms shortly escape from the zeroland (10 to 100  calls  are 
    enough  to  get  equiprobability  of bits 0 and 1 on 4 successive calls).  The 256 
    version of the algorithm has nevertheless shown close repeats flaws,  with  a  bad 
    Hamming weight near zero. Xoroshiro512 seems to best fit this property.
    (see https://www.pcg-random.org/posts/xoshiro-repeat-flaws.html).
    
    See Xoroshiro256, Xoroshiro512, Xoroshiro1024 for long  period  generators  (resp. 
    2^256,  2^512  and  2^1024 periods,  i.e. resp. 1.16e+77,  1.34e+154 and 1.80e+308 
    periods),  64-bits precision calculations and short memory consumption  (resp.  8, 
    16 and 32 integers coded on 64 bits.
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseXoroshiro() # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )        # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )       # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) )    # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attribute '_STATE_SIZE'. See Xoroshiro1024
    for an example.

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
    _NORMALIZE: Final[float ]= 5.421_010_862_427_522_170_037_3e-20  # i.e. 1.0 / (1 << 64)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: Final[int] = 64
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    _MODULO: Final[int] = (1 << 64) - 1


    #-------------------------------------------------------------------------
    def __init__(self, _seedState: Numerical | StatesList = None, /) -> None:
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
    def getstate(self) -> list[int]:
        """Returns an object capturing the current internal state of the  generator.
        
        This object can be passed to setstate() to restore the state. 
        It is a tuple containing a list of self._STATE_SIZE integers.
        """
        return self._state[:]


    #-------------------------------------------------------------------------
    def setstate(self, _seedState: Numerical | StatesList = None, /) -> None:
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
            match len( _seedState ):
                case 0:
                    self._initstate()
                
                case 1:
                    self._initstate( _seedState[0] )
                
                case _:
                    if (len(_seedState[0]) == self._STATE_SIZE):
                        self._state = _seedState[:]    # each entry in _seedState MUST be integer
                    else:
                        self._initstate( _seedState[0] )
                
        except:
            self._initstate( _seedState )


    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: Numerical = None, /) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        initRand = SplitMix64( _initialSeed )
        self._state = [ initRand() for _ in range(self._STATE_SIZE) ]        


#=====   end of module   basexoroshiro.py   ==================================

