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
import sys
from time import perf_counter_ns
from timeit import repeat

from PyRandLib import *


#=============================================================================
def test_perf(prng_class_name: str, seed_value: int, n_loops: int, n_repeats: int):
    """Evaluates the CPU time spent evaluating a number in [0.0, 1.0)."""
    print("---", prng_class_name, "---")
    perfs = repeat("rnd.next()",
                   setup=f"from PyRandLib import {prng_class_name}; rnd = {prng_class_name}({seed_value})",
                   repeat=n_repeats,
                   timer=perf_counter_ns,
                   number=n_loops)
    print([1e-9 * p / n_loops for p in perfs])
    print(f"--> {min(perfs) / n_loops * 1e-3:.4f} us\n")


#=============================================================================
if __name__ == "__main__":

    print("=== PyRandLib CPU time performances ===")
    print("Python version:", sys.version, '\n')

    N = 15

    test_perf("FastRand32"  , 0x3ca5_8796          , 2_000_000, N)
    test_perf("FastRand63"  , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("LFib78"      , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("LFib116"     , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("LFib668"     , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("LFib1340"    , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("MRGRand287"  , 0x3ca5_8796          , 2_000_000, N)
    test_perf("MRGRand1457" , 0x3ca5_8796          , 2_000_000, N)
    test_perf("MRGRand49507", 0x3ca5_8796          , 2_000_000, N)
    test_perf("Pcg64_32"    , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("Pcg128_64"   , 0x3ca5_8796_1f2e_b45a_3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("Pcg1024_32"  , 0x3ca5_8796_1f2e_b45a, 2_000_000, N)
    test_perf("Well512a"    , 0x3ca5_8796          , 1_000_000, N)
    test_perf("Well1024a"   , 0x3ca5_8796          , 1_000_000, N)
    test_perf("Well19937c"  , 0x3ca5_8796          , 1_000_000, N)
    test_perf("Well44497b"  , 0x3ca5_8796          , 1_000_000, N)


#=====   end of module   testCPUPerfs.py   ===================================
