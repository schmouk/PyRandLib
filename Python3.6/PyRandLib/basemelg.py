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
from .listindexstate   import ListIndexState
from .annotation_types import SeedStateType
from .splitmix         import SplitMix64


#=============================================================================
class BaseMELG( ListIndexState ):
    """Definition of the base class for all MELG pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    Maximally  Equidistributed  Long-period  Linear  Generators  (MELG)   use   linear 
    recurrence  based  on  state  transitions  with double feedbacks and linear output 
    transformations with several memory references. See reference [11] in README.md.
    
    MELGs offer large to very large periods with best known results in the  evaluation 
    of their randomness.  They ensure a maximally equidistributed generation of pseudo 
    random numbers.  They pass all TestU01 tests and newer ones but are the slowest to
    compute ones in the base of PRNGs that have been implemented in PyRandLib.

    Notice: while the WELL algorithm use 32-bits integers as their internal state  and 
    output pseudo-random 32-bits integers also, the MELG algorithm is full 64-bits.
       
    See Melg607 for a large period MELG-Generator (2^607, i.e. 5.31e+182)  with medium
    computation  time  and  the  equivalent  of  21  32-bits  integers  memory  little 
    consumption. This is the shortest period version proposed in paper [11].
    See Melg19937 for an even larger period MELG-Generator (2^19,937, i.e. 4.32e+6001),
    same computation time and equivalent of 626 integers memory consumption.
    See Melg44497 for a very large period (2^44,497,  i.e. 15.1e+13,466)  with  similar 
    computation  time  but  use  of even more memory space (equivalent of 1,393 32-bits
    integers). This is the longest period version proposed in paper [11].
    
    Please notice that this class and all its inheriting sub-classes are callable.
    Example:
    
      rand = BaseMELG()   # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attributes  '_STATE_SIZE'. See Melg607  for 
    an example.

    Reminder:
    We give you here below a copy of the table of tests for the  MELG  algorithms  that 
    have  been  implemented in PyRandLib, as provided in paper [11] and when available.

 | PyRandLib class | [11] generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Melg607         | melg607-64          |    21 x 4-bytes | 2^607   |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |
 | Melg19937       | melg19937-64        |   625 x 4-bytes | 2^19937 |    n.a.     |     4.21     |          0       |       0     |       0        |
 | Melg44497       | melg44497-64        | 1,393 x 4-bytes | 2^44497 |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """


    #-------------------------------------------------------------------------
    _NORMALIZE: float = 5.421_010_862_427_522_170_037_3e-20  # i.e. 1.0 / (1 << 64)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: int = 64
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _stateSize: int, _seedState: SeedStateType = None, /) -> None:
        """Constructor.
        
        _stateSize is the size of the internal state list of integers.
        _seedState is either a valid state,  an integer,  a float or  None.
        About   valid  state:   this  is  a  tuple  containing  a  list  of  
        self._STATE_SIZE 64-bits integers,  an index in this  list  and  an 
        additional  64-bits integer as a state extension. Should _seedState 
        be a sole integer or float then it is used as initial seed for  the 
        random filling of the internal state of the PRNG. Should _seedState 
        be anything else (e.g. None)  then  the   shuffling  of  the  local 
        current time value is used as such an initial seed.

        """
        super().__init__( SplitMix64, _stateSize, _seedState )
            # this  call  creates  the  two  attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().


#=====   end of module   basemelg.py   =======================================
