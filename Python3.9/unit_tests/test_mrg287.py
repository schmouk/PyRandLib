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

from PyRandLib.mrg287 import Mrg287


#=============================================================================
class TestMrg287:
    """Tests class Mrg287.
    """
    
    Mrg287_STATE_SIZE = 256

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Mrg287._NORMALIZE == 1.0 / (1 << 32)
        assert Mrg287._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        mrg = Mrg287()
        assert mrg._STATE_SIZE == TestMrg287.Mrg287_STATE_SIZE
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        mrg = Mrg287(1)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  1] == 0xbeeb8da1
        assert mrg._state[ 43] == 0xa7ff0d38
        assert mrg._state[ 85] == 0xf0dad827
        assert mrg._state[127] == 0x6524e51f
        assert mrg._state[169] == 0x100ba66a
        assert mrg._state[211] == 0xb4bdc811
        assert mrg._state[253] == 0x7804cbe7

        mrg = Mrg287(-2)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 40] == 0xf0a98b8d
        assert mrg._state[ 82] == 0xb2624a7c
        assert mrg._state[124] == 0x62be4a8f
        assert mrg._state[166] == 0xe7fa3f41
        assert mrg._state[208] == 0x9a81c04b
        assert mrg._state[250] == 0x4e0895df

        mrg = Mrg287(0x0123_4567_89ab_cdef)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 27] == 0x591a7755
        assert mrg._state[ 69] == 0xed265d05
        assert mrg._state[111] == 0x50850db1
        assert mrg._state[153] == 0x55e4c9e5
        assert mrg._state[195] == 0x442c3cd8
        assert mrg._state[237] == 0xef61a955

        mrg = Mrg287(-8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 22] == 0x012e2133
        assert mrg._state[ 64] == 0x6de00a02
        assert mrg._state[106] == 0xc968b7ee
        assert mrg._state[148] == 0x1c661102
        assert mrg._state[190] == 0x36b3b4b1
        assert mrg._state[232] == 0x99c2bd69

        mrg = Mrg287(8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 20] == 0x288353fb
        assert mrg._state[ 62] == 0xc56561d5
        assert mrg._state[104] == 0x58e9b28d
        assert mrg._state[146] == 0xfceb2f8c
        assert mrg._state[188] == 0x6bfd76c0
        assert mrg._state[230] == 0x687a6e56

        mrg = Mrg287(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 27] == 0xa01dd9f8
        assert mrg._state[ 69] == 0xbadf8c45
        assert mrg._state[111] == 0xd7db021b
        assert mrg._state[153] == 0xd0ad13da
        assert mrg._state[195] == 0x72bd3013
        assert mrg._state[237] == 0x78f88cbf

    #-------------------------------------------------------------------------
    def test_init_float(self):
        mrg = Mrg287(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  0] == 0x5fee464f
        assert mrg._state[ 42] == 0x9882d3d0
        assert mrg._state[ 84] == 0x0a02114b
        assert mrg._state[126] == 0x1d616c45
        assert mrg._state[168] == 0xe93c7669
        assert mrg._state[210] == 0x5bcac23d
        assert mrg._state[252] == 0xe2635469

        mrg = Mrg287(1.0)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

        with pytest.raises(ValueError):
            mrg = Mrg287(-0.0001)
        with pytest.raises(ValueError):
            mrg = Mrg287(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        mrg = Mrg287(tuple(i for i in range(TestMrg287.Mrg287_STATE_SIZE)))  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            mrg = Mrg287(list(i+10 for i in range(TestMrg287.Mrg287_STATE_SIZE)))  # type: ignore
            assert mrg._index == 0
            assert mrg.gauss_next is None  # type: ignore
            assert mrg._state == list(i+10 for i in range(TestMrg287.Mrg287_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            mrg = Mrg287((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg287((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg287([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg287([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg287(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        mrg = Mrg287(0x0123_4567_89ab_cdef)
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 27] == 0x591a7755
        assert mrg._state[ 69] == 0xed265d05
        assert mrg._state[111] == 0x50850db1
        assert mrg._state[153] == 0x55e4c9e5
        assert mrg._state[195] == 0x442c3cd8
        assert mrg._state[237] == 0xef61a955

        for v in [0x189f70e0, 0x128dcd48, 0x370e755c, 0xc77233f8, 0xdbe891b3]:
            assert mrg.next() == v

        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 5
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  6] == 0xb8fc5b10
        assert mrg._state[ 48] == 0x42e5f9bb
        assert mrg._state[ 90] == 0x591d691f
        assert mrg._state[132] == 0x2f98b506
        assert mrg._state[174] == 0x1280ba85
        assert mrg._state[216] == 0x42ff9df5

    #-------------------------------------------------------------------------
    def test_seed(self):
        mrg = Mrg287()
        
        mrg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 27] == 0xa01dd9f8
        assert mrg._state[ 69] == 0xbadf8c45
        assert mrg._state[111] == 0xd7db021b
        assert mrg._state[153] == 0xd0ad13da
        assert mrg._state[195] == 0x72bd3013
        assert mrg._state[237] == 0x78f88cbf

        mrg.seed(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  0] == 0x5fee464f
        assert mrg._state[ 42] == 0x9882d3d0
        assert mrg._state[ 84] == 0x0a02114b
        assert mrg._state[126] == 0x1d616c45
        assert mrg._state[168] == 0xe93c7669
        assert mrg._state[210] == 0x5bcac23d
        assert mrg._state[252] == 0xe2635469

        with pytest.raises(ValueError):
            mrg.seed(-0.0001)
        with pytest.raises(ValueError):
            mrg.seed(1.001)

        mrg.seed()
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

        with pytest.raises(TypeError):
            mrg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            mrg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            mrg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            mrg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            mrg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        mrg = Mrg287()

        mrg.setstate()
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore
    
        with pytest.raises(TypeError):
            mrg.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            mrg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            mrg.setstate("123")  # type: ignore

        mrg.setstate((tuple(i+31 for i in range(TestMrg287.Mrg287_STATE_SIZE)), 3))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+31 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        mrg.setstate([[i+41 for i in range(TestMrg287.Mrg287_STATE_SIZE)], TestMrg287.Mrg287_STATE_SIZE + 8])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+41 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        mrg.setstate([tuple(i+51 for i in range(TestMrg287.Mrg287_STATE_SIZE)), 3])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+51 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        mrg.setstate(([i+61 for i in range(TestMrg287.Mrg287_STATE_SIZE)], TestMrg287.Mrg287_STATE_SIZE + 8))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+61 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        mrg.setstate(tuple(i+11 for i in range(TestMrg287.Mrg287_STATE_SIZE)))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+11 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        mrg.setstate([i+21 for i in range(TestMrg287.Mrg287_STATE_SIZE)])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+21 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            mrg.setstate([1, 2])
        with pytest.raises(TypeError):
            mrg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            mrg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            mrg.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore
            _state[TestMrg287.Mrg287_STATE_SIZE - 2] = -1
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore
            _state[TestMrg287.Mrg287_STATE_SIZE - 3] = 0.321
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg287.Mrg287_STATE_SIZE)]  # type: ignore
            _state[TestMrg287.Mrg287_STATE_SIZE - 5] = {1, 2}
            mrg.setstate(_state)  # type: ignore
