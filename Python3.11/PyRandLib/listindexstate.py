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
from typing import Final

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
        """Returns an object capturing the current internal state of the generator.
        
        This  object can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._STATE_SIZE integers and an 
        index in this list (index value being then in range(0,self._STATE_SIZE).
        """
        return (self._state, self._index)


    #-------------------------------------------------------------------------
    def seed(self, _seedState: Numerical, /) -> None:
        """Initiates the internal state of this pseudo-random generator.
        
        Should _seedState be a sole integer or float then it is  used 
        as  initial  seed for the random filling of the internal list 
        of self._STATE_SIZE integers.  Should _seedState be None then 
        the shuffling of the local current time value is used as such 
        an initial seed.
        """
        if _seedState is None or isinstance(_seedState, int | float):
            self._index = 0
            self._initstate( _seedState )
        else:
            raise TypeError( f"seed value must be None, an integer or a float (currently is of type {type(_seedState)})" )


    #-------------------------------------------------------------------------
    def setstate(self, _state: StateType, /) -> None:
        """Restores the internal state of the generator.
        
        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate()  was  called.
        About valid state:  this is a  tuple  containing  a  list  of 
        self._STATE_SIZE integers and an index in  this  list  (index 
        value being then in range [0,self._STATE_SIZE)).
        """
        if (_state is None):
            self._index = 0
            self._initstate()
        else:
            try:
                if not isinstance( _state, list | tuple ):
                    raise TypeError
                
                match len( _state ):
                    case 0:
                        self._index = 0
                        self._initstate()
                    
                    case self._STATE_SIZE:
                        self._index = 0
                        # each entry in _seedState MUST be a positive integer integer
                        if not all(isinstance(s, int)  for s in _state):  
                            raise ValueError(f"all values of internal state must be integers ({_state}")
                        if any(s < 0 for s in _state):
                            raise ValueError(f"no value in internal state may be negative ({_state}")
                        self._state = list(_state)
                    
                    case _:
                        self._initindex( _state[1] )
                        if (len(_state[0]) == self._STATE_SIZE):
                            # each entry in _seedState MUST be a positive integer
                            if not all(isinstance(s, int) and s >= 0 for s in _state[0]):
                                raise ValueError(f"all values of internal state must be integers: {_state[0]}")
                            if any(s < 0 for s in _state[0]):
                                raise ValueError(f"no value in internal state may be negative ({_state[0]})")
                            self._state = list(_state[0][:])
                        else:
                            self._initstate( _state[0] )
            
            except ValueError:
                raise

            except:
                raise TypeError( f"Incorrect type for internal state as argument of 'setstate()'. Should be tuple or list (currently is {type(_state)})" ) 


    #-------------------------------------------------------------------------
    def _initindex(self, _index: int, /) -> None:
        """Inits the internal index pointing to the internal list.
        """
        if isinstance(_index, int):
            self._index = _index % self._STATE_SIZE
        else:
            raise TypeError( f"the internal state attribute 'index' must be of type integer (currently is {type(_index)})" )


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
