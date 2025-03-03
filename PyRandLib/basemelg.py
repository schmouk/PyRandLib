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
from .baserandom       import BaseRandom
from .annotation_types import SeedStateType, StateType
from .splitmix         import SplitMix64


#=============================================================================
class BaseMELG( BaseRandom ):
    """Definition of the base class for all WELL pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    Maximally  Equidistributed  Long-period  Linear  Generators  (MELG)   use   linear 
    recurrence  based  on  state  transitions  with double feedbacks and linear output 
    transformations with several memory references.
    
    MELGs offer large to very large periods with best known results in the  evaluation 
    of their randomness.  They ensure a maximally equidistributed generation of pseudo 
    random numbers.  They pass all TestU01 tests and newer ones but are the slowest to
    compute ones in the base of PRNGs that have been implemented in PyRandLib.
    See reference [11] in README.md.

    Notice: while the WELL algorithm use 32-bits integers as their internal state  and 
    output pseudo-random 32-bits integers also, the MELG algorithm is full 64-bits.
       
    See Melg607 for a large period MELG-Generator (2^607, i.e. 5.31e+182)  with medium
    computation  time  and  the  equivalent  of  21  32-bits  integers  memory  little 
    consumption. This is the shortest period version proposed in paper [11].
    See Melg19937 for an even larger period MELG-Generator (2^19937,  i.e. 4.32e+6001),
    same computation time and equivalent of 626 integers memory consumption.
    See Melg44497 for a very large  period  (2^44497,  i.e. 15.1e+13466)  with  similar 
    computation  time  but  use  of even more memory space (equivalent of 1,393 32-bits
    integers). This is the longest period version proposed in paper [11].
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseMELG()   # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attributes '_STATE_SIZE'. See Melg607  for 
    an example.

    Reminder:
    We give you here below a copy of the table of tests for the MELG  algorithms  that 
    have  been implemented in PyRandLib, as provided in paper [11] and when available.

 | PyRandLib class | [11] generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Melg607         | melg607-64          |    21 x 4-bytes | 2^607   |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |
 | Melg19937       | melg19937-64        |   626 x 4-bytes | 2^19937 |    n.a.     |     4.21     |          0       |       0     |       0        |
 | Melg44497       | melg44497-64        | 1,393 x 4-bytes | 2^44497 |    n.a.     |      n.a.    |        n.a.      |     n.a.    |     n.a.       |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, _seedState: SeedStateType = None) -> None:
        """Constructor.
        
        _seedState is either a valid state, an integer, a float or  None.
        About  valid  state:  this  is  a  tuple  containing  a  list  of  
        self._STATE_SIZE integers and an index in this list (index  value 
        being  then  in range(0,self._STATE_SIZE)).  Should _seedState be 
        a sole integer or float then it is used as initial seed  for  the 
        random filling of the internal list of self._STATE_SIZE integers. 
        Should _seedState be anything else (e.g. None) then the shuffling 
        of the local current time value is used as such an initial seed.

        """
        super().__init__( _seedState )
            # this  call  creates  the  two  attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().

 
    #-------------------------------------------------------------------------
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the  generator.
        
        This object can be passed to setstate() to restore the state. It is a
        tuple  containing a list of self._STATE_SIZE integers and an index in 
        this list (index value being then in range(0,self._STATE_SIZE).
        """
        return (self._state[:], self._index, self._extState)
            
 
    #-------------------------------------------------------------------------
    def setstate(self, _seedState: StateType) -> None:
        """Restores the internal state of the generator.

        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate()  was  called.
        Should  _seedstate not contain a list of self._STATE_SIZE 64-
        bits integers,  a value for attribute self._index and a value 
        for  attribute self._extState,  this method tries its best to 
        initialize all these values.
        """
        try:
            count = len( _seedState )
            
            if count == 0:
                self._index = 0
                self._initstate()
                self._initext()
                
            elif count == 1:
                self._index = 0
                self._initstate( _seedState[0] )
                self._initext()
            
            elif count == 2:
                self._initindex( _seedState[1] )
                if (len(_seedState[0]) == self._STATE_SIZE):
                    self._state = _seedState[0][:]    # each entry in _seedState MUST be integer
                else:
                    self._initstate( _seedState[0] )
                self._initext()

            else:
                self._initindex( _seedState[1] )
                if (len(_seedState[0]) == self._STATE_SIZE):
                    self._state = _seedState[0][:]    # each entry in _seedState MUST be integer
                else:
                    self._initstate( _seedState[0] )
                self._initext( _seedState[2] )
                
        except:
            self._index = 0
            self._initstate( _seedState )
            self._initext()

 
    #-------------------------------------------------------------------------
    def _initext(self, _ext: int = None) -> None:
        """Inits the internal state extension.

        Notice: if _ext is None, this method MUST NOT be called before 
                attributes _index and _state have been initialized.
        """
        try:
            self._extState = int( _ext )  # Notice: raises exception if _ext is None
        except:
            lastState = self._state[-1]
            self._extState = (0x5851_f42d_4c95_7f2d * (lastState ^ (lastState >> 62)) + self._index)
        
        self._extState &= 0xffff_ffff_ffff_ffff

 
    #-------------------------------------------------------------------------
    def _initindex(self, _index: int) -> None:
        """Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._STATE_SIZE
        except:
            self._index = 0
                       
 
    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: StateType = None) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        # feeds the list according to an initial seed and the value+1 of the modulo.
        initRand = SplitMix64( _initialSeed )
        self._state = [ initRand() for _ in range(self._STATE_SIZE) ]


#=====   end of module   basemelg.py   =======================================
