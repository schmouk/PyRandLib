"""
Copyright (c) 2025 Philippe Schmouker, ph (dot) schmouker (at) gmail.com

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


#=============================================================================
class ListIndexState( BaseRandom ):
    """The base class for all LFib PRNG based on 64-bits numbers.
        
        Definition of the class of the internal state data for many  pseudo
        random  generators: those that embed a list a integers and maybe an
        index related to this list..

        This module is part of library PyRandLib.
        
        Copyright (c) 2025 Philippe Schmouker
    """
    

    #-------------------------------------------------------------------------
    def __init__(self, _initRandClass, _stateSize: int, _seedState: SeedStateType = None, /) -> None:
        """Constructor.
        
        _initRandClass is the class to  be  instantiated  for  the  random
        initialization of the internal state list of integers.
        _stateSize is the size of the internal state list of integers.
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
        self._initRandClass = _initRandClass
        self._STATE_SIZE = _stateSize
        super().__init__( _seedState )
            # this  call  creates  the  two   attributes
            # self._state and self._index, and sets them
            # since it internally calls self.setstate().


    #-------------------------------------------------------------------------
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the  generator.
        
        This  object can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._STATE_SIZE integers and an 
        index in this list (index value being then in range(0,self._STATE_SIZE).
        """
        return (self._state[:], self._index)


    #-------------------------------------------------------------------------
    def setstate(self, _seedState: StateType, /) -> None:
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
            if (count := len( _seedState )) == 0:
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
    def _initindex(self, _index: int, /) -> None:
        """Inits the internal index pointing to the internal list.
        """
        try:
            self._index = int( _index ) % self._STATE_SIZE
        except:
            self._index = 0


    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: Numerical = None, /) -> None:
        """Inits the internal list of values.
        
        Inits the internal list of values according to some initial
        seed  that  has  to be an integer or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        initRand = self._initRandClass( _initialSeed )
        self._state = [ initRand() for _ in range(self._STATE_SIZE) ]        
