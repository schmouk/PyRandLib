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

from PyRandLib.xoroshiro512 import Xoroshiro512


#=============================================================================
class TestXoroshiro512:
    """Tests class Xoroshiro512.
    """
    
    Xoroshiro512_STATE_SIZE = 8

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Xoroshiro512._NORMALIZE == 1.0 / (1 << 64)
        assert Xoroshiro512._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        xrsr = Xoroshiro512()
        assert xrsr._STATE_SIZE == TestXoroshiro512.Xoroshiro512_STATE_SIZE
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        xrsr = Xoroshiro512(1)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x910a2dec89025cc1
        assert xrsr._state[1] == 0xbeeb8da1658eec67
        assert xrsr._state[2] == 0xf893a2eefb32555e
        assert xrsr._state[3] == 0x71c18690ee42c90b
        assert xrsr._state[4] == 0x71bb54d8d101b5b9
        assert xrsr._state[5] == 0xc34d0bff90150280
        assert xrsr._state[6] == 0xe099ec6cd7363ca5
        assert xrsr._state[7] == 0x85e7bb0f12278575

        xrsr = Xoroshiro512(-2)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf3203e9039f4a821
        assert xrsr._state[1] == 0xba56949915dcf9e9
        assert xrsr._state[2] == 0xd0d5127a96e8d90d
        assert xrsr._state[3] == 0x1ef156bb76650c37
        assert xrsr._state[4] == 0x7842841591543f1d
        assert xrsr._state[5] == 0xd85ab7a2b154095a
        assert xrsr._state[6] == 0xea909a92e113bf3c
        assert xrsr._state[7] == 0x1e2b53fb7bd63f05

        xrsr = Xoroshiro512(0x0123_4567_89ab_cdef)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x157a3807a48faa9d
        assert xrsr._state[1] == 0xd573529b34a1d093
        assert xrsr._state[2] == 0x2f90b72e996dccbe
        assert xrsr._state[3] == 0xa2d419334c4667ec
        assert xrsr._state[4] == 0x01404ce914938008
        assert xrsr._state[5] == 0x14bc574c2a2b4c72
        assert xrsr._state[6] == 0xb8fc5b1060708c05
        assert xrsr._state[7] == 0x8931545f4f9ea651

        xrsr = Xoroshiro512(-8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x48bbc5b84275f3ca
        assert xrsr._state[1] == 0xe2fbc345a799b5aa
        assert xrsr._state[2] == 0x86ce19a135fba0de
        assert xrsr._state[3] == 0x637c87187035ea06
        assert xrsr._state[4] == 0x2a03b9aff2bfd421
        assert xrsr._state[5] == 0x534fe17cac5d7a22
        assert xrsr._state[6] == 0x95d0c8e531644d42
        assert xrsr._state[7] == 0xe6d2502493ff622e

        xrsr = Xoroshiro512(8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xeede014d9a5a6108
        assert xrsr._state[1] == 0xa6eb6466bac9f251
        assert xrsr._state[2] == 0x4246cbb1a64bf70c
        assert xrsr._state[3] == 0xaf6aa8f43ebb8659
        assert xrsr._state[4] == 0xe1b0fb2c7e764cdb
        assert xrsr._state[5] == 0x56d25f68391b2f83
        assert xrsr._state[6] == 0x1408795faf81b73d
        assert xrsr._state[7] == 0xe0c07d9420f2f41e

        xrsr = Xoroshiro512(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[1] == 0xec779c3693f88501
        assert xrsr._state[2] == 0xfed9eeb4936de39d
        assert xrsr._state[3] == 0x6f9fb04b092bd30a
        assert xrsr._state[4] == 0x260ffb0260bbbe5f
        assert xrsr._state[5] == 0x082cfe8866fac366
        assert xrsr._state[6] == 0x7a5f67e38e997e3f
        assert xrsr._state[7] == 0xd7c07017388fa2af

    #-------------------------------------------------------------------------
    def test_init_float(self):
        xrsr = Xoroshiro512(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x5fee464f36fc42c3
        assert xrsr._state[1] == 0x954faf5a9ad49cf8
        assert xrsr._state[2] == 0xa985465a4a5fc644
        assert xrsr._state[3] == 0x77714db9e870d702
        assert xrsr._state[4] == 0xa3aac457d81d552c
        assert xrsr._state[5] == 0xbcf1fb888caf4f02
        assert xrsr._state[6] == 0x1c4d126a40f3f8a9
        assert xrsr._state[7] == 0xe6b536617ee8b60c

        xrsr = Xoroshiro512(1.0)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

        with pytest.raises(ValueError):
            xrsr = Xoroshiro512(-0.0001)
        with pytest.raises(ValueError):
            xrsr = Xoroshiro512(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        xrsr = Xoroshiro512(tuple(i for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)))  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            xrsr = Xoroshiro512(list(i+10 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)))  # type: ignore
            assert xrsr._index == 0
            assert xrsr.gauss_next is None  # type: ignore
            assert xrsr._state == list(i+10 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            xrsr = Xoroshiro512((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro512((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro512([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro512([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro512(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        xrsr = Xoroshiro512(0x0123_4567_89ab_cdef)
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr._state[0] == 0x157a3807a48faa9d
        assert xrsr._state[1] == 0xd573529b34a1d093
        assert xrsr._state[2] == 0x2f90b72e996dccbe
        assert xrsr._state[3] == 0xa2d419334c4667ec
        assert xrsr._state[4] == 0x01404ce914938008
        assert xrsr._state[5] == 0x14bc574c2a2b4c72
        assert xrsr._state[6] == 0xb8fc5b1060708c05
        assert xrsr._state[7] == 0x8931545f4f9ea651

        for v in [0xa2c2a42038d4ec3d, 0x5fc25d0738e7b0f, 0x8cdae320589ff91e, 0x5ef9741cae1d2a1c, 0xb5bfb1afdbeb04dd]:
            assert xrsr.next() == v

        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x2dd1d8834a1d1abe
        assert xrsr._state[1] == 0xfd4348c7c59ed738
        assert xrsr._state[2] == 0xe8c9a4d483fa1ce6
        assert xrsr._state[3] == 0x90f3152a081b547f
        assert xrsr._state[4] == 0xadf094a1bc23213c
        assert xrsr._state[5] == 0x08bb748601635214
        assert xrsr._state[6] == 0xfad74f72516c3bfd
        assert xrsr._state[7] == 0x8f2b04287d66d6e6

    #-------------------------------------------------------------------------
    def test_seed(self):
        xrsr = Xoroshiro512()
        
        xrsr.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[1] == 0xec779c3693f88501
        assert xrsr._state[2] == 0xfed9eeb4936de39d
        assert xrsr._state[3] == 0x6f9fb04b092bd30a
        assert xrsr._state[4] == 0x260ffb0260bbbe5f
        assert xrsr._state[5] == 0x082cfe8866fac366
        assert xrsr._state[6] == 0x7a5f67e38e997e3f
        assert xrsr._state[7] == 0xd7c07017388fa2af

        xrsr.seed(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[0] == 0x5fee464f36fc42c3
        assert xrsr._state[1] == 0x954faf5a9ad49cf8
        assert xrsr._state[2] == 0xa985465a4a5fc644
        assert xrsr._state[3] == 0x77714db9e870d702
        assert xrsr._state[4] == 0xa3aac457d81d552c
        assert xrsr._state[5] == 0xbcf1fb888caf4f02
        assert xrsr._state[6] == 0x1c4d126a40f3f8a9
        assert xrsr._state[7] == 0xe6b536617ee8b60c

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
        xrsr = Xoroshiro512()

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

        xrsr.setstate((tuple(i+31 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)), 3))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+31 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        xrsr.setstate([[i+41 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)], TestXoroshiro512.Xoroshiro512_STATE_SIZE + 8])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+41 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        xrsr.setstate([tuple(i+51 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)), 3])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3 % TestXoroshiro512.Xoroshiro512_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+51 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        xrsr.setstate(([i+61 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)], TestXoroshiro512.Xoroshiro512_STATE_SIZE + 8))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 8 % TestXoroshiro512.Xoroshiro512_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+61 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        xrsr.setstate(tuple(i+11 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+11 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        xrsr.setstate([i+21 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+21 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            xrsr.setstate([1, 2])
        with pytest.raises(TypeError):
            xrsr.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            xrsr.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            xrsr.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro512.Xoroshiro512_STATE_SIZE - 2] = -1
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro512.Xoroshiro512_STATE_SIZE - 3] = 0.321
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro512.Xoroshiro512_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro512.Xoroshiro512_STATE_SIZE - 5] = {1, 2}
            xrsr.setstate(_state)  # type: ignore
