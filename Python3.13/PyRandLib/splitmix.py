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
import time
from typing import override

from .annotation_types import Numerical


#=============================================================================
class SplitMix64:
    """The splitting and mixing algorithm used to initialize internal states of PRNGs.

    This class and its inheriting classes are  only  provided  for  the 
    initialization of the internal state of all other PRNGs.  It SHOULD 
    NOT BE USED as a generic PRNG due to is randomness big limitations.

    This class evaluates "random" values on 64 bits.  It implements the
    64-bits  version   of   the  Fast  Splittable  Pseudorandom  Number 
    Generators proposed by Steele Jr, Guy L.,  Doug Lea,  and Christine 
    H. Flood in  "Fast splittable pseudorandom number generators.",  in
    ACM SIGPLAN Notices 49.10 (2014): pp. 453-472.
    
    It uses the Gamma method inited by Sebastiano Vigna (vigna@acm.org) 
    in  2015,  provided under the Creative Commons license and modified 
    under the same license by D. Lemire by Aug. 2017.
    (see https://github.com/lemire/testingRNG/blob/master/source/splitmix64.h).
    """
    #-------------------------------------------------------------------------
    def __init__(self, _seed: Numerical = None, /) -> None:
        """Constructor.

        Should _seed be None, the internal system local time is used as the initial seed
        """
        if isinstance( _seed, int ):
            self.state = self.__call__( _seed )

        elif isinstance( _seed, float ):
            # transforms passed initial seed from float to integer
            if _seed < 0.0 :
                _seed = -_seed
            
            if _seed >= 1.0:
                self._state = self.__call__( round(_seed) )
            else:
                self._state = self.__call__( int(_seed * 0x1_0000_0000_0000_0000) )

        else:
            # uses system local time
            self._state = self.__call__( int(time.time() * 1000.0) )
        

    #-------------------------------------------------------------------------
    def __call__(self, _seed: int = None, /) -> int:
        """The split-mix algorithm.
        """
        if _seed is not None:
            self._state = _seed & 0xffff_ffff_ffff_ffff

        self._state += 0x9e37_79b9_7f4a_7c15  # this is the 'Golden' Gamma value: int( ((1+math.sqrt(5))/2) * 2**64) & 0xffff_ffff_ffff_ffff
        self._state &= 0xffff_ffff_ffff_ffff

        z = self._state
        z = ((z ^ (z >> 30)) * 0xbf5_8476_d1ce_4e5b9) & 0xffff_ffff_ffff_ffff
        z = ((z ^ (z >> 27)) * 0x94d_049b_b133_111eb) & 0xffff_ffff_ffff_ffff

        return z ^ (z >> 31)
    

#=============================================================================
class SplitMix63( SplitMix64 ):
    """The splitting and mixing algorithm used to initialize internal states of PRNGs.

    This class and its inheriting classes are  only  provided  for  the 
    initialization of the internal state of all other PRNGs.  It SHOULD 
    NOT BE USED as a generic PRNG due to is randomness big limitations.

    This class evaluates "random" values on 63 bits.
    """
    #-------------------------------------------------------------------------
    def __init__(self, _seed: Numerical = None, /) -> None:
        """Constructor.

        Should _seed be None, the internal system local time is used as the initial seed
        """
        super().__init__( _seed )
    
    #-------------------------------------------------------------------------
    @override
    def __call__(self, _seed: int = None, /) -> int:
        """The split-mix algorithm.
        """
        # returns the 63 higher bits generated by base class operator ()
        return super().__call__( _seed ) >> 1
    

#=============================================================================
class SplitMix32( SplitMix64 ):
    """The splitting and mixing algorithm used to initialize internal states of PRNGs.

    This class and its inheriting classes are  only  provided  for  the 
    initialization of the internal state of all other PRNGs.  It SHOULD 
    NOT BE USED as a generic PRNG due to is randomness big limitations.

    This class evaluates "random" values on 32 bits.
    """
    #-------------------------------------------------------------------------
    def __init__(self, _seed: Numerical = None, /) -> None:
        """Constructor.

        Should _seed be None, the internal system local time is used as the initial seed
        """
        super().__init__( _seed )
    
    #-------------------------------------------------------------------------
    @override
    def __call__(self, _seed: int = None, /) -> int:
        """The split-mix algorithm.
        """
        # returns the 32 higher bits generated by base class operator ()
        return super().__call__( _seed ) >> 32


#=====   end of module   splitmix.py   =======================================
