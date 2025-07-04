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

from PyRandLib.well44497b import Well44497b


#=============================================================================
class TestWell44497b:
    """Tests class Well44497b.
    """
    
    Well44497b_STATE_SIZE = 1391

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Well44497b._NORMALIZE == 1.0 / (1 << 32)
        assert Well44497b._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        wll = Well44497b()
        assert wll._STATE_SIZE == TestWell44497b.Well44497b_STATE_SIZE
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 32) for s in wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        wll = Well44497b(1)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[   1] == 0xbeeb8da1
        assert wll._state[ 232] == 0xa13e727a
        assert wll._state[ 463] == 0xc7fd0b60
        assert wll._state[ 694] == 0x43bf1ac4
        assert wll._state[ 925] == 0xb269cad1
        assert wll._state[1156] == 0xaac932c2
        assert wll._state[1387] == 0x46f1f73f

        wll = Well44497b(-2)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 233] == 0xe09472b5
        assert wll._state[ 464] == 0x46038a1e
        assert wll._state[ 695] == 0x79a6b61c
        assert wll._state[ 926] == 0xe0bcd931
        assert wll._state[1157] == 0x995061d0
        assert wll._state[1388] == 0x9e846e17

        wll = Well44497b(0x0123_4567_89ab_cdef)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 125] == 0x9c889382
        assert wll._state[ 356] == 0x253a378b
        assert wll._state[ 587] == 0x690c72ab
        assert wll._state[ 818] == 0x78f5d84f
        assert wll._state[1049] == 0x8375eb49
        assert wll._state[1280] == 0x92e2ba8b

        wll = Well44497b(-8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[  50] == 0x1d0bb5d2
        assert wll._state[ 281] == 0x073462d5
        assert wll._state[ 512] == 0xa500600f
        assert wll._state[ 743] == 0x0c57749a
        assert wll._state[ 974] == 0xa039f6de
        assert wll._state[1205] == 0xb2f5bbaa

        wll = Well44497b(8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 185] == 0x57dfb91b
        assert wll._state[ 416] == 0x8bc453b4
        assert wll._state[ 647] == 0x59c0a78e
        assert wll._state[ 878] == 0x361926a3
        assert wll._state[1109] == 0xbb2b9865
        assert wll._state[1340] == 0x150e567c

        wll = Well44497b(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 127] == 0x33f37c98
        assert wll._state[ 358] == 0xd9760a2a
        assert wll._state[ 589] == 0x2774c2e3
        assert wll._state[ 820] == 0x3827beea
        assert wll._state[1051] == 0xb9dcad84
        assert wll._state[1282] == 0x986d6ae2

    #-------------------------------------------------------------------------
    def test_init_float(self):
        wll = Well44497b(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[   0] == 0x5fee464f
        assert wll._state[ 231] == 0xa1c9c800
        assert wll._state[ 462] == 0x9b8c5c6f
        assert wll._state[ 693] == 0xf6d7870f
        assert wll._state[ 924] == 0xb5682bb8
        assert wll._state[1155] == 0xeae78622
        assert wll._state[1386] == 0xb47820d7

        wll = Well44497b(1.0)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 64) for s in wll._state)  # type: ignore

        with pytest.raises(ValueError):
            wll = Well44497b(-0.0001)
        with pytest.raises(ValueError):
            wll = Well44497b(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        wll = Well44497b(tuple(i for i in range(TestWell44497b.Well44497b_STATE_SIZE)))  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            wll = Well44497b(list(i+10 for i in range(TestWell44497b.Well44497b_STATE_SIZE)))  # type: ignore
            assert wll._index == 0
            assert wll.gauss_next is None  # type: ignore
            assert wll._state == list(i+10 for i in range(TestWell44497b.Well44497b_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            wll = Well44497b((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well44497b((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well44497b([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well44497b([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well44497b(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        wll = Well44497b(0x0123_4567_89ab_cdef)
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll._state[ 125] == 0x9c889382
        assert wll._state[ 356] == 0x253a378b
        assert wll._state[ 587] == 0x690c72ab
        assert wll._state[ 818] == 0x78f5d84f
        assert wll._state[1049] == 0x8375eb49
        assert wll._state[1280] == 0x92e2ba8b

        for v in [0x5cbd80e9, 0xe4d7c606, 0x514f30a3, 0x7379b30b, 0xf3549668]:
            assert wll.next() == v

        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 1386
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[   9] == 0x2680d065
        assert wll._state[ 240] == 0x443ca02a
        assert wll._state[ 471] == 0xcda43b6a
        assert wll._state[ 702] == 0x033dc469
        assert wll._state[ 933] == 0x0a34b280
        assert wll._state[1164] == 0x0e1d2eaf

        wll._index = 1
        wll.next()
        assert wll._index == 0

    #-------------------------------------------------------------------------
    def test_seed(self):
        wll = Well44497b()
        
        wll.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 127] == 0x33f37c98
        assert wll._state[ 358] == 0xd9760a2a
        assert wll._state[ 589] == 0x2774c2e3
        assert wll._state[ 820] == 0x3827beea
        assert wll._state[1051] == 0xb9dcad84
        assert wll._state[1282] == 0x986d6ae2

        wll.seed(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[   0] == 0x5fee464f
        assert wll._state[ 231] == 0xa1c9c800
        assert wll._state[ 462] == 0x9b8c5c6f
        assert wll._state[ 693] == 0xf6d7870f
        assert wll._state[ 924] == 0xb5682bb8
        assert wll._state[1155] == 0xeae78622
        assert wll._state[1386] == 0xb47820d7

        with pytest.raises(ValueError):
            wll.seed(-0.0001)
        with pytest.raises(ValueError):
            wll.seed(1.001)

        wll.seed()
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 64) for s in wll._state)  # type: ignore

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
        wll = Well44497b()

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

        wll.setstate((tuple(i+31 for i in range(TestWell44497b.Well44497b_STATE_SIZE)), 3))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+31 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        wll.setstate([[i+41 for i in range(TestWell44497b.Well44497b_STATE_SIZE)], TestWell44497b.Well44497b_STATE_SIZE + 8])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+41 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        wll.setstate([tuple(i+51 for i in range(TestWell44497b.Well44497b_STATE_SIZE)), 3])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+51 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        wll.setstate(([i+61 for i in range(TestWell44497b.Well44497b_STATE_SIZE)], TestWell44497b.Well44497b_STATE_SIZE + 8))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+61 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        wll.setstate(tuple(i+11 for i in range(TestWell44497b.Well44497b_STATE_SIZE)))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+11 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

        wll.setstate([i+21 for i in range(TestWell44497b.Well44497b_STATE_SIZE)])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+21 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore
            _state[TestWell44497b.Well44497b_STATE_SIZE - 2] = -1
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore
            _state[TestWell44497b.Well44497b_STATE_SIZE - 3] = 0.321
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell44497b.Well44497b_STATE_SIZE)]  # type: ignore
            _state[TestWell44497b.Well44497b_STATE_SIZE - 5] = {1, 2}
            wll.setstate(_state)  # type: ignore
