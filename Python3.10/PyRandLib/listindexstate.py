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
        """Returns an object capturing the current internal state of the generator.
        
        This  object can be passed to setstate() to restore the state.  It is a
        tuple containing a list of self._STATE_SIZE integers and an 
        index in this list (index value being then in range(0,self._STATE_SIZE).
        """
        return (self._state, self._index)


    #-------------------------------------------------------------------------
    def seed(self, _seed: Numerical = None, /) -> None:
        """Initiates the internal state of this pseudo-random generator.
        
        Should _seedState be a sole integer or float then it is  used 
        as  initial  seed for the random filling of the internal list 
        of self._STATE_SIZE integers.  Should _seedState be None then 
        the shuffling of the local current time value is used as such 
        an initial seed.
        """
        if _seed is None or isinstance(_seed, int | float):
            self._index = 0
            self._initstate( _seed )
        else:
            raise TypeError( f"seed value must be None, an integer or a float (currently is of type {type(_seed)})" )


    #-------------------------------------------------------------------------
    def setstate(self, _state: StateType = None, /) -> None:
        """Restores the internal state of the generator.
        
        _seedState should have been obtained from a previous call  to 
        getstate(), and setstate() restores the internal state of the 
        generator to what it was at the time setstate()  was  called.
        About valid state:  this is a  tuple  containing  a  list  of 
        self._STATE_SIZE integers and an index in  this  list  (index 
        value being then in range [0,self._STATE_SIZE)).
        """
        if (_state is None):
            self.seed()

        elif not isinstance( _state, list | tuple ):
            raise TypeError(f"initialization state must be a tuple or a list (actually is {type(_state)})")
        
        else:
            match len( _state ):
                case 0:
                    self._initindex( 0 )
                    self._initstate()
                
                case self._STATE_SIZE:
                    self._initindex( 0 )
                    # each entry in _seedState MUST be a positive integer integer
                    if not all(isinstance(s, int) and s >= 0 for s in _state):  
                        raise ValueError(f"all values of internal state must be non negative integers ({_state}")
                    else:
                        self._state = list(_state)
                
                case _:
                    if not isinstance( _state[0], list | tuple ):
                        raise TypeError(f"initialization state must be a tuple or a list (actually is {type(_state[0])})")
                    elif (len(_state[0]) != self._STATE_SIZE):
                        raise ValueError(f"Incorrect size for initializing state (should be {self._STATE_SIZE} integers, currently is {len(_state)})")
                    else:
                        self._initindex( _state[1] )
                        # each entry in _seedState MUST be a positive or null integer
                        if not all(isinstance(s, int) and s >= 0 for s in _state[0]):
                            raise ValueError(f"all values of internal state must be non negative integers: {_state[0]}")
                        else:
                            self._state = list(_state[0])


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
