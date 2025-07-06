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
from typing import Any
import pytest

from PyRandLib.xoroshiro256 import Xoroshiro256


#=============================================================================
class TestXoroshiro256:
    """Tests class Xoroshiro256.
    """
    
    Xoroshiro256_STATE_SIZE = 4

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Xoroshiro256._NORMALIZE == 1.0 / (1 << 64)
        assert Xoroshiro256._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        xrsr = Xoroshiro256()
        assert xrsr._STATE_SIZE == TestXoroshiro256.Xoroshiro256_STATE_SIZE
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        xrsr = Xoroshiro256(1)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x910a2dec89025cc1
        assert xrsr._state[1] == 0xbeeb8da1658eec67
        assert xrsr._state[2] == 0xf893a2eefb32555e
        assert xrsr._state[3] == 0x71c18690ee42c90b

        xrsr = Xoroshiro256(-2)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf3203e9039f4a821
        assert xrsr._state[1] == 0xba56949915dcf9e9
        assert xrsr._state[2] == 0xd0d5127a96e8d90d
        assert xrsr._state[3] == 0x1ef156bb76650c37

        xrsr = Xoroshiro256(0x0123_4567_89ab_cdef)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x157a3807a48faa9d
        assert xrsr._state[1] == 0xd573529b34a1d093
        assert xrsr._state[2] == 0x2f90b72e996dccbe
        assert xrsr._state[3] == 0xa2d419334c4667ec

        xrsr = Xoroshiro256(-8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x48bbc5b84275f3ca
        assert xrsr._state[1] == 0xe2fbc345a799b5aa
        assert xrsr._state[2] == 0x86ce19a135fba0de
        assert xrsr._state[3] == 0x637c87187035ea06

        xrsr = Xoroshiro256(8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xeede014d9a5a6108
        assert xrsr._state[1] == 0xa6eb6466bac9f251
        assert xrsr._state[2] == 0x4246cbb1a64bf70c
        assert xrsr._state[3] == 0xaf6aa8f43ebb8659

        xrsr = Xoroshiro256(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[1] == 0xec779c3693f88501
        assert xrsr._state[2] == 0xfed9eeb4936de39d
        assert xrsr._state[3] == 0x6f9fb04b092bd30a

    #-------------------------------------------------------------------------
    def test_init_float(self):
        xrsr = Xoroshiro256(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x5fee464f36fc42c3
        assert xrsr._state[1] == 0x954faf5a9ad49cf8
        assert xrsr._state[2] == 0xa985465a4a5fc644
        assert xrsr._state[3] == 0x77714db9e870d702

        xrsr = Xoroshiro256(1.0)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

        with pytest.raises(ValueError):
            xrsr = Xoroshiro256(-0.0001)
        with pytest.raises(ValueError):
            xrsr = Xoroshiro256(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        xrsr = Xoroshiro256(tuple(i for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)))  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            xrsr = Xoroshiro256(list(i+10 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)))  # type: ignore
            assert xrsr._index == 0
            assert xrsr.gauss_next is None  # type: ignore
            assert xrsr._state == list(i+10 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            xrsr = Xoroshiro256((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro256((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro256([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro256([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro256(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        xrsr = Xoroshiro256(0x0123_4567_89ab_cdef)
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr._state[0] == 0x157a3807a48faa9d
        assert xrsr._state[1] == 0xd573529b34a1d093
        assert xrsr._state[2] == 0x2f90b72e996dccbe
        assert xrsr._state[3] == 0xa2d419334c4667ec

        for v in [0xa2c2a42038d4ec3d, 0x5fc25d0738e7b0f, 0x625e7bff938e701e, 0x1ba4ddc6fe2b5726, 0xdf0a2482ac9254cf]:
            assert xrsr.next() == v

        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x8b6f756e3cf6d25d
        assert xrsr._state[1] == 0x4390c3ff2f4e84c9
        assert xrsr._state[2] == 0xdfd0524fbf0afc81
        assert xrsr._state[3] == 0x288d5f023136edc7

    #-------------------------------------------------------------------------
    def test_seed(self):
        xrsr = Xoroshiro256()
        
        xrsr.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[1] == 0xec779c3693f88501
        assert xrsr._state[2] == 0xfed9eeb4936de39d
        assert xrsr._state[3] == 0x6f9fb04b092bd30a

        xrsr.seed(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x5fee464f36fc42c3
        assert xrsr._state[1] == 0x954faf5a9ad49cf8
        assert xrsr._state[2] == 0xa985465a4a5fc644
        assert xrsr._state[3] == 0x77714db9e870d702

        with pytest.raises(ValueError):
            xrsr.seed(-0.0001)
        with pytest.raises(ValueError):
            xrsr.seed(1.001)

        xrsr.seed()
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 < s < (1 << 64) for s in xrsr._state)  # type: ignore

        with pytest.raises(TypeError):
            xrsr.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            xrsr.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            xrsr.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            xrsr.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            xrsr.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        xrsr = Xoroshiro256()

        xrsr.setstate()
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 < s < (1 << 64) for s in xrsr._state)  # type: ignore
    
        with pytest.raises(TypeError):
            xrsr.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            xrsr.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            xrsr.setstate("123")  # type: ignore

        xrsr.setstate((tuple(i+31 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)), 3))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+31 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        xrsr.setstate([[i+41 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)], TestXoroshiro256.Xoroshiro256_STATE_SIZE + 8])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+41 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        xrsr.setstate([tuple(i+51 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)), 3])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3 % TestXoroshiro256.Xoroshiro256_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+51 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        xrsr.setstate(([i+61 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)], TestXoroshiro256.Xoroshiro256_STATE_SIZE + 8))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 8 % TestXoroshiro256.Xoroshiro256_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+61 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        xrsr.setstate(tuple(i+11 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+11 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        xrsr.setstate([i+21 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+21 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            xrsr.setstate([1, 2])
        with pytest.raises(TypeError):
            xrsr.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(ValueError):
            xrsr.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(ValueError):
            xrsr.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro256.Xoroshiro256_STATE_SIZE - 2] = -1
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro256.Xoroshiro256_STATE_SIZE - 3] = 0.321
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro256.Xoroshiro256_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro256.Xoroshiro256_STATE_SIZE - 5] = {1, 2}
            xrsr.setstate(_state)  # type: ignore
