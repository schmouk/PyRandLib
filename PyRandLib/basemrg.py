"""
Copyright (c) 2016-2025 Philippe Schmouker, schmouk (at) gmail.com

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
from .annotation_types import Numerical, SeedStateType, StateType
from .splitmix         import SplitMix64


#=============================================================================
class BaseMRG( BaseRandom ):
    """Definition of the base class for all MRG pseudo-random generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

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
       
    See Mrg287 for  a  shor t period  MR-Generator  (2^287,  i.e. 2.49e+86)  with  low
    computation time but 256 integers memory consumption.
    See Mrg1457 for a longer period MR-Generator  (2^1457,  i.e. 4.0e+438)  and longer
    computation  time  (2^31-1 modulus calculations) but less memory space consumption 
    (47 integers).
    See Mrg49507 for  a  far  longer  period  (2^49507,  i.e. 1.2e+14903)  with  lower 
    computation  time  too  (32-bits  modulus)  but  use  of  more  memory space (1597 
    integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = BaseMRG()    # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Inheriting classes have to define class attributes  '_STATE_SIZE'  and  '_MODULO'. 
    See Mrg287 for an example.

    Reminder:
    We give you here below a copy of the table of tests for the MRGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRandLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Mrg287          | Marsa-LFIB4         |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | Mrg1457         | DX-47-3             |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | Mrg49507        | DX-1597-2-7         | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |

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
        return (self._state[:], self._index)
            
 
    #-------------------------------------------------------------------------
    def setstate(self, _seedState: StateType) -> None:
        """Restores the internal state of the generator.

        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate()  was  called.
        About valid state:  this is a  tuple  containing  a  list  of 
        self._STATE_SIZE integers (31-bits) and an index in this list 
        (index value being then in range(0,self._STATE_SIZE)). Should 
        _seedState  be  a  sole  integer  or float then it is used as 
        initial seed for the random filling of the internal  list  of 
        self._STATE_SIZE integers. Should _seedState be anything else
        (e.g. None) then the shuffling  of  the  local  current  time
        value is used as such an initial seed.
        """
        try:
            count = len( _seedState )
            
            if count == 0:
                self._index = 0
                self._initstate()
                
            elif count == 1:
                self._index = 0
                self._initstate( _seedState[0] )
                
            else:
                self._initindex( _seedState[1] )
                if (len(_seedState[0]) == self._STATE_SIZE):
                    self._state = _seedState[0][:]    # each entry in _seedState MUST be integer
                else:
                    self._initstate( _seedState[0] )
                
        except:
            self._index = 0
            self._initstate( _seedState )
                       
 
    #-------------------------------------------------------------------------
    def _initindex(self, _index: int) -> None:
        """Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._STATE_SIZE
        except:
            self._index = 0
                       
 
    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: Numerical = None) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        # feeds the list according to an initial seed and the value+1 of the modulo.
        initRand = SplitMix64( _initialSeed )
        self._state = [ initRand() & self._MODULO for _ in range(self._STATE_SIZE) ]

 
#=====   end of module   basemrg.py   ========================================
