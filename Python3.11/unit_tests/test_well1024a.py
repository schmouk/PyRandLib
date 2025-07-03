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

from PyRandLib.well1024a import Well1024a


#=============================================================================
class TestWell1024a:
    """Tests class Well1024a.
    """
    
    Well1024a_STATE_SIZE = 32

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Well1024a._NORMALIZE == 1.0 / (1 << 32)
        assert Well1024a._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        wll = Well1024a()
        assert wll._STATE_SIZE == TestWell1024a.Well1024a_STATE_SIZE
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 32) for s in wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        wll = Well1024a(1)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xbeeb8da1
        assert wll._state[ 7] == 0x85e7bb0f
        assert wll._state[13] == 0x87b341d6
        assert wll._state[19] == 0xe2631837
        assert wll._state[25] == 0x0c43407d
        assert wll._state[31] == 0x962b1967

        wll = Well1024a(-2)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 5] == 0xd85ab7a2
        assert wll._state[11] == 0xf79e3f6d
        assert wll._state[17] == 0x7b875a0b
        assert wll._state[23] == 0xcfee92df
        assert wll._state[29] == 0xcc6d17e0

        wll = Well1024a(0x0123_4567_89ab_cdef)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 6] == 0xb8fc5b10
        assert wll._state[12] == 0x8eba85b2
        assert wll._state[18] == 0x997f31f8
        assert wll._state[24] == 0x5e4d770f
        assert wll._state[30] == 0x09193ec6

        wll = Well1024a(-8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xe2fbc345
        assert wll._state[ 7] == 0xe6d25024
        assert wll._state[13] == 0xfbe6cd71
        assert wll._state[19] == 0xd8a2a21a
        assert wll._state[25] == 0xea0b583d
        assert wll._state[31] == 0xc20cfd85

        wll = Well1024a(8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 6] == 0x1408795f
        assert wll._state[12] == 0xc6afab58
        assert wll._state[18] == 0xfb8939c5
        assert wll._state[24] == 0x7c374de5
        assert wll._state[30] == 0x4bf0de50

        wll = Well1024a(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 6] == 0x7a5f67e3
        assert wll._state[12] == 0x149cc0b2
        assert wll._state[18] == 0x4f7825c4
        assert wll._state[24] == 0x54551aad
        assert wll._state[30] == 0xd1de816e

    #-------------------------------------------------------------------------
    def test_init_float(self):
        wll = Well1024a(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0x5fee464f
        assert wll._state[ 6] == 0x1c4d126a
        assert wll._state[12] == 0x102227a3
        assert wll._state[18] == 0x239bcb0a
        assert wll._state[24] == 0x7ce1cb9d
        assert wll._state[30] == 0x365bbd9a

        wll = Well1024a(1.0)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 64) for s in wll._state)  # type: ignore

        with pytest.raises(ValueError):
            wll = Well1024a(-0.0001)
        with pytest.raises(ValueError):
            wll = Well1024a(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        wll = Well1024a(tuple(i for i in range(TestWell1024a.Well1024a_STATE_SIZE)))  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll = Well1024a(list(i+10 for i in range(TestWell1024a.Well1024a_STATE_SIZE)))  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == list(i+10 for i in range(TestWell1024a.Well1024a_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            wll = Well1024a((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well1024a((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well1024a([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well1024a([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well1024a(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        wll = Well1024a(0x0123_4567_89ab_cdef)
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll._state[ 6] == 0xb8fc5b10
        assert wll._state[12] == 0x8eba85b2
        assert wll._state[18] == 0x997f31f8
        assert wll._state[24] == 0x5e4d770f
        assert wll._state[30] == 0x09193ec6

        for v in [0xaef20bef, 0x3d574a34, 0x1f36d6d6, 0x227fe92e, 0x680e6922]:
            assert wll.next() == v

        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 27
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 3] == 0xa2d41933
        assert wll._state[ 9] == 0x2680d065
        assert wll._state[15] == 0xd7ebcca1
        assert wll._state[21] == 0x797f89de
        assert wll._state[27] == 0xfddc00f7

    #-------------------------------------------------------------------------
    def test_seed(self):
        wll = Well1024a()
        
        wll.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 6] == 0x7a5f67e3
        assert wll._state[12] == 0x149cc0b2
        assert wll._state[18] == 0x4f7825c4
        assert wll._state[24] == 0x54551aad
        assert wll._state[30] == 0xd1de816e

        wll.seed(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0x5fee464f
        assert wll._state[ 6] == 0x1c4d126a
        assert wll._state[12] == 0x102227a3
        assert wll._state[18] == 0x239bcb0a
        assert wll._state[24] == 0x7ce1cb9d
        assert wll._state[30] == 0x365bbd9a

        with pytest.raises(ValueError):
            wll.seed(-0.0001)
        with pytest.raises(ValueError):
            wll.seed(1.001)

        wll.seed()
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 < s < (1 << 64) for s in wll._state)  # type: ignore

        with pytest.raises(TypeError):
            wll.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            wll.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            wll.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            wll.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            wll.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        wll = Well1024a()

        wll.setstate()
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 < s < (1 << 64) for s in wll._state)  # type: ignore
    
        with pytest.raises(TypeError):
            wll.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            wll.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            wll.setstate("123")  # type: ignore

        wll.setstate((tuple(i+31 for i in range(TestWell1024a.Well1024a_STATE_SIZE)), 3))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+31 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll.setstate([[i+41 for i in range(TestWell1024a.Well1024a_STATE_SIZE)], TestWell1024a.Well1024a_STATE_SIZE + 8])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+41 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll.setstate([tuple(i+51 for i in range(TestWell1024a.Well1024a_STATE_SIZE)), 3])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+51 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll.setstate(([i+61 for i in range(TestWell1024a.Well1024a_STATE_SIZE)], TestWell1024a.Well1024a_STATE_SIZE + 8))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+61 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll.setstate(tuple(i+11 for i in range(TestWell1024a.Well1024a_STATE_SIZE)))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+11 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        wll.setstate([i+21 for i in range(TestWell1024a.Well1024a_STATE_SIZE)])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+21 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            wll.setstate([1, 2])
        with pytest.raises(TypeError):
            wll.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            wll.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            wll.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore
            _state[TestWell1024a.Well1024a_STATE_SIZE - 2] = -1
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore
            _state[TestWell1024a.Well1024a_STATE_SIZE - 3] = 0.321
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell1024a.Well1024a_STATE_SIZE)]  # type: ignore
            _state[TestWell1024a.Well1024a_STATE_SIZE - 5] = {1, 2}
            wll.setstate(_state)  # type: ignore
