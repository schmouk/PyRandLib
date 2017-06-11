# -*- coding: utf-8 -*-
#=============================================================================
from .baselfib64 import BaseLFib64


#=============================================================================
class LFib668( BaseLFib64 ):
    """
    Pseudo-random numbers generator  -  Definition of a fast 64-bits Lagged  Fibonacci 
    Generator with quite short period (1.2e+201).
    This module is part of library PyRandLib.
    
    Copyright (c) 2017 Philippe Schmouker


    Lagged Fibonacci generators LFib( m, r, k, op) use the recurrence
    
        x(i) = (x(i-r) op (x(i-k)) mod m
    
    where op is an operation that can be:
        + (addition),
        - (substraction),
        * (multiplication),
        ^(bitwise exclusive-or).
    
    With the + or - operation, such generators are in fact MRGs. They offer very large
    periods  with  the  best  known  results in the evaluation of their randomness, as
    stated in the evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de
    Montreal)  in  "TestU01:  A  C  Library  for Empirical Testing  of  Random  Number  
    Generators - ACM Transactions  on  Mathematical  Software,  vol.33 n.4,  pp.22-40, 
    August 2007".  It  is  recommended  to  use  such pseudo-random numbers generators 
    rather than LCG ones for serious simulation applications.

    The implementation of this LFib 64-bits model  is  based  on  a  Lagged  Fibonacci 
    generator (LFIB) that uses the recurrence
    
        x(i) = (x(i-273) + x(i-607)) mod 2^64
    
    and offers a period of about 2^668 - i.e. 1.2e+201 - with low computation time due
    to the use of a 2^64 modulo but memory space consumption (607 long integers).
    
    Please notice that the TestUO1 article states that  the  operator  should  be  '*' 
    while Mascagni & Srinivasan  in their original article stated that the operator is 
    '+'.  We've implemented here the original operator: '+'.
       
    See LFib78,  LFib116 and LFib1340 for long period  LFib  generators  (resp.  2^78,  
    2^116  and  2^1340  periods,  i.e.  resp.  3.0e+23,  8.3e+34 and 2.4e+403 periods) 
    while same computation time and far higher precision (64-bits  calculations)  than  
    MRGs, but memory consumption (resp. 17, 55 and 1279 integers).
    
    Please notice that this class and all its  inheriting  sub-classes  are  callable.
    Example:
    
      rand = LFib668()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)

    Please notice that for simulating the roll of a dice you should program:

      diceRoll = LFib668()
      print(int(diceRoll(1, 7))) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRabndLib class | TU01 generator name      | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ------------------------ | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | LFibRand78       | LFib(2^64, 17, 5, +)     |    34 x 4-bytes | 2^78    |    n.a.     |     1.1      |          0       |       0     |       0        |
 | LFibRand116      | LFib(2^64, 55, 24, +)    |   110 x 4-bytes | 2^116   |    n.a.     |     1.0      |          0       |       0     |       0        |
 | LFibRand668      | LFib(2^64, 607, 273, +)  | 1,214 x 4-bytes | 2^668   |    n.a.     |     0.9      |          0       |       0     |       0        |
 | LFibRand1340     | LFib(2^64, 1279, 861, +) | 2,558 x 4-bytes | 2^1340  |    n.a.     |     0.9      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """

    #=========================================================================
    # 'protected' constant
    _LIST_SIZE = 607 # this 'LFib(2^64, 607, 273, +)' generator is based on a suite containing 607 integers        
            
 
    #=========================================================================
    def random(self):
        """
        This is the core of the pseudo-random generator.
        Returned values are within [0.0, 1.0).
        """
        # evaluates indexes in suite for the i-273 and i-607 -th values
        k273 = self._index-273
        if k273 < 0:
            k273 += LFib668._LIST_SIZE
        
        # then evaluates current value
        myValue = (self._list[k273] + self._list[self._index]) & 18446744073709551615
        self._list[self._index] = myValue
        
        # next index
        self._index = (self._index+1) % LFib668._LIST_SIZE
        
        # then returns float value within [0.0, 1.0)
        return  myValue / 18446744073709551616.0

 
#=====   end of module   lfib668.py   =======================================

