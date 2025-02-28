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
from .annotation_types import SeedStateType, StatesList


#=============================================================================
class BaseSquares( BaseRandom ):
    """Definition of the base class for the Squares counter-based pseudo-random Generator.
    
    This module is part of library PyRandLib.

    Copyright (c) 2025 Philippe Schmouker

    Squares models are based on an incremented counter and a key.  The 
    algorithm squares a combination of the counter and the key values, 
    and exchanges the upper and lower bits  of  the  combination,  the 
    whole  repeated  a number of times (4 to 5 rounds).  Output values 
    are provided on 32-bits or on 64-bits according to the model.  See 
    [9] in README.md.

    See Squares32 for a 2^64 (i.e. about 1.84e+19)  period  PRNG  with 
    low  computation  time,  medium period,  32-bits output values and 
    very good randomness characteristics.

    See Squares64 for a 2^64 (i.e. about 1.84e+19)  period  PRNG  with 
    low  computation  time,  medium period,  64-bits output values and 
    very good randomness characteristics.

    Furthermore this class is callable:
      rand = BaseSquares()# Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Reminder:
    We give you here below a copy of the table of tests for the Squares 
    that have been implemented in PyRandLib,  as presented in paper [9]
    - see file README.md.

 | PyRandLib class | [9] generator name | Memory Usage  | Period   | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | ------------------ | ------------- | -------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | Squares32       | squares32          |  4 x 4-bytes  |   2^64   |    n.a.     |     n.a.     |          0       |       0     |       0        |
 | Squares64       | squares64          |  4 x 4-bytes  |   2^64   |    n.a.     |     n.a.     |          0       |       0     |       0        |_

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
        
        Should _seedState be None then the local time is used as a seed  (with 
        its shuffled value).
        Notice: method setstate() is not implemented in base class BaseRandom.
        So,  it  must be implemented in classes inheriting BaseLCG and it must
        initialize attribute self._state.
        """
        super().__init__( _seedState )  # this internally calls 'setstate()'  which
                                        # MUST be implemented in inheriting classes


    #-------------------------------------------------------------------------
    def getstate(self) -> StatesList:
        """Returns an object capturing the current internal state of the generator.
        
        This object can be passed to setstate() to restore the state.
        For  CWG,  this  state is defined by a list of control values 
        (a, weyl and s - or a list of 4 coeffs) and an internal state 
        value,  which  are used in methods 'next() and 'setstate() of 
        every inheriting class.

        All inheriting classes MUST IMPLEMENT this method.
        """
        raise NotImplementedError()
    

    #-------------------------------------------------------------------------
    def _initKey(self, _seed: int = None) -> int:
        """Initalizes the attribute _key according to the original recommendations - see [9].
        """
        #TODO: implement this
        return 0xa589f_cb13_d7e6_34cb


#=====   end of module   basesquares.py   ====================================
