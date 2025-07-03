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
import platform
import pytest

from PyRandLib.well512a import Well512a


#=============================================================================
class TestWell512a:
    """Tests class Well512a.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')
    Well512a_STATE_SIZE = 16

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Well512a._NORMALIZE == 1.0 / (1 << 32)
        assert Well512a._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        wll = Well512a()
        assert wll._STATE_SIZE == TestWell512a.Well512a_STATE_SIZE
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 32) for s in wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        wll = Well512a(1)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xbeeb8da1
        assert wll._state[ 4] == 0x71bb54d8
        assert wll._state[ 7] == 0x85e7bb0f
        assert wll._state[10] == 0x6775dc77
        assert wll._state[13] == 0x87b341d6

        wll = Well512a(-2)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0xf3203e90
        assert wll._state[ 3] == 0x1ef156bb
        assert wll._state[ 6] == 0xea909a92
        assert wll._state[ 9] == 0x19fbbd62
        assert wll._state[12] == 0x8e1f0e39
        assert wll._state[15] == 0x52ef36bb

        wll = Well512a(0x0123_4567_89ab_cdef)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xd573529b
        assert wll._state[ 4] == 0x01404ce9
        assert wll._state[ 7] == 0x8931545f
        assert wll._state[10] == 0xcdb8c9cd
        assert wll._state[13] == 0x97f6c698

        wll = Well512a(-8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0x48bbc5b8
        assert wll._state[ 3] == 0x637c8718
        assert wll._state[ 6] == 0x95d0c8e5
        assert wll._state[ 9] == 0x5f29354e
        assert wll._state[12] == 0xba17e257
        assert wll._state[15] == 0xfeb66399

        wll = Well512a(8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0xeede014d
        assert wll._state[ 3] == 0xaf6aa8f4
        assert wll._state[ 6] == 0x1408795f
        assert wll._state[ 9] == 0x04443a10
        assert wll._state[12] == 0xc6afab58
        assert wll._state[15] == 0x4a80a9e7

        wll = Well512a(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xec779c36
        assert wll._state[ 4] == 0x260ffb02
        assert wll._state[ 7] == 0xd7c07017
        assert wll._state[10] == 0x71da8c61
        assert wll._state[13] == 0x69f17ee1

    #-------------------------------------------------------------------------
    def test_init_float(self):
        wll = Well512a(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0x5fee464f
        assert wll._state[ 3] == 0x77714db9
        assert wll._state[ 6] == 0x1c4d126a
        assert wll._state[ 9] == 0xe8f9525b
        assert wll._state[12] == 0x102227a3
        assert wll._state[15] == 0xd619e21c

        wll = Well512a(1.0)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 64) for s in wll._state)  # type: ignore

        with pytest.raises(ValueError):
            wll = Well512a(-0.0001)
        with pytest.raises(ValueError):
            wll = Well512a(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        wll = Well512a(tuple(i for i in range(TestWell512a.Well512a_STATE_SIZE)))  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                wll = Well512a(list(i+10 for i in range(TestWell512a.Well512a_STATE_SIZE)))  # type: ignore
        else:
            wll = Well512a(list(i+10 for i in range(TestWell512a.Well512a_STATE_SIZE)))  # type: ignore
            assert wll._index == 0
            assert wll.gauss_next is None  # type: ignore
            assert wll._state == list(i+10 for i in range(TestWell512a.Well512a_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            wll = Well512a((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well512a((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well512a([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well512a([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well512a(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        wll = Well512a(0x0123_4567_89ab_cdef)
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll._state[ 1] == 0xd573529b
        assert wll._state[ 4] == 0x01404ce9
        assert wll._state[ 7] == 0x8931545f
        assert wll._state[10] == 0xcdb8c9cd
        assert wll._state[13] == 0x97f6c698

        for v in [0xff43fee0, 0xab5a9c3d, 0x7fa6da51, 0xd6c5abfb, 0x79f26a62]:
            assert wll.next() == v

        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 11
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 2] == 0x2f90b72e
        assert wll._state[ 5] == 0x14bc574c
        assert wll._state[ 8] == 0xf984db4e
        assert wll._state[11] == 0x07bd2fcf
        assert wll._state[14] == 0x7fa6da51

    #-------------------------------------------------------------------------
    def test_seed(self):
        wll = Well512a()
        
        wll.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 1] == 0xec779c36
        assert wll._state[ 4] == 0x260ffb02
        assert wll._state[ 7] == 0xd7c07017
        assert wll._state[10] == 0x71da8c61
        assert wll._state[13] == 0x69f17ee1

        wll.seed(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 0] == 0x5fee464f
        assert wll._state[ 3] == 0x77714db9
        assert wll._state[ 6] == 0x1c4d126a
        assert wll._state[ 9] == 0xe8f9525b
        assert wll._state[12] == 0x102227a3
        assert wll._state[15] == 0xd619e21c

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
        wll = Well512a()

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

        wll.setstate((tuple(i+31 for i in range(TestWell512a.Well512a_STATE_SIZE)), 3))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+31 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        wll.setstate([[i+41 for i in range(TestWell512a.Well512a_STATE_SIZE)], TestWell512a.Well512a_STATE_SIZE + 8])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+41 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        wll.setstate([tuple(i+51 for i in range(TestWell512a.Well512a_STATE_SIZE)), 3])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+51 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        wll.setstate(([i+61 for i in range(TestWell512a.Well512a_STATE_SIZE)], TestWell512a.Well512a_STATE_SIZE + 8))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+61 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        wll.setstate(tuple(i+11 for i in range(TestWell512a.Well512a_STATE_SIZE)))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+11 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

        wll.setstate([i+21 for i in range(TestWell512a.Well512a_STATE_SIZE)])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+21 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore
            _state[TestWell512a.Well512a_STATE_SIZE - 2] = -1
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore
            _state[TestWell512a.Well512a_STATE_SIZE - 3] = 0.321
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell512a.Well512a_STATE_SIZE)]  # type: ignore
            _state[TestWell512a.Well512a_STATE_SIZE - 5] = {1, 2}
            wll.setstate(_state)  # type: ignore
