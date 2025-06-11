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
from .annotation_types import Numerical, SeedStateType, StateType
from .pcg64_32         import Pcg64_32
from .splitmix         import SplitMix32


#=============================================================================
class Pcg1024_32( Pcg64_32 ):
    """
    Pseudo-random  numbers  generator  -  Permutated  Congruential  Generator 
    extended  by  1,024  equidistributed  generators,  dedicated  to  64-bits 
    calculations and 32-bits output with very large period (about 6.53e+9882) 
    but  very short time computation.  This version of the PCG algorithm gets
    the largest memory consumption: 1,026 x 4-bytes. The PCG algorithm offers 
    jump ahead and multi streams features.

    This module is part of library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    As LCGs do, PCG models evaluate pseudo-random numbers  suites  x(i)  as  a 
    simple mathematical function of x(i-1):
 
       x(i) = (a * x(i-1) + c) mod m

    PCGs associate to this recurrence a permutation of a subpart o f the  bits 
    of  the internal state of the PRNG.  The output of PCGs is this permutated
    subpart of its internal state,  leading to a very large enhancement of the
    randomness of these algorithms compared with the LCGs one.
    
    These PRNGs have been tested with TestU01 and have shown to pass all tests
    (Pierre  L'Ecuyer and Richard Simard (Universite de Montreal) in 'TestU01: 
    A C Library for Empirical  Testing  of  Random  Number  Generators  -  ACM 
    Transactions on Mathematical Software, vol.33 n.4, pp.22-40, August 2007')
  
    PCGs are very fast generators, with low memory usage except for a very few 
    of them and medium to very large periods.  They offer jump ahead and multi
    streams features for most of them. They are difficult to very difficult to
    invert and to predict.

    The Pcg1024_32 class implements the "PCG XSH RS 64/32 (EXT 1024)"  version 
    of  th e PCG  algorithm,  as  specified  in  the related paper (see [7] in 
    document README.md), so with a and c coded on 64-bits, the modulo m = 2^64 
    and  the  additional permutation output function and its internal multiple 
    states that implements its  1024-dimensionally  equidistributed  generator
    directly coded in method 'next()'.

    See Pcg64_32 for a 2^64 (i.e. about 1.84e+19) period PC-Generator with low 
    computation  time  also  and  a  longer  period than for Pcg64_32,  with 2 
    32-bits word integers memory consumption.  Output values are  returned  on 
    32 bits.

    See Pcg128_64 for a 2^128 (i.e. about 3.40e+38) period  PC-Generator  with  
    low  computation  time also and a longer period than for Pcg64_32,  with 4 
    32-bits word integers memory consumption.  Output values are  returned  on 
    64 bits.

    See Pcg1024_32 for a 2^32,830 (i.e. about 6.53e+9882) period  PC-Generator
    with low computation time also and a very large period,  but 1,026 32-bits
    word integers memory consumption. Output values are returned on 32 bits.
      
    Furthermore this class is callable:
      rand = Pcg1024_32()
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)

    Notice that for simulating the roll of a dice you should program:
      diceRoll = Pcg1024_32()
      print( int(diceRoll.randint(1, 6)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Reminder:
    We give you here below a copy of the table of tests for the PCGs that have 
    been  implemented  in  PyRandLib,  as provided by the author of PCGs - see
    reference [7] in file README.md.

 | PyRandLib class | initial PCG algo name       | Memory Usage    | Period   | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | --------------- | --------------------------- | --------------- | -------- | ------------ | ---------------- | ----------- | -------------- |
 | Pcg64_32        | PCG XSH RS 64/32 (LCG)      |     2 x 4-bytes | 2^64     |     0.79     |          0       |       0     |       0        |
 | Pcg128_64       | PCG XSL RR 128/64 (LCG)     |     4 x 4-bytes | 2^128    |     1.70     |          0       |       0     |       0        |
 | Pcg1024_32      | PCG XSH RS 64/32 (EXT 1024) | 1,026 x 4-bytes | 2^32,830 |     0.78     |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRNG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics
    * _big crush_ is the ultimate set of difficult tests that  any  GOOD  PRNG 
    should definitively pass.
    """

    #-------------------------------------------------------------------------
    _EXTENDED_STATE_SIZE: int = 1024


    #-------------------------------------------------------------------------
    def __init__(self, _seed: SeedStateType = None) -> None:
        """Constructor.
        
        Should _seed be None or not be of SeedStateType then the 
        local time is used (with its shuffled value) as a seed.
        """
        super().__init__( _seed ) # this call creates attributes self._state and self._externalState and sets them


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator.
        """
        # evaluates a to-be-xor'ed 32-bits value from current extended state
        if self._state & 0xffff_ffff == 0:
            self._advancetable()
        extendedValue = self._externalState[ self._state & 0x03ff ]

        # then xor's it with the next 32-bits value evaluated with the internal state
        return super().next() ^ extendedValue


    #-------------------------------------------------------------------------
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the  generator.
        
        This object can be passed to setstate() to restore the state.
        It is a list that contains self._STATE_SIZE integers.
        """
        return (self._externalState[:], self._state)


    #-------------------------------------------------------------------------
    def setstate(self, _seedState: SeedStateType) -> None:
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
            count = len(_seedState)

            if count == 0:
                self._initstate()

            elif count == Pcg1024_32._EXTENDED_STATE_SIZE:
                # sets the internal state
                super().setstate()
                # then sets the external state
                if not all(isinstance(s, int) for s in _seedState):  # each entry in _seedState MUST be integer
                    raise ValueError("all values of external state must be integers")
                self._externalState = [s & 0xffff_ffff for s in _seedState]

            elif count == 2:
                # each entry in _seedState[0] MUST be a 32-bits integer
                extendedCount = len( _seedState[0] )
                if extendedCount == Pcg1024_32._EXTENDED_STATE_SIZE:
                    # sets the internal state, MUST be a 64-bits integer
                    if isinstance(_seedState[1], int):
                        self._state = _seedState[1] & 0xffff_ffff_ffff_ffff
                    else:
                        raise ValueError(f"seed values for internal state must be integers (currently is {_seedState[1]})")
                    # then sets the external state, MUST be 32-bits integers
                    if all(isinstance(s, int) for s in _seedState[0]):
                        self._externalState = [s & 0xffff_ffff for s in _seedState[0]]
                    else:
                        raise ValueError("all values of external state must be integers")
                else:
                    self._initstate( _seedState[1] )
                
            else:
                self._initstate()
                        
        except ValueError as exc:
            raise exc

        except:
            self._initstate( _seedState )


    #-------------------------------------------------------------------------
    def _advancetable(self) -> None:
        """Advances the extended states
        """
        carry = False
        for i, s in enumerate( self._externalState ):
            if carry:
                carry = self._extendedstep(s, i)
            if self._extendedstep(s, i):  # notice: must be evaluated before carry is set
                carry = True


    #-------------------------------------------------------------------------
    def _extendedstep(self, value: int, i: int) -> bool:
        """Evaluates new extended state indexed value in the extended state table.

        Returns True when the evaluated extended value is set to zero on all bits
        but its two lowest ones - these two bits never change with MCGs.
        """
        state = (0xacb8_6d69 * (value ^ (value >> 22))) & 0xffff_ffff
        state = self._invxrs( state, 32, 4 + (state >> 28) & 0x0f )
        state = (0x108e_f2d9 * state + 2 * (i + 1)) & 0xffff_ffff

        result = 0x108e_f2d9 * (state ^ (state >> (4 + (state >> 28))))
        result ^= result >> 22

        self._externalState[i] = result

        return result == state & 0b11


    #-------------------------------------------------------------------------
    def _initexternalstate(self, _initialSeed: Numerical = None) -> None:
        """Inits the extended list of values.
        
        Inits the extended list of values according to some initial
        seed  that  has to be an integer, or a float ranging within
        [0.0, 1.0).  Should it be None or anything  else  then  the
        current local time value is used as initial seed value.
        """
        # feeds the list according to an initial seed.
        initRand = SplitMix32( _initialSeed )
        self._externalState = [ initRand() for _ in range(Pcg1024_32._EXTENDED_STATE_SIZE) ]
        

    #-------------------------------------------------------------------------
    def _initstate(self, _initialSeed: Numerical = None) -> None:
        """Inits the internal state of this PRNG.

        Inits its current state and its  extended  state  also.  The
        initial seed has to be an integer, or a float ranging within
        [0.0, 1.0).  Should it be None or  anything  else  then  the
        current  local time value is used as the initial seed value.
        The same initial seed is finally used to  seed  the  current
        state  and  the  extended  state.  To  avoid  any unexpected 
        correlation between current  state  and  any  value  of  the 
        extended  one,  we  use different PRNGs to seed the internal 
        state on one side and the extended state on the other side.
        Raises exception ValueError if _initialSeed is a  float  and 
        its value is out of range [0.0, 1.0].
        """
        super().setstate( _initialSeed )        # uses Pcg64_32()
        self._initexternalstate( _initialSeed ) # uses Well1024a()


    #-------------------------------------------------------------------------
    @classmethod
    def _invxrs(cls, value: int, bitsCount: int, shift: int) -> int:
        """Evaluates the inversion of an xor-shift operation.
        """
        if shift * 2 >= bitsCount:
            return value ^ (value >> shift)

        botMask = (1 << (bitsCount - shift * 2)) - 1
        topMask = ~botMask & 0xffff_ffff

        top = (value ^ (value >> shift)) & topMask

        newBitsShift = bitsCount - shift
        bot = cls._invxrs( (top | (value & botMask)) & ((1 << newBitsShift) - 1), newBitsShift, shift ) & botMask
        
        return top | bot


#=====   end of module   pcg1024_32.py   =====================================
