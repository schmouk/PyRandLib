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

from PyRandLib.xoroshiro1024 import Xoroshiro1024


#=============================================================================
class TestXoroshiro1024:
    """Tests class Xoroshiro1024.
    """
    
    Xoroshiro1024_STATE_SIZE = 16

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Xoroshiro1024._NORMALIZE == 1.0 / (1 << 64)
        assert Xoroshiro1024._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        xrsr = Xoroshiro1024()
        assert xrsr._STATE_SIZE == TestXoroshiro1024.Xoroshiro1024_STATE_SIZE
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        xrsr = Xoroshiro1024(1)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 1] == 0xbeeb8da1658eec67
        assert xrsr._state[ 4] == 0x71bb54d8d101b5b9
        assert xrsr._state[ 7] == 0x85e7bb0f12278575
        assert xrsr._state[10] == 0x6775dc7701564f61
        assert xrsr._state[13] == 0x87b341d690d7a28a

        xrsr = Xoroshiro1024(-2)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 1] == 0xba56949915dcf9e9
        assert xrsr._state[ 4] == 0x7842841591543f1d
        assert xrsr._state[ 7] == 0x1e2b53fb7bd63f05
        assert xrsr._state[10] == 0x2b724bbbfb591868
        assert xrsr._state[13] == 0x8457d34b5125f667

        xrsr = Xoroshiro1024(0x0123_4567_89ab_cdef)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 0] == 0x157a3807a48faa9d
        assert xrsr._state[ 3] == 0xa2d419334c4667ec
        assert xrsr._state[ 6] == 0xb8fc5b1060708c05
        assert xrsr._state[ 9] == 0x2680d065cb73ece7
        assert xrsr._state[12] == 0x8eba85b28df77747
        assert xrsr._state[15] == 0xd7ebcca19d49c3f5

        xrsr = Xoroshiro1024(-8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 1] == 0xe2fbc345a799b5aa
        assert xrsr._state[ 4] == 0x2a03b9aff2bfd421
        assert xrsr._state[ 7] == 0xe6d2502493ff622e
        assert xrsr._state[10] == 0x4592e2e878ff1b75
        assert xrsr._state[13] == 0xfbe6cd715ff52a4a

        xrsr = Xoroshiro1024(8_870_000_000_000_000_000)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 2] == 0x4246cbb1a64bf70c
        assert xrsr._state[ 5] == 0x56d25f68391b2f83
        assert xrsr._state[ 8] == 0x13d184a1443e3dbe
        assert xrsr._state[11] == 0xff42f03c6e8cba89
        assert xrsr._state[14] == 0x74d601c8c6c14f90

        xrsr = Xoroshiro1024(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[ 3] == 0x6f9fb04b092bd30a
        assert xrsr._state[ 6] == 0x7a5f67e38e997e3f
        assert xrsr._state[ 9] == 0x56a7458a6eece57b
        assert xrsr._state[12] == 0x149cc0b2e9f5efed
        assert xrsr._state[15] == 0x4a78cd4fccb7e9f8

    #-------------------------------------------------------------------------
    def test_init_float(self):
        xrsr = Xoroshiro1024(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 0] == 0x5fee464f36fc42c3
        assert xrsr._state[ 3] == 0x77714db9e870d702
        assert xrsr._state[ 6] == 0x1c4d126a40f3f8a9
        assert xrsr._state[ 9] == 0xe8f9525bf6c56aef
        assert xrsr._state[12] == 0x102227a35cb75364
        assert xrsr._state[15] == 0xd619e21c3a243eb0

        xrsr = Xoroshiro1024(1.0)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in xrsr._state)
        assert all(0 <= s < (1 << 64) for s in xrsr._state)  # type: ignore

        with pytest.raises(ValueError):
            xrsr = Xoroshiro1024(-0.0001)
        with pytest.raises(ValueError):
            xrsr = Xoroshiro1024(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        xrsr = Xoroshiro1024(tuple(i for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)))  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.9
            xrsr = Xoroshiro1024(list(i+10 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)))  # type: ignore
            assert xrsr._index == 0
            assert xrsr.gauss_next is None  # type: ignore
            assert xrsr._state == list(i+10 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            xrsr = Xoroshiro1024((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro1024((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro1024([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro1024([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            xrsr = Xoroshiro1024(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        xrsr = Xoroshiro1024(0x0123_4567_89ab_cdef)
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr._state[ 0] == 0x157a3807a48faa9d
        assert xrsr._state[ 3] == 0xa2d419334c4667ec
        assert xrsr._state[ 6] == 0xb8fc5b1060708c05
        assert xrsr._state[ 9] == 0x2680d065cb73ece7
        assert xrsr._state[12] == 0x8eba85b28df77747
        assert xrsr._state[15] == 0xd7ebcca19d49c3f5

        for v in [0xa2c2a42038d4ec3d, 0x3819987c267eb726, 0xa437023430223ecf, 0x26c27c4ef6c0b41b, 0x8dac31b4ce3806cb]:
            assert xrsr.next() == v

        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 5
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 1] == 0x648a17705da44419
        assert xrsr._state[ 4] == 0x1fd7e2f11d1d3f70
        assert xrsr._state[ 7] == 0x8931545f4f9ea651
        assert xrsr._state[10] == 0xcdb8c9cd9a62da0f
        assert xrsr._state[13] == 0x97f6c69811cfb13b

    #-------------------------------------------------------------------------
    def test_seed(self):
        xrsr = Xoroshiro1024()
        
        xrsr.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 0] == 0xf75f04cbb5a1a1dd
        assert xrsr._state[ 3] == 0x6f9fb04b092bd30a
        assert xrsr._state[ 6] == 0x7a5f67e38e997e3f
        assert xrsr._state[ 9] == 0x56a7458a6eece57b
        assert xrsr._state[12] == 0x149cc0b2e9f5efed
        assert xrsr._state[15] == 0x4a78cd4fccb7e9f8

        xrsr.seed(0.357)
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state[ 0] == 0x5fee464f36fc42c3
        assert xrsr._state[ 3] == 0x77714db9e870d702
        assert xrsr._state[ 6] == 0x1c4d126a40f3f8a9
        assert xrsr._state[ 9] == 0xe8f9525bf6c56aef
        assert xrsr._state[12] == 0x102227a35cb75364
        assert xrsr._state[15] == 0xd619e21c3a243eb0

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
        xrsr = Xoroshiro1024()

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

        xrsr.setstate((tuple(i+31 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)), 3))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+31 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        xrsr.setstate([[i+41 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)], TestXoroshiro1024.Xoroshiro1024_STATE_SIZE + 8])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == (TestXoroshiro1024.Xoroshiro1024_STATE_SIZE + 8) % TestXoroshiro1024.Xoroshiro1024_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+41 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        xrsr.setstate([tuple(i+51 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)), 3])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 3 % TestXoroshiro1024.Xoroshiro1024_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+51 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        xrsr.setstate(([i+61 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)], TestXoroshiro1024.Xoroshiro1024_STATE_SIZE + 8))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == (TestXoroshiro1024.Xoroshiro1024_STATE_SIZE + 8) % TestXoroshiro1024.Xoroshiro1024_STATE_SIZE
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+61 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        xrsr.setstate(tuple(i+11 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)))  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+11 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

        xrsr.setstate([i+21 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)])  # type: ignore
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._index == 0
        assert xrsr.gauss_next is None  # type: ignore
        assert xrsr._state == [i+21 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro1024.Xoroshiro1024_STATE_SIZE - 2] = -1
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro1024.Xoroshiro1024_STATE_SIZE - 3] = 0.321
            xrsr.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestXoroshiro1024.Xoroshiro1024_STATE_SIZE)]  # type: ignore
            _state[TestXoroshiro1024.Xoroshiro1024_STATE_SIZE - 5] = {1, 2}
            xrsr.setstate(_state)  # type: ignore
