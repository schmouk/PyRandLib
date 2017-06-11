# -*- coding: utf-8 -*-
#=============================================================================
from .basemrg import BaseMRG


#=============================================================================
class MRGRand287( BaseMRG ):
    """
    Pseudo-random numbers generator  - Definition of a fast 32-bits Multiple Recursive
    Generator with a long period (2.49e+86).
    This module is part of library PyRandLib.
    
    Copyright (c) 2017 Philippe Schmouker


    Multiple Recursive Generators (MRGs)  use  recurrence  to  evaluate  pseudo-random
    numbers suites. Recurrence is of the form:
    
       x(i) = A * SUM[ x(i-k) ]  mod M
    
    for 2 to more k different values.

    MRGs offer very large periods with the best known results  in  the  evaluation  of 
    their  randomness,  as  stated  in  the  evaluation  done  by  Pierre L'Ecuyer and 
    Richard Simard (Universite de Montreal)  in "TestU01:  A C Library  for  Empirical 
    Testing of Random  Number Generators  - ACM Transactions on Mathematical Software, 
    vol.33 n.4, pp.22-40, August 2007".  It is recommended to use  such  pseudo-random
    numbers generators rather than LCG ones for serious simulation applications.

    The implementation of this MRG 32-bits  model  is  based  on  a  Lagged  Fibonacci 
    generator (LFIB), the Marsa-LFIB4 one.
    Lagged Fibonacci generators LFib( m, r, k, op) use the recurrence
    
        x(i) = (x(i-r) op (x(i-k)) mod m
    
    where op is an operation that can be
        + (addition),
        - (substraction),
        * (multiplication),
        ^(bitwise exclusive-or).
    
    With the + or - operation, such generators are in fact MRGs. They offer very large
    periods  with  the  best  known  results in the evaluation of their randomness, as
    stated in the evaluation done by Pierre L'Ecuyer and Richard Simard (Universite de
    Montreal) paper.
    
    The Marsa-LIBF4 version uses the recurrence
    
        x(i) = (x(i-55) + x(i-119) + x(i-179) + x(i-256)) mod 2^32
    
    and offers a period of about 2^287 - i.e. 2.49e+86 - with low computation time due
    to the use of a 2^32 modulo.
    
    See MRGRand1457 for a  longer  period  MR-Generator  (2^1457,  i.e. 4.0e+438)  and 
    longer  computation  time  (2^31-1  modulus  calculations)  but  less memory space 
    consumption (47 integers).
    See MRGRand49507 for a far  longer  period  (2^49507,  i.e. 1.2e+14903)  with  low 
    computation  time  too  (31-bits  modulus)  but  use  of  more  memory space (1597 
    integers).
      
    Furthermore this class is callable:
      rand = MRGRand287()
      print( rand() )    # prints a uniform pseudo-random value within [0.0, 1.0)
      print( rand(a) )   # prints a uniform pseudo-random value within [0.0, a)
      print( rand(a,b) ) # prints a uniform pseudo-random value within [a  , b)

    Please notice that for simulating the roll of a dice you should program:
      diceRoll = MRGRand287()
      print( int(diceRoll(1, 7)) ) # prints a uniform roll within set {1, 2, 3, 4, 5, 6}

    Such a programming is an accelerated while still robust emulation of  the 
    inherited methods:
      - random.Random.randint(self,1,6) and 
      - random.Random.randrange(self,1,7,1)

    Reminder:
    We give you here below a copy of the table of tests for the LCGs that have 
    been implemented in PyRandLib, as provided in paper "TestU01, ..."  -  see
    file README.md.

 | PyRabndLib class | TU01 generator name | Memory Usage    | Period  | time-32bits | time-64 bits | SmallCrush fails | Crush fails | BigCrush fails |
 | ---------------- | ------------------- | --------------- | ------- | ----------- | ------------ | ---------------- | ----------- | -------------- |
 | MRGRand287       | Marsa-LFIB4         |   256 x 4-bytes | 2^287   |    3.40     |     0.8      |          0       |       0     |       0        |
 | MRGRand1457      | DX-47-3             |    47 x 4-bytes | 2^1457  |    n.a.     |     1.4      |          0       |       0     |       0        |
 | MRGRand49507     | DX-1597-2-7         | 1,597 x 4-bytes | 2^49507 |    n.a.     |     1.4      |          0       |       0     |       0        |

    * _small crush_ is a small set of simple tests that quickly tests some  of
    the expected characteristics for a pretty good PRG;
    * _crush_ is a bigger set of tests that test more deeply  expected  random 
    characteristics;
    * _big crush_ is the ultimate set of difficult tests  that  any  GOOD  PRG 
    should definitively pass.
    """
    
    #=========================================================================
    # 'protected' constant
    _LIST_SIZE = 256        # this 'Marsa-LFIB4' MRG is based on a suite containing 256 integers
    _MODULO    = 4294967295 # i.e. 0x7fffffff, or (1<<31)-1, the modulo for DX-47-3 MRG
            
 
    #=========================================================================
    def random(self):
        """
        This is the core of the pseudo-random generator.
        Returned values are within [0.0, 1.0).
        """
        #The Marsa-LIBF4 version uses the recurrence
        #    x(i) = (x(i-55) + x(i-119) + x(i-179) + x(i-256)) mod 2^32

        # evaluates indexes in suite for the i-55, i-119, i-179 (and i-256) -th values
        k55 = self._index-55
        if k55 < 0:
            k55 += MRGRand287._LIST_SIZE
        
        k119 = self._index-119
        if k119 < 0:
            k119 += MRGRand287._LIST_SIZE
        
        k179 = self._index-179
        if k179 < 0:
            k179 += MRGRand287._LIST_SIZE
        
        # then evaluates current value
        myValue = (self._list[k55] + self._list[k119] + self._list[k179] + self._list[self._index]) % 4294967295
        self._list[self._index] = myValue
        
        # next index
        self._index = (self._index+1) % self._LIST_SIZE
        
        # then returns float value within [0.0, 1.0)
        return  myValue / 4294967295.0
 
#=====   end of module   mrgrand287.py   ==================================
