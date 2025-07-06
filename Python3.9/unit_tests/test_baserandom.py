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
from math import log
import pytest

from PyRandLib.baserandom       import BaseRandom
from PyRandLib.annotation_types import StateType


#=============================================================================
class TestBaseRandom:
    """Tests the base class BaseRandom"""
    
    #-------------------------------------------------------------------------
    class BRand0(BaseRandom):
        def next(self) -> int: return 0
        def getstate(self) -> StateType: return 0  # type: ignore

    class BRand1(BaseRandom):
        def next(self) -> int: return 0xffff_ffff
        def getstate(self) -> StateType: return 0xffff_ffff  # type: ignore

    class BRand33(BaseRandom):
        def next(self) -> int: return 0x5555_5555
        def getstate(self) -> StateType: return 0x5555_5555  # type: ignore


    #-------------------------------------------------------------------------
    def test_class(self):
        assert BaseRandom._NORMALIZE == 1.0 / (1 << 32)
        assert BaseRandom._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        b_rnd = BaseRandom()
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        b_rnd = BaseRandom(1)
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_float(self):
        b_rnd = BaseRandom(0.357)
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

        with pytest.raises(ValueError):
            b_rnd = BaseRandom(-0.001)
        with pytest.raises(ValueError):
            b_rnd = BaseRandom(1.001)
    
    #-------------------------------------------------------------------------
    def test_init_else(self):
        with pytest.raises(NotImplementedError):
            b_rnd = BaseRandom((1, 2, 3))  # type: ignore
            assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
            assert b_rnd._OUT_BITS == 32
            assert b_rnd.gauss_next is None  # type: ignore

        with pytest.raises(NotImplementedError):
            b_rnd = BaseRandom("123")  # type: ignore
            assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
            assert b_rnd._OUT_BITS == 32
            assert b_rnd.gauss_next is None  # type: ignore

        with pytest.raises(NotImplementedError):
            b_rnd = BaseRandom(BaseRandom())  # type: ignore
            assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
            assert b_rnd._OUT_BITS == 32
            assert b_rnd.gauss_next is None  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            b_rnd.next()
        
        b_rnd = TestBaseRandom.BRand0()
        assert b_rnd.next() == 0
        
        b_rnd = TestBaseRandom.BRand1()
        assert b_rnd.next() == 0xffff_ffff
        
        b_rnd = TestBaseRandom.BRand33()
        assert b_rnd.next() == 0x5555_5555

    #-------------------------------------------------------------------------
    def test_random(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            b_rnd.random()
        
        b_rnd = TestBaseRandom.BRand0()
        assert b_rnd.random() == 0.0
        
        b_rnd = TestBaseRandom.BRand1()
        assert b_rnd.random() == 0xffff_ffff * b_rnd._NORMALIZE
        
        b_rnd = TestBaseRandom.BRand33()
        assert b_rnd.random() == 0x5555_5555 * b_rnd._NORMALIZE

    #-------------------------------------------------------------------------
    def test_binomialvariate(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            b_rnd.binomialvariate()
                    
        b_rnd = TestBaseRandom.BRand0()
        assert b_rnd.binomialvariate() == 1
        assert b_rnd.binomialvariate(3) == 3
        assert b_rnd.binomialvariate(5, 0.0) == 0
        assert b_rnd.binomialvariate(7, 0.00001) == 7
        assert b_rnd.binomialvariate(11, 1.0) == 11

        b_rnd = TestBaseRandom.BRand1()
        assert b_rnd.binomialvariate() == 0
        assert b_rnd.binomialvariate(3) == 0
        assert b_rnd.binomialvariate(5, 0.0) == 0
        assert b_rnd.binomialvariate(7, 0.00001) == 0
        assert b_rnd.binomialvariate(11, 0.9999) == 0
        assert b_rnd.binomialvariate(11, 1.0) == 11
        
        b_rnd = TestBaseRandom.BRand33()
        assert b_rnd.binomialvariate() == 1
        assert b_rnd.binomialvariate(3) == 3
        assert b_rnd.binomialvariate(5, 0.0) == 0
        assert b_rnd.binomialvariate(7, 0.333) == 0
        assert b_rnd.binomialvariate(7, 0.334) == 7
        assert b_rnd.binomialvariate(11, 1.0) == 11

    #-------------------------------------------------------------------------
    def test_expovariate(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            b_rnd.expovariate()
        with pytest.raises(NotImplementedError):
            b_rnd.expovariate(0.5)

        b_rnd = TestBaseRandom.BRand0()
        assert b_rnd.expovariate() == 0.0  #-log(1.0 - b_rnd.random()) / 1.0
        assert b_rnd.expovariate(0.5) == 0.0  #-log(1.0 - b_rnd.random()) / 0.5
        assert b_rnd.expovariate(2.0) == 0.0  #-log(1.0 - b_rnd.random()) / 2.0

        b_rnd = TestBaseRandom.BRand1()
        assert b_rnd.expovariate() == -log(1.0 - 0xffff_ffff * b_rnd._NORMALIZE) / 1.0
        assert b_rnd.expovariate(0.5) == -log(1.0 - 0xffff_ffff * b_rnd._NORMALIZE) / 0.5
        assert b_rnd.expovariate(2.0) == -log(1.0 - 0xffff_ffff * b_rnd._NORMALIZE) / 2.0

        b_rnd = TestBaseRandom.BRand33()
        assert b_rnd.expovariate() == -log(1.0 - 0x5555_5555 * b_rnd._NORMALIZE) / 1.0
        assert b_rnd.expovariate(0.5) == -log(1.0 - 0x5555_5555 * b_rnd._NORMALIZE) / 0.5
        assert b_rnd.expovariate(2.0) == -log(1.0 - 0x5555_5555 * b_rnd._NORMALIZE) / 2.0

    #-------------------------------------------------------------------------
    def test_getrandbits(self):
        b_rnd = BaseRandom()
        assert b_rnd.getrandbits(0) == 0
        with pytest.raises(AssertionError):
            n = b_rnd.getrandbits(-1)
        with pytest.raises(AssertionError):
            n = b_rnd.getrandbits(b_rnd._OUT_BITS)
        with pytest.raises(AssertionError):
            n = b_rnd.getrandbits(b_rnd._OUT_BITS + 1)
        for k in range(1, b_rnd._OUT_BITS):
            with pytest.raises(NotImplementedError):
                n = b_rnd.getrandbits(k)

        b_rnd = TestBaseRandom.BRand0()
        for k in range(b_rnd._OUT_BITS):
            assert b_rnd.getrandbits(k) == 0

        b_rnd = TestBaseRandom.BRand1()
        for k in range(b_rnd._OUT_BITS):
            assert b_rnd.getrandbits(k) == (1 << k) - 1

        b_rnd = TestBaseRandom.BRand33()
        for k in range(b_rnd._OUT_BITS):
            assert b_rnd.getrandbits(k) == int((0x5555_5555 / 0xffff_ffff) * (1 << k))

    #-------------------------------------------------------------------------
    def test_randbytes(self):
        b_rnd = BaseRandom(1)
        with pytest.raises(AssertionError):
            b_rnd.randbytes(-1)

        b = b_rnd.randbytes(0)
        assert len(b) == 0

        for n in range(1, 5):
            with pytest.raises(NotImplementedError):
                b = b_rnd.randbytes(n)

        b_rnd = TestBaseRandom.BRand0()
        bytes_ = b_rnd.randbytes(5)
        for b in bytes_:
            assert b == 0

        b_rnd = TestBaseRandom.BRand1()
        bytes_ = b_rnd.randbytes(5)
        for b in bytes_:
            assert b == 255
       
        b_rnd = TestBaseRandom.BRand33()
        bytes_ = b_rnd.randbytes(5)
        for b in bytes_:
            assert b == 255 // 3
     
    #-------------------------------------------------------------------------
    def test_getstate(self):
        b_rnd = BaseRandom(1)
        with pytest.raises(NotImplementedError):
            s = b_rnd.getstate()

        b_rnd = TestBaseRandom.BRand0()
        assert b_rnd.getstate() == 0

        b_rnd = TestBaseRandom.BRand1()
        assert b_rnd.getstate() == 0xffff_ffff

        b_rnd = TestBaseRandom.BRand33()
        assert b_rnd.getstate() == 0x5555_5555

    #-------------------------------------------------------------------------
    def test_seed(self):
        b_rnd = BaseRandom()

        b_rnd.seed()
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

        b_rnd.seed(-1)
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

        b_rnd.seed(0xffff_fffe)
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

        b_rnd.seed(0.357)
        assert b_rnd._NORMALIZE == 1.0 / (1 << 32)
        assert b_rnd._OUT_BITS == 32
        assert b_rnd.gauss_next is None  # type: ignore

        with pytest.raises(ValueError):
            b_rnd.seed(-0.002)
        with pytest.raises(ValueError):
            b_rnd.seed(1.002)
        with pytest.raises(TypeError):
            b_rnd.seed((1.002, -0.003))  # type: ignore
        with pytest.raises(TypeError):
            b_rnd.seed("123")  # type: ignore
        with pytest.raises(TypeError):
            b_rnd.seed(b_rnd)  # type: ignore
    
    #-------------------------------------------------------------------------
    def test_setstate(self):
        b_rnd = BaseRandom(1)
        with pytest.raises(NotImplementedError):
            s = b_rnd.setstate()

    #-------------------------------------------------------------------------
    def test_call_empty(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            n = b_rnd()

    #-------------------------------------------------------------------------
    def test_call_times(self):
        b_rnd = BaseRandom()
        with pytest.raises(AssertionError):
            n = b_rnd(times = -1)
        assert b_rnd(times = 0) == []
        with pytest.raises(NotImplementedError):
            n = b_rnd(times = 1)
        with pytest.raises(NotImplementedError):
            n = b_rnd(times = 2)
        with pytest.raises(AssertionError):
            n = b_rnd(times = 0.1)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(times =(4, 5))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(times = b_rnd)  # type: ignore

        b_rnd = TestBaseRandom.BRand0()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0.0
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0.0
        assert b_rnd(times = 2) == [0.0, 0.0]

        b_rnd = TestBaseRandom.BRand1()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 2) == [0xffff_ffff / (1 << 32), 0xffff_ffff / (1 << 32)]

        b_rnd = TestBaseRandom.BRand33()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 2) == [0x5555_5555 / (1 << 32), 0x5555_5555 / (1 << 32)]


    #-------------------------------------------------------------------------
    def test_call_int(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            n = b_rnd(0x0123_4567_89ab_cdef)
        with pytest.raises(AssertionError):
            n = b_rnd(0x0123_4567_89ab_cdef, -1)
        assert b_rnd(0x0123_4567_89ab_cdef, 0) == []
        with pytest.raises(NotImplementedError):
            n = b_rnd(0x0123_4567_89ab_cdef, 1)
        with pytest.raises(NotImplementedError):
            n = b_rnd(0x0123_4567_89ab_cdef, 5)
        with pytest.raises(AssertionError):
            n = b_rnd(5, times = 0.1)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(7, times =(4, 5))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(11, times = b_rnd)  # type: ignore
    
        b_rnd = TestBaseRandom.BRand0(0x0123_4567_89ab_cdef)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0.0
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0.0
        assert b_rnd(times = 2) == [0.0]*2
        assert b_rnd(5) == 0
        with pytest.raises(AssertionError):
            assert b_rnd(5, -2) == 0
        assert b_rnd(5, 3) == [0]*3

        b_rnd = TestBaseRandom.BRand1(0x0123_4567_89ab_cdef)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 2) == [0xffff_ffff / (1 << 32), 0xffff_ffff / (1 << 32)]
        assert b_rnd(5) == 4
        with pytest.raises(AssertionError):
            assert b_rnd(5, -2) == 4
        assert b_rnd(5, 3) == [4]*3

        b_rnd = TestBaseRandom.BRand33(0x0123_4567_89ab_cdef)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 0) == []
        assert b_rnd(times = 1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 2) == [0x5555_5555 / (1 << 32), 0x5555_5555 / (1 << 32)]
        assert b_rnd(55) == 55 // 3
        with pytest.raises(AssertionError):
            assert b_rnd(55, -2) == 55 // 3
        assert b_rnd(55, 3) == [55 // 3]*3

    #-------------------------------------------------------------------------
    def test_call_float(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            n = b_rnd(0.357)
        with pytest.raises(AssertionError):
            n = b_rnd(0.357, -1)
        assert b_rnd(0.357, 0) == []
        with pytest.raises(NotImplementedError):
            n = b_rnd(0.357, 1)
        with pytest.raises(NotImplementedError):
            n = b_rnd(0.357, 5)
        with pytest.raises(AssertionError):
            n = b_rnd(5.0, times = 0.1)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(7.0, times =(4, 5))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd(11.0, times = b_rnd)  # type: ignore
    
        b_rnd = TestBaseRandom.BRand0(0.357)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0.0
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0.0
        assert b_rnd(times = 1) == 0.0
        assert b_rnd(times = 2) == [0.0, 0.0]

        b_rnd = TestBaseRandom.BRand1(0.357)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0xffff_ffff / (1 << 32)
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 2) == [0xffff_ffff / (1 << 32), 0xffff_ffff / (1 << 32)]

        b_rnd = TestBaseRandom.BRand33(0.357)
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0x5555_5555 / (1 << 32)
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 2) == [0x5555_5555 / (1 << 32), 0x5555_5555 / (1 << 32)]

    #-------------------------------------------------------------------------
    def test_call_tuple(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            t = b_rnd((1, 2, 3))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd((1, 2, 3), -1)  # type: ignore
        assert b_rnd((1.0, 2, 3), 0) == []  # type: ignore
        with pytest.raises(NotImplementedError):
            n = b_rnd((1, 2.1, 3), 1)  # type: ignore
        with pytest.raises(NotImplementedError):
            n = b_rnd((1, 2, 3.2), 5)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd((1, 2, 3), times = 0.1)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd((1, 2.3, 3), times =(4, 5))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd((1, 2, 3.4), times = b_rnd)  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd((1, 2, (3, 4)))  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd((1, 2, [5, 6.0]))  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd((1, b_rnd, [5, 6.0]))  # type: ignore
    
        b_rnd = TestBaseRandom.BRand0()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0.0
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0.0
        assert b_rnd(times = 1) == 0.0
        assert b_rnd(times = 2) == [0.0, 0.0]

        b_rnd = TestBaseRandom.BRand1()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0xffff_ffff / (1 << 32)
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 1) == 0xffff_ffff / (1 << 32)
        assert b_rnd(times = 2) == [0xffff_ffff / (1 << 32), 0xffff_ffff / (1 << 32)]

        b_rnd = TestBaseRandom.BRand33()
        with pytest.raises(AssertionError):
            assert b_rnd(times = -1) == 0x5555_5555 / (1 << 32)
        with pytest.raises(AssertionError):
            assert b_rnd(times = 0) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 1) == 0x5555_5555 / (1 << 32)
        assert b_rnd(times = 2) == [0x5555_5555 / (1 << 32), 0x5555_5555 / (1 << 32)]

    #-------------------------------------------------------------------------
    def test_call_list(self):
        b_rnd = BaseRandom()
        with pytest.raises(NotImplementedError):
            t = b_rnd([1, 2, 3])  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd([1, 2, 3], -1)  # type: ignore
        assert b_rnd([1.0, 2, 3], 0) == []  # type: ignore
        with pytest.raises(NotImplementedError):
            n = b_rnd([1, 2.1, 3], 1)  # type: ignore
        with pytest.raises(NotImplementedError):
            n = b_rnd([1, 2, 3.2], 5)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd([1, 2, 3], times = 0.1)  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd([1, 2.3, 3], times =(4, 5))  # type: ignore
        with pytest.raises(AssertionError):
            n = b_rnd([1, 2, 3.4], times = b_rnd)  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd([1, 2, (3, 4)])  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd([1, 2, [5, 6.0]])  # type: ignore
        with pytest.raises(ValueError):
            t = b_rnd([1, b_rnd, [5, 6.0]])  # type: ignore

    #-------------------------------------------------------------------------
    def test_rot_left(self):
        
        for n in range(1, 16):
            assert 1 << n == BaseRandom._rotleft(1, n, 16)
        for n in range(1, 32):
            assert 1 << n == BaseRandom._rotleft(1, n, 32)
        for n in range(1, 64):
            assert 1 << n == BaseRandom._rotleft(1, n, 64)

        v = 0b1000_0010_0100_0001
        assert 0b1000_0010_0100_0001 == BaseRandom._rotleft(v, 0, 16)
        assert 0b0000_0100_1000_0011 == BaseRandom._rotleft(v, 1, 16)
        assert 0b0000_1001_0000_0110 == BaseRandom._rotleft(v, 2, 16)
        assert 0b0001_0010_0000_1100 == BaseRandom._rotleft(v, 3, 16)
        assert 0b0010_0100_0001_1000 == BaseRandom._rotleft(v, 4, 16)
        assert 0b0100_1000_0011_0000 == BaseRandom._rotleft(v, 5, 16)
        assert 0b1001_0000_0110_0000 == BaseRandom._rotleft(v, 6, 16)
        assert 0b0010_0000_1100_0001 == BaseRandom._rotleft(v, 7, 16)
        assert 0b0100_0001_1000_0010 == BaseRandom._rotleft(v, 8, 16)
        assert 0b1000_0011_0000_0100 == BaseRandom._rotleft(v, 9, 16)
        assert 0b0000_0110_0000_1001 == BaseRandom._rotleft(v, 10, 16)
        assert 0b0000_1100_0001_0010 == BaseRandom._rotleft(v, 11, 16)
        assert 0b0001_1000_0010_0100 == BaseRandom._rotleft(v, 12, 16)
        assert 0b0011_0000_0100_1000 == BaseRandom._rotleft(v, 13, 16)
        assert 0b0110_0000_1001_0000 == BaseRandom._rotleft(v, 14, 16)
        assert 0b1100_0001_0010_0000 == BaseRandom._rotleft(v, 15, 16)
        assert 0b1000_0010_0100_0001 == BaseRandom._rotleft(v, 16, 16)

        v = 0b1000_0010_0100_0001_1000_0010_0100_0001;
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 1, 32)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 2, 32)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 3, 32)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 4, 32)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 5, 32)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 6, 32)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 7, 32)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 8, 32)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 9, 32)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 10, 32)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 11, 32)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 12, 32)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 13, 32)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 14, 32)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 15, 32)
        assert 0b1000_0010_0100_0001_1000_0010_0100_0001 == BaseRandom._rotleft(v, 16, 32)
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 17, 32)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 18, 32)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 19, 32)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 20, 32)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 21, 32)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 22, 32)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 23, 32)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 24, 32)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 25, 32)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 26, 32)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 27, 32)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 28, 32)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 29, 32)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 30, 32)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 31, 32)

        v = 0b1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 1)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 2)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 3)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 4)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 5)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 6)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 7)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 8)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 9)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 10)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 11)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 12)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 13)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 14)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 15)
        assert 0b1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001 == BaseRandom._rotleft(v, 16)
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 17)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 18)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 19)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 20)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 21)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 22)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 23)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 24)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 25)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 26)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 27)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 28)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 29)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 30)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 31)
        assert 0b1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001 == BaseRandom._rotleft(v, 32)
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 33)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 34)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 35)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 36)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 37)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 38)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 39)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 40)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 41)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 42)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 43)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 44)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 45)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 46)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 47)
        assert 0b1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001 == BaseRandom._rotleft(v, 48)
        assert 0b0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011 == BaseRandom._rotleft(v, 49)
        assert 0b0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110 == BaseRandom._rotleft(v, 50)
        assert 0b0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100 == BaseRandom._rotleft(v, 51)
        assert 0b0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000 == BaseRandom._rotleft(v, 52)
        assert 0b0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000 == BaseRandom._rotleft(v, 53)
        assert 0b1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000 == BaseRandom._rotleft(v, 54)
        assert 0b0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001 == BaseRandom._rotleft(v, 55)
        assert 0b0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010 == BaseRandom._rotleft(v, 56)
        assert 0b1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100 == BaseRandom._rotleft(v, 57)
        assert 0b0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001 == BaseRandom._rotleft(v, 58)
        assert 0b0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010 == BaseRandom._rotleft(v, 59)
        assert 0b0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100_0001_1000_0010_0100 == BaseRandom._rotleft(v, 60)
        assert 0b0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000_0011_0000_0100_1000 == BaseRandom._rotleft(v, 61)
        assert 0b0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000_0110_0000_1001_0000 == BaseRandom._rotleft(v, 62)
        assert 0b1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000_1100_0001_0010_0000 == BaseRandom._rotleft(v, 63)
