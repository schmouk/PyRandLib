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
from random import Random

from .annotation_types import Numerical, SeedStateType, StateType


#=============================================================================
class BaseRandom( Random ):
    """This is the base class for all pseudo-random numbers generators.
    
    This module is part of library PyRandLib.
    
    Copyright (c) 2016-2025 Philippe Schmouker

    See FastRand32 for a 2^32 (i.e. 4.29e+9) period LC-Generator and FastRand63 for  a  
    2^63 (i.e. about 9.2e+18) period  LC-Generator with very low computation time with 
    very low memory consumption (resp. 1 and 2 32-bits integers).
           
    See LFibRand78, LFibRand116, LFibRand668 and LFibRand1340 for  large  period  LFib
    generators  (resp.  2^78,  2^116,  2^668  and 2^1340 periods,  i.e. resp. 3.0e+23,
    8.3e+34, 1.2e+201 and 2.4e+403 periods) while same computation time and far higher
    precision  (64-bits  calculations) but memory consumption (resp. 17,  55,  607 and
    1279 32-bits integers).

    See Mrg287 fo r a  short  period  MR-Generator  (2^287,  i.e. 2.49e+86)  with  low
    computation time but 256 32-bits integers memory consumption.
    See Mrg1457 for a longer period MR-Generator  (2^1457,  i.e. 4.0e+438)  and longer
    computation  time  (2^31-1 modulus calculations) but less memory space consumption 
    (32-bits 47 integers).
    See  Mrg49507  for  a  far  larger  period  (2^49507,  i.e. 1.2e+14903)  with  low 
    computation  time  too  (31-bits  modulus)  but  use  of  more  memory space (1597 
    32-bits integers).

    See Pcg64_32, Pcg128_64 and Pcg1024_32 for medium to very large periods,  very low 
    computation time,  and for very low memory consumption for the two first (resp. 4, 
    8 and 1,026 times 32-bits).  Associated periods are resp. 2^64, 2^128 and 2^32830, 
    i.e. 1.84e+19, 3.40e+38 and 6.53e+9882. These PRNGs provide multi-streams and jump 
    ahead features.  Since they all are exposing only a part of their internal  state, 
    they are difficult to reverse and to predict.

    See Well512a, Well1024a, Well19937c and Well44479b for large to very large  period 
    generators (resp. 2^512, 2^1024, 2^19937 and 2^44479 periods, i.e. resp. 1.34e+154,
    2.68e+308,  4.32e+6001 and 1.51e+13466 periods),  a little bit longer  computation 
    times but very quick escaping from zeroland.  Memory consumption is resp. 32,  64, 
    624 and 1391 32-bits integers.

    Python built-in class random.Random is subclassed here to use  a  different  basic 
    generator of our own devising: in that case, overriden methods are:
    
      random(), seed(), getstate(), and setstate().

    Since version 2.0 of PyRandLib,  the core engine of every PRNG is coded in  method
    next().
    
    Furthermore this class and all its inheriting sub-classes are callable. Example:
      rand = BaseRandom() # Caution: this is just used as illustrative. This base class cannot be instantiated
      print( rand() )     # prints a pseudo-random value within [0.0, 1.0)
      print( rand(a) )    # prints a pseudo-random value within [0, a) or [0.0, a) depending on the type of a
      print( rand(a, n) ) # prints a list of n pseudo-random values each within [0, a)
    
    Please notice that for simulating the roll of a dice you should program:
      diceRoll = UFastRandom()
      print( int( diceRoll(1, 7) ) ) # prints a uniform roll within {1, ..., 6}.
    Such a programming is a simplified  while  still  robust  emulation  of  inherited
    methods random.Random.randint(self,1,6) and random.Random.randrange(self,1,7,1).
 
    Inheriting from random.Random, next methods are also available:
     |
     |  betavariate(self, alpha, beta)
     |      Beta distribution.
     |      
     |      Conditions on the parameters are alpha > 0 and beta > 0.
     |      Returned values range between 0 and 1.
     |  
     |
     |  choice(self, seq)
     |      Choose a random element from a non-empty sequence.
     |  
     |
     |  binomialvariate**(self, n=1, p=0.5)
     |      Binomial distribution. Return the number of successes for n 
     |      independent trials with the probability of success in each 
     |      trial being p.
     |      Notice: added since Python 3.12, implemented in PyRandLib
     |              for all previous versions of Python.
     |      n >= 0, 0.0 <= p <= 1.0,
     |      the result is an integer in the range 0 <= X <= n.
     |  
     |
     |  expovariate(self, lambd=1.0)
     |      Exponential distribution.
     |      
     |      lambd is 1.0 divided by the desired mean.  It should be
     |      nonzero.  (The parameter would be called "lambda", but that is
     |      a reserved word in Python.)  Returned values range from 0 to
     |      positive infinity if lambd is positive, and from negative
     |      infinity to 0 if lambd is negative.
     |  
     |
     |  gammavariate(self, alpha, beta)
     |      Gamma distribution.  Not the gamma function!
     |      
     |      Conditions on the parameters are alpha > 0 and beta > 0.
     |  
     |
     |  gauss(self, mu, sigma)
     |      Gaussian distribution.
     |      
     |      mu is the mean, and sigma is the standard deviation.  This is
     |      slightly faster than the normalvariate() function.
     |      
     |      Not thread-safe without a lock around calls.
     |  
     |  
     |  getrandbits(self, k)
     |      Returns a non-negative Python integer with k random bits.
     |      Changed since version 3.9: This method now accepts zero for k.
     |  
     |
     |  getstate(self)
     |      Return internal state; can be passed to setstate() later.
     |  
     |
     |  lognormvariate(self, mu, sigma)
     |      Log normal distribution.
     |      
     |      If you take the natural logarithm of this distribution, you'll get a
     |      normal distribution with mean mu and standard deviation sigma.
     |      mu can have any value, and sigma must be greater than zero.
     |  
     |
     |  normalvariate(self, mu, sigma)
     |      Normal distribution.
     |      
     |      mu is the mean, and sigma is the standard deviation.
     |  
     |
     |  paretovariate(self, alpha)
     |      Pareto distribution.  alpha is the shape parameter.
     |  
     |
     |  randbytes(self, n)
     |      Generate n random bytes.
     |      This method should not be used for generating security tokens.
     |      Notice: this method has been added in Python 3.9. It is implemented
     |      in PyRandLib for former versions of the language also.
     |  
     |
     |  randint(self, a, b)
     |      Return random integer in range [a, b], including both end points.
     |  
     |
     |  randrange(self, start, stop=None, step=1, int=<class 'int'>)
     |      Choose a random item from range(start, stop[, step]).
     |      
     |      This fixes the problem with randint() which includes the
     |      endpoint; in Python this is usually not what you want.
     |      
     |      Do not supply the 'int' argument.
     |  
     |
     |  sample(self, population, k)
     |      Chooses k unique random elements from a population sequence or set.
     |      
     |      Returns a new list containing elements from the population while
     |      leaving the original population unchanged.  The resulting list is
     |      in selection order so that all sub-slices will also be valid random
     |      samples.  This allows raffle winners (the sample) to be partitioned
     |      into grand prize and second place winners (the subslices).
     |      
     |      Members of the population need not be hashable or unique.  If the
     |      population contains repeats, then each occurrence is a possible
     |      selection in the sample.
     |      
     |      To choose a sample in a range of integers, use range as an argument.
     |      This is especially fast and space efficient for sampling from a
     |      large population:   sample(range(10000000), 60)
     |  
     |
     |  seed(self, a=None, version=2)
     |      Initialize internal state from hashable object.
     |      
     |      None or no argument seeds from current time or from an operating
     |      system specific randomness source if available.
     |      
     |      For version 2 (the default), all of the bits are used if *a *is a str,
     |      bytes, or bytearray.  For version 1, the hash() of *a* is used instead.
     |      
     |      If *a* is an int, all bits are used.
     |  
     |
     |  setstate(self, state)
     |      Restore internal state from object returned by getstate().
     |  
     |
     |  shuffle(self, x, random=None, int=<class 'int'>)
     |      x, random=random.random -> shuffle list x in place; return None.
     |      
     |      Optional arg random is a 0-argument function returning a random
     |      float in [0.0, 1.0); by default, the standard random.random.
     |  
     |
     |  triangular(self, low=0.0, high=1.0, mode=None)
     |      Triangular distribution.
     |      
     |      Continuous distribution bounded by given lower and upper limits,
     |      and having a given mode value in-between.
     |      
     |      http://en.wikipedia.org/wiki/Triangular_distribution
     |  
     |
     |  uniform(self, a, b)
     |      Get a random number in the range [a, b) or [a, b] depending on rounding.
     |  
     |
     |  vonmisesvariate(self, mu, kappa)
     |      Circular data distribution.
     |      
     |      mu is the mean angle, expressed in radians between 0 and 2*pi, and
     |      kappa is the concentration parameter, which must be greater than or
     |      equal to zero.  If kappa is equal to zero, this distribution reduces
     |      to a uniform random angle over the range 0 to 2*pi.
     |  
     |
     |  weibullvariate(self, alpha, beta)
     |      Weibull distribution.
     |      
     |      alpha is the scale parameter and beta is the shape parameter.
    """


    #-------------------------------------------------------------------------
    _NORMALIZE: float = 2.328_306_436_538_696_289_062_5e-10  # i.e. 1.0 / (1 << 32)
    """The value of this class attribute MUST BE OVERRIDDEN in  inheriting
    classes  if  returned random integer values are coded on anything else 
    than 32 bits.  It is THE multiplier constant value to  be  applied  to  
    pseudo-random number for them to be normalized in interval [0.0, 1.0).
    """

    _OUT_BITS: int = 32
    """The value of this class attribute MUST BE OVERRIDDEN in inheriting
    classes  if returned random integer values are coded on anything else 
    than 32 bits.
    """


    #-------------------------------------------------------------------------
    def __init__(self, _seed: SeedStateType = None, /) -> None:
        """Constructor.
        
        Should _seed be None or not a number then the local time is used
        (with its shuffled value) as a seed.

        Notice: the Python built-in base class random.Random  internally 
        calls method setstate() which MUST be overridden in classes that 
        inherit from class BaseRandom.
        """
        super().__init__( _seed )


    #-------------------------------------------------------------------------
    def next(self) -> int:
        """This is the core of the pseudo-random generator. It returns the next pseudo random integer value generated by the inheriting generator.

        This is the core of the PRNGs.
        Inheriting classes MUST IMPLEMENT this method.
        """
        raise NotImplementedError()


    #-------------------------------------------------------------------------
    def random(self) -> float:
        """Returns the next pseudo-random floating-point number in interval [0.0, 1.0).
        
        Inheriting classes MUST OVERRIDE the value of the base class constant 
        attribute _NORMALIZE when the random integer values they  return  are 
        coded on anything else than 32 bits.
        """
        return self.next() * self._NORMALIZE
    

    #-------------------------------------------------------------------------
    def binomialvariate(self, n: int = 1, p: float = 0.5) -> int:
        """Binomial distribution. Returns the number of successes for n>=0 independent trials.
        
        The probability of success in each trial is p, 0.0 <= p <= 1.0.
        Built-in method available since Python 3.12, implemented in PyRandLib
        for all  former versions of Python.
        """       
        return sum( self.random() < p for _ in range(n) )


    #-------------------------------------------------------------------------
    def expovariate(self, lambd: float = 1.0) -> float:
        """Exponential distribution.

        Since Python 3.12,  a default value is assigned to the parameter of 
        this bult-in method. So, it is define this way in PyRandLib for all 
        former versions of Python.
        """
        return super().expovariate(lambd)

    #-------------------------------------------------------------------------
    def getrandbits(self, k: int, /) -> int:
        """Returns k bits from the internal state of the generator.

        k must be a positive value greater or equal to  zero.
        """
        assert k >= 0, "the returned bits count must not be negative"
        assert k < self._OUT_BITS, f"the returned bits count must be less than {self._OUT_BITS}"

        return 0 if k == 0 else self.next() >> (self._OUT_BITS - k)
        

    #-------------------------------------------------------------------------
    def randbytes(self, n: int, /) -> bytes:
        """Generates n random bytes.

        This method should not be used for generating security tokens.
        (use Python built-in secrets.token_bytes() instead)
        """
        assert n >= 0  # and self._OUT_BITS >= 8
        return bytes([self.next() >> (self._OUT_BITS - 8) for _ in range(n)])


    #-------------------------------------------------------------------------
    def getstate(self) -> StateType:
        """Returns an object capturing the current internal state of the generator.
        
        This object can then be passed to setstate() to restore the state.
        Inheriting classes MUST IMPLEMENT this method.
        """
        raise NotImplementedError()


    #-------------------------------------------------------------------------
    def setstate(self, _state: StateType, /) -> None:
        """Restores the internal state of the generator.
        
        _state should have been obtained from a previous call to getstate(),
        and  setstate() restores the internal state of the generator to what
        it was at the time setstate() was called.
        Inheriting classes MUST IMPLEMENT this method.
        """
        raise NotImplementedError()


    #-------------------------------------------------------------------------
    def seed(self, _seed: SeedStateType = None, /) -> None:
        """Initiates the internal state of this pseudo-random generator.
        """
        try:
            self.setstate( _seed )
        except:
            super().seed( _seed )


    #-------------------------------------------------------------------------
    def __call__(self, _max : Numerical | tuple[Numerical] | list[Numerical] = 1.0,
                       /,
                       times: int                                            = 1   ) -> Numerical | list[Numerical]:
        """This class's instances are callable.
        
        The returned value is uniformly contained within the 
        interval [0.0 : _max].  When times is set, a list of
        iterated pseudo-random values is  returned.  'times'
        must  be an integer.  If less than 1 it is forced to
        be 1.
        '_max' may be a list or a tuple of values,  in which
        case  a  list  of  related  pseudo-random  values is
        returned with entries of the same type than the same 
        indexed entry in '_max'.
        """
        assert isinstance( times, int )
        if times < 1:
            times =  1
         
        if isinstance( _max, int ):
            ret = [ int(_max * self.random()) for _ in range(times) ]
        elif isinstance( _max, float ):
            ret = [ _max * self.random() for _ in range(times) ]
        else:
            try:
                if times == 1:
                    ret = [ self(m,1) for m in _max ] 
                else:
                    ret = [ [self(m,1) for m in _max] for _ in range(times) ]
            except:
                ret = [ self.__call__(times=1) ]
        
        return ret[0] if len(ret) == 1 else ret
    

    #-------------------------------------------------------------------------
    @classmethod
    def _rotleft(cls, _value: int, _rotCount: int, _bitsCount: int = 64, /) -> int:
        """Returns the value of a left rotating by _rotCount bits

        Useful for some inheriting classes.
        """
        #assert 1 <=_rotCount <= _bitsCount 
        hiMask = ((1 << _bitsCount) - 1) ^ (loMask := (1 << (_bitsCount - _rotCount)) - 1)
        return ((_value & loMask) << _rotCount) | ((_value & hiMask) >> (_bitsCount - _rotCount))


#=====   end of module   baserandom.py   =====================================
