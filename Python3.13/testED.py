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
from math import sqrt
from statistics import mean, median, stdev
from PyRandLib import *


#=============================================================================
def test_algo(rnd_algo, nb_entries: int = 1_000, nb_loops: int = 1_000_000):
    """Tests the equi-distribution of every PRNGs as implemented in library PyRandLib.
        
    This module is provided with library PyRandLib.
    
    Copyright (c) 2025 Philippe Schmouker

    The Pseudo-Random Numbers Generators implemented in library PyRandLib have
    been chosen as being the best in class ones about their randomness quality
    - as evaluated with test program  TestU01  (Pierre  L'Ecuyer  and  Richard 
    Simard  (Université  de  Montréal) in 'TestU01:  A C Library for Empirical 
    Testing of Random Number Generators  -  ACM  Transactions  on Mathematical 
    Software, vol.33 n.4, pp.22-40,  August 2007').

    One of the main characteristics of these PRNGs is the equidistribution  of
    the  generated  random numbers.  Validating this equidistribution does not
    ensure the correctness of any  implementation  BUT  the  failure  of  this
    validation ensures a not correct implementation.  This is the sole goal of
    this litle script.

    This script runs an N-times loop on each algprithm. At each loop, it draws
    a pseudo-random number in the interval [0; 1,000) and sets an histogram of
    the drawings (1,000 entries).  It then evaluates statistics  values  mean, 
    median  and standard  eviation for each histogram and,  for each histogram 
    entry, evaluates its variance.  Should mean value be far from N / 1,000 or 
    any  variance  get  a  too large value,  the script outputs on console all 
    faulty values.
    """
    algo_name = rnd_algo.__class__.__name__
    print('-'*(len(algo_name)+1), algo_name, '-'*(len(algo_name)+1), sep='\n')

    hist = [0]*nb_entries

    expected_max_diff_mean_median = (nb_loops / nb_entries) * 0.002    # i.e. difference should be less than 0.2 % of expected mean
    expected_max_stdev = 1.04 * sqrt(nb_loops / nb_entries)            # i.e. +4 % max over expected stdandard deviation
    expected_max_variance = 4.5                                        # this is the absolute value of the expected max on local variance

    if expected_max_diff_mean_median < 0.5:
        expected_max_diff_mean_median= 0.5

    for _ in range(nb_loops):
        n = int(rnd_algo() * nb_entries)
        hist[n] += 1

    # uncomment next line if you want to print the content of the histograms
    #print(hist, '\n')

    print (f"{nb_loops:,d} loops, {nb_entries:,d} entries in histogram, expected mean: {round(nb_loops / nb_entries):,d}")
    mn, md, st = mean(hist), median(hist), stdev(hist)
    print(f"  mean: {mn:,f}, median: {md:,f}, standard deviation: {st:,.3f}")

    err = False

    if (abs(md - mn) > expected_max_diff_mean_median):
        err = True
        print(f"  incoherence btw. mean and median values, difference expected to be less than {expected_max_diff_mean_median:,.1f}")
    if (st > expected_max_stdev):
        err = True
        print(f"  standard deviation is out of range, should be less than {expected_max_stdev:_.3f}")

    min_variance = max_variance = 0.0

    for i in range(nb_entries):
        variance = (hist[i] - mn) / st
        if abs(variance) > expected_max_variance:
            print(f"  entry {i:,d}: hist = {hist[i]:,d}, variance = {variance:,.4f} seems too large")
            err = True
        if variance < min_variance:
            min_variance = variance
        elif variance > max_variance:
            max_variance = variance
            
    print(f"  variances are in range [{min_variance:,.3f} ; {'+' if max_variance > 0.0 else ''}{max_variance:,.3f}]", end='')
    print(f", min: {min(hist)}, max: {max(hist)}")

    if (not err):
        print("  Test OK.")
    print()


#=============================================================================
if __name__ == "__main__":
    test_algo(Cwg64(),         3217, nb_loops = 2_000_000)   # notice: 3217 is a prime number
    test_algo(Cwg128_64(),     3217, nb_loops = 2_000_000)
    test_algo(Cwg128(),        3217, nb_loops = 2_000_000)
    test_algo(FastRand32(),    3217, nb_loops = 2_000_000)
    test_algo(FastRand63(),    3217, nb_loops = 2_000_000)
    test_algo(LFib78(),        3217, nb_loops = 2_000_000)
    test_algo(LFib116(),       3217, nb_loops = 2_000_000)
    test_algo(LFib668(),       3217, nb_loops = 2_000_000)
    test_algo(LFib1340(),      3217, nb_loops = 2_000_000)
    test_algo(Melg607(),       3217, nb_loops = 2_000_000)
    test_algo(Melg19937(),     3217, nb_loops = 2_000_000)
    test_algo(Melg44497(),     3217, nb_loops = 2_000_000)
    test_algo(Mrg287(),        3217, nb_loops = 2_000_000)
    test_algo(Mrg1457(),       3217, nb_loops = 2_000_000)
    test_algo(Mrg49507(),      3217, nb_loops = 2_000_000)
    test_algo(Pcg64_32(),      3217, nb_loops = 2_000_000)
    test_algo(Pcg128_64(),     3217, nb_loops = 2_000_000)
    test_algo(Pcg1024_32(),    3217, nb_loops = 2_000_000)
    test_algo(Squares32(),     3217, nb_loops = 2_000_000)
    test_algo(Squares64(),     3217, nb_loops = 2_000_000)
    test_algo(Well512a(),      3217, nb_loops = 1_500_000)
    test_algo(Well1024a(),     3217, nb_loops = 1_500_000)
    test_algo(Well19937c(),    2029)                         # notice: 2029 is a prime number
    test_algo(Well44497b(),    2029)
    test_algo(Xoroshiro256(),  3217, nb_loops = 2_000_000)
    test_algo(Xoroshiro512(),  3217, nb_loops = 2_000_000)
    test_algo(Xoroshiro1024(), 3217, nb_loops = 2_000_000)
    


#=====   end of module   testED.py   =========================================
