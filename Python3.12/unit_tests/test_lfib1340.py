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

from PyRandLib.lfib1340 import LFib1340


#=============================================================================
class TestLFib1340:
    """Tests class LFib1340.
    """
    
    LFib1340_STATE_SIZE = 1279

    #-------------------------------------------------------------------------
    def test_class(self):
        assert LFib1340._NORMALIZE == 1.0 / (1 << 64)
        assert LFib1340._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lfib = LFib1340()
        assert lfib._STATE_SIZE == TestLFib1340.LFib1340_STATE_SIZE
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lfib = LFib1340(1)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  72] == 0xf902155aa328d575
        assert lfib._state[ 285] == 0x741cad5364f02a78
        assert lfib._state[ 498] == 0xb844e2ec5f91aae4
        assert lfib._state[ 711] == 0x3a62209c3fcf0186
        assert lfib._state[ 924] == 0x5fa048438ae81274
        assert lfib._state[1137] == 0xba01f31340cbe6dd

        lfib = LFib1340(-2)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  69] == 0x7892c83522f7d7ef
        assert lfib._state[ 282] == 0xf37b8c9e51800f48
        assert lfib._state[ 495] == 0xc314d56916b97b66
        assert lfib._state[ 708] == 0xdbc7469e2509e204
        assert lfib._state[ 921] == 0x6939f1bb0f77111a
        assert lfib._state[1134] == 0x700be0b1f884906f

        lfib = LFib1340(0x0123_4567_89ab_cdef)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 176] == 0x349ffd38cb9dd55d
        assert lfib._state[ 389] == 0xd57d7467699349cb
        assert lfib._state[ 602] == 0x2736fee2a4e1416a
        assert lfib._state[ 815] == 0x1251b233b6bee6b8
        assert lfib._state[1028] == 0x3fb8a1cf72aa7d52
        assert lfib._state[1241] == 0x5a8736fd16abc59e

        lfib = LFib1340(-8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 114] == 0x58936da4dd390547
        assert lfib._state[ 327] == 0xc4b92afd301cb2b4
        assert lfib._state[ 540] == 0xcfde8fee4028fe15
        assert lfib._state[ 753] == 0x350ffeb259eadcc7
        assert lfib._state[ 966] == 0x509add6ee2f82a6d
        assert lfib._state[1179] == 0x8b52f609e9039839

        lfib = LFib1340(8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  28] == 0x8670f33f969fb20d
        assert lfib._state[ 241] == 0x780261dabe792b80
        assert lfib._state[ 454] == 0x20c9a6945b67e651
        assert lfib._state[ 667] == 0x0c18711ceef4d0f2
        assert lfib._state[ 880] == 0x6c73ee9b31f3a8db
        assert lfib._state[1093] == 0x10187b94f0384098

        lfib = LFib1340(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 158] == 0xd461ce58038fc9f9
        assert lfib._state[ 371] == 0x10970a243a7818bb
        assert lfib._state[ 584] == 0x53add06887e5c0fd
        assert lfib._state[ 797] == 0x26d20c416ef4b509
        assert lfib._state[1010] == 0xfeb0fca0a50ab9d2
        assert lfib._state[1223] == 0xf68183fdd3bb40e8

    #-------------------------------------------------------------------------
    def test_init_float(self):
        lfib = LFib1340(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  71] == 0x7fde3752e0b07d27
        assert lfib._state[ 284] == 0xefc598238522eb63
        assert lfib._state[ 497] == 0x91af6061e4006dcc
        assert lfib._state[ 710] == 0x312725df9584eeb3
        assert lfib._state[ 923] == 0xb6716d176c4b597a
        assert lfib._state[1136] == 0x224cf21abad4b4ae

        lfib = LFib1340(1.0)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

        with pytest.raises(ValueError):
            lfib = LFib1340(-0.0001)
        with pytest.raises(ValueError):
            lfib = LFib1340(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lfib = LFib1340(tuple(i for i in range(TestLFib1340.LFib1340_STATE_SIZE)))  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib = LFib1340(list(i+10 for i in range(TestLFib1340.LFib1340_STATE_SIZE)))  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == list(i+10 for i in range(TestLFib1340.LFib1340_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            lfib = LFib1340((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib1340((i for i in range(TestLFib1340.LFib1340_STATE_SIZE+1)))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib1340([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib1340([i for i in range(TestLFib1340.LFib1340_STATE_SIZE+1)])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib1340(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lfib = LFib1340(0x0123_4567_89ab_cdef)
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 176] == 0x349ffd38cb9dd55d
        assert lfib._state[ 389] == 0xd57d7467699349cb
        assert lfib._state[ 602] == 0x2736fee2a4e1416a
        assert lfib._state[ 815] == 0x1251b233b6bee6b8
        assert lfib._state[1028] == 0x3fb8a1cf72aa7d52
        assert lfib._state[1241] == 0x5a8736fd16abc59e

        for v in [0xf808ad0938a84212, 0x8bcb541c42eef6b5, 0x94d93887673e368f, 0x4c922b172455da8f, 0xda7f94589c17e131]:
            assert lfib.next() == v

        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  34] == 0xf7a2cc8df2b2c4f6
        assert lfib._state[ 247] == 0x7e07ab8606a92cfc
        assert lfib._state[ 460] == 0x997ee6416930557b
        assert lfib._state[ 673] == 0x20d4e5146b3bff6d
        assert lfib._state[ 886] == 0x3b2ee6608180063f
        assert lfib._state[1099] == 0x820166d19fd2b597

    #-------------------------------------------------------------------------
    def test_seed(self):
        lfib = LFib1340()
        
        lfib.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 158] == 0xd461ce58038fc9f9
        assert lfib._state[ 371] == 0x10970a243a7818bb
        assert lfib._state[ 584] == 0x53add06887e5c0fd
        assert lfib._state[ 797] == 0x26d20c416ef4b509
        assert lfib._state[1010] == 0xfeb0fca0a50ab9d2
        assert lfib._state[1223] == 0xf68183fdd3bb40e8

        lfib.seed(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  71] == 0x7fde3752e0b07d27
        assert lfib._state[ 284] == 0xefc598238522eb63
        assert lfib._state[ 497] == 0x91af6061e4006dcc
        assert lfib._state[ 710] == 0x312725df9584eeb3
        assert lfib._state[ 923] == 0xb6716d176c4b597a
        assert lfib._state[1136] == 0x224cf21abad4b4ae

        with pytest.raises(ValueError):
            lfib.seed(-0.0001)
        with pytest.raises(ValueError):
            lfib.seed(1.001)

        lfib.seed()
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

        with pytest.raises(TypeError):
            lfib.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lfib.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            lfib.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lfib.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            lfib.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        lfib = LFib1340()

        lfib.setstate()
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore
    
        with pytest.raises(TypeError):
            lfib.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            lfib.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            lfib.setstate("123")  # type: ignore

        lfib.setstate((tuple(i+31 for i in range(TestLFib1340.LFib1340_STATE_SIZE)), 3))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+31 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib.setstate([[i+41 for i in range(TestLFib1340.LFib1340_STATE_SIZE)], TestLFib1340.LFib1340_STATE_SIZE+5])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+41 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib.setstate([tuple(i+51 for i in range(TestLFib1340.LFib1340_STATE_SIZE)), 3])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+51 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib.setstate(([i+61 for i in range(TestLFib1340.LFib1340_STATE_SIZE)], TestLFib1340.LFib1340_STATE_SIZE+11))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 11
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+61 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib.setstate(tuple(i+11 for i in range(TestLFib1340.LFib1340_STATE_SIZE)))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+11 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        lfib.setstate([i+21 for i in range(TestLFib1340.LFib1340_STATE_SIZE)])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+21 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            lfib.setstate([1, 2])
        with pytest.raises(TypeError):
            lfib.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            lfib.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            lfib.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore
            _state[15] = -1
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore
            _state[12] = 0.321
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib1340.LFib1340_STATE_SIZE)]  # type: ignore
            _state[12] = {1, 2}
            lfib.setstate(_state)  # type: ignore
