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

from PyRandLib.lfib78 import LFib78


#=============================================================================
class TestLFib78:
    """Tests class LFib78.
    """
    
    LFib78_STATE_SIZE = 17

    #-------------------------------------------------------------------------
    def test_class(self):
        assert LFib78._NORMALIZE == 1.0 / (1 << 64)
        assert LFib78._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lfib = LFib78()
        assert lfib._STATE_SIZE == TestLFib78.LFib78_STATE_SIZE
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lfib = LFib78(1)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xbeeb8da1658eec67
        assert lfib._state[4]  == 0x71bb54d8d101b5b9
        assert lfib._state[7]  == 0x85e7bb0f12278575
        assert lfib._state[10] == 0x6775dc7701564f61
        assert lfib._state[13] == 0x87b341d690d7a28a
        assert lfib._state[16] == 0xa534a6a6b7fd0b63

        lfib = LFib78(-2)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xba56949915dcf9e9
        assert lfib._state[4]  == 0x7842841591543f1d
        assert lfib._state[7]  == 0x1e2b53fb7bd63f05
        assert lfib._state[10] == 0x2b724bbbfb591868
        assert lfib._state[13] == 0x8457d34b5125f667
        assert lfib._state[16] == 0xd3e46307eece8848

        lfib = LFib78(0x0123_4567_89ab_cdef)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xd573529b34a1d093
        assert lfib._state[4]  == 0x01404ce914938008
        assert lfib._state[7]  == 0x8931545f4f9ea651
        assert lfib._state[10] == 0xcdb8c9cd9a62da0f
        assert lfib._state[13] == 0x97f6c69811cfb13b
        assert lfib._state[16] == 0x2ab8c4e395cb5958

        lfib = LFib78(-8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xe2fbc345a799b5aa
        assert lfib._state[4]  == 0x2a03b9aff2bfd421
        assert lfib._state[7]  == 0xe6d2502493ff622e
        assert lfib._state[10] == 0x4592e2e878ff1b75
        assert lfib._state[13] == 0xfbe6cd715ff52a4a
        assert lfib._state[16] == 0x61075d5da12791c9

        lfib = LFib78(8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xa6eb6466bac9f251
        assert lfib._state[4]  == 0xe1b0fb2c7e764cdb
        assert lfib._state[7]  == 0xe0c07d9420f2f41e
        assert lfib._state[10] == 0xa92d263b8e9fbd45
        assert lfib._state[13] == 0x39390f80db89e31d
        assert lfib._state[16] == 0xcbe9dce4849cf8e6

        lfib = LFib78(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xec779c3693f88501
        assert lfib._state[4]  == 0x260ffb0260bbbe5f
        assert lfib._state[7]  == 0xd7c07017388fa2af
        assert lfib._state[10] == 0x71da8c61bc0cfda9
        assert lfib._state[13] == 0x69f17ee1a874dbdd
        assert lfib._state[16] == 0x66fb5ba3ae1546e0

    #-------------------------------------------------------------------------
    def test_init_float(self):
        lfib = LFib78(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0x954faf5a9ad49cf8
        assert lfib._state[4]  == 0xa3aac457d81d552c
        assert lfib._state[7]  == 0xe6b536617ee8b60c
        assert lfib._state[10] == 0x0df3d30dc1390db9
        assert lfib._state[13] == 0xee8fd4bfccca5ee3
        assert lfib._state[16] == 0x63be72f7c7521c27

        lfib = LFib78(1.0)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

        with pytest.raises(ValueError):
            lfib = LFib78(-0.0001)
        with pytest.raises(ValueError):
            lfib = LFib78(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lfib = LFib78(tuple(i for i in range(TestLFib78.LFib78_STATE_SIZE)))  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashalbe lists bug in Python 3.10
            lfib = LFib78(list(i+10 for i in range(TestLFib78.LFib78_STATE_SIZE)))  # type: ignore
            assert lfib._index == 0
            assert lfib.gauss_next is None  # type: ignore
            assert lfib._state == list(i+10 for i in range(TestLFib78.LFib78_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            lfib = LFib78((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib78((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib78([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib78([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib78(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lfib = LFib78(0x0123_4567_89ab_cdef)
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xd573529b34a1d093
        assert lfib._state[4]  == 0x01404ce914938008
        assert lfib._state[7]  == 0x8931545f4f9ea651
        assert lfib._state[10] == 0xcdb8c9cd9a62da0f
        assert lfib._state[13] == 0x97f6c69811cfb13b
        assert lfib._state[16] == 0x2ab8c4e395cb5958

        for v in [0xa434bdba328721e4, 0x6d6a1933467181ce, 0x679f428b01be068d, 0x7abfe5d4e9902be1, 0x2bf911ccaa5ed960]:
            assert lfib.next() == v

        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0x6d6a1933467181ce
        assert lfib._state[4]  == 0x2bf911ccaa5ed960
        assert lfib._state[7]  == 0x8931545f4f9ea651
        assert lfib._state[10] == 0xcdb8c9cd9a62da0f
        assert lfib._state[13] == 0x97f6c69811cfb13b
        assert lfib._state[16] == 0x2ab8c4e395cb5958

    #-------------------------------------------------------------------------
    def test_seed(self):
        lfib = LFib78()
        
        lfib.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0xec779c3693f88501
        assert lfib._state[4]  == 0x260ffb0260bbbe5f
        assert lfib._state[7]  == 0xd7c07017388fa2af
        assert lfib._state[10] == 0x71da8c61bc0cfda9
        assert lfib._state[13] == 0x69f17ee1a874dbdd
        assert lfib._state[16] == 0x66fb5ba3ae1546e0

        lfib.seed(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[1]  == 0x954faf5a9ad49cf8
        assert lfib._state[4]  == 0xa3aac457d81d552c
        assert lfib._state[7]  == 0xe6b536617ee8b60c
        assert lfib._state[10] == 0x0df3d30dc1390db9
        assert lfib._state[13] == 0xee8fd4bfccca5ee3
        assert lfib._state[16] == 0x63be72f7c7521c27

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
        lfib = LFib78()

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

        lfib.setstate((tuple(i+31 for i in range(TestLFib78.LFib78_STATE_SIZE)), 3))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+31 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        lfib.setstate([[i+41 for i in range(TestLFib78.LFib78_STATE_SIZE)], 18])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 1
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+41 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        lfib.setstate([tuple(i+51 for i in range(TestLFib78.LFib78_STATE_SIZE)), 3])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+51 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        lfib.setstate(([i+61 for i in range(TestLFib78.LFib78_STATE_SIZE)], 18))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 1
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+61 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        lfib.setstate(tuple(i+11 for i in range(TestLFib78.LFib78_STATE_SIZE)))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+11 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

        lfib.setstate([i+21 for i in range(TestLFib78.LFib78_STATE_SIZE)])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+21 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore
            _state[15] = -1
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore
            _state[12] = 0.321
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib78.LFib78_STATE_SIZE)]  # type: ignore
            _state[12] = {1, 2}
            lfib.setstate(_state)  # type: ignore
