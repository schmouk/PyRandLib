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
import pytest
import platform

from PyRandLib.listindexstate import ListIndexState
from PyRandLib.splitmix       import SplitMix31, SplitMix32, SplitMix63, SplitMix64


#=============================================================================
class TestListIndexState:
    """Tests class SplitMix64.
    """

    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')

    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lis = ListIndexState(SplitMix31, 15)
        assert lis._initRandClass == SplitMix31
        assert lis._STATE_SIZE == 15
        assert lis._index == 0
        assert len(lis._state) == 15
        assert all(isinstance(s, int) for s in lis._state)
        assert all(0 <= s <= 0x7fff_ffff for s in lis._state)  # type: ignore


    #-------------------------------------------------------------------------
    def test_init_int(self):
        lis = ListIndexState(SplitMix64, 17, 1)
        assert lis._initRandClass == SplitMix64
        assert lis._STATE_SIZE == 17
        assert lis._index == 0
        assert len(lis._state) == 17
        assert lis._state[1]  == 0xbeeb8da1658eec67
        assert lis._state[4]  == 0x71bb54d8d101b5b9
        assert lis._state[7]  == 0x85e7bb0f12278575
        assert lis._state[10] == 0x6775dc7701564f61
        assert lis._state[13] == 0x87b341d690d7a28a
        assert lis._state[16] == 0xa534a6a6b7fd0b63

        lis = ListIndexState(SplitMix63, 15, -2)
        assert lis._initRandClass == SplitMix63
        assert lis._STATE_SIZE == 15
        assert lis._index == 0
        assert len(lis._state) == 15
        assert lis._state[1]  == 0xba56949915dcf9e9 >> 1
        assert lis._state[4]  == 0x7842841591543f1d >> 1
        assert lis._state[7]  == 0x1e2b53fb7bd63f05 >> 1
        assert lis._state[10] == 0x2b724bbbfb591868 >> 1
        assert lis._state[13] == 0x8457d34b5125f667 >> 1

        lis = ListIndexState(SplitMix32, 21, 0x0123_4567_89ab_cdef)
        assert lis._initRandClass == SplitMix32
        assert lis._STATE_SIZE == 21
        assert lis._index == 0
        assert len(lis._state) == 21
        assert lis._state[1]  == 0xd573529b34a1d093 >> 32
        assert lis._state[4]  == 0x01404ce914938008 >> 32
        assert lis._state[7]  == 0x8931545f4f9ea651 >> 32
        assert lis._state[10] == 0xcdb8c9cd9a62da0f >> 32
        assert lis._state[13] == 0x97f6c69811cfb13b >> 32
        assert lis._state[16] == 0x2ab8c4e395cb5958 >> 32

        lis = ListIndexState(SplitMix63, 11, -8_870_000_000_000_000_000)
        assert lis._initRandClass == SplitMix63
        assert lis._STATE_SIZE == 11
        assert lis._index == 0
        assert len(lis._state) == 11
        assert lis._state[1]  == 0xe2fbc345a799b5aa >> 1
        assert lis._state[4]  == 0x2a03b9aff2bfd421 >> 1
        assert lis._state[7]  == 0xe6d2502493ff622e >> 1
        assert lis._state[10] == 0x4592e2e878ff1b75 >> 1

        lis = ListIndexState(SplitMix64, 27, 8_870_000_000_000_000_000)
        assert lis._initRandClass == SplitMix64
        assert lis._STATE_SIZE == 27
        assert lis._index == 0
        assert len(lis._state) == 27
        assert lis._state[1]  == 0xa6eb6466bac9f251
        assert lis._state[4]  == 0xe1b0fb2c7e764cdb
        assert lis._state[7]  == 0xe0c07d9420f2f41e
        assert lis._state[10] == 0xa92d263b8e9fbd45
        assert lis._state[13] == 0x39390f80db89e31d
        assert lis._state[16] == 0xcbe9dce4849cf8e6

        lis = ListIndexState(SplitMix31, 31, 0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lis._initRandClass == SplitMix31
        assert lis._STATE_SIZE == 31
        assert lis._index == 0
        assert len(lis._state) == 31
        assert lis._state[1]  == 0xec779c3693f88501 >> 33
        assert lis._state[4]  == 0x260ffb0260bbbe5f >> 33
        assert lis._state[7]  == 0xd7c07017388fa2af >> 33
        assert lis._state[10] == 0x71da8c61bc0cfda9 >> 33
        assert lis._state[13] == 0x69f17ee1a874dbdd >> 33
        assert lis._state[16] == 0x66fb5ba3ae1546e0 >> 33

    #-------------------------------------------------------------------------
    def test_init_float(self):
        lis = ListIndexState(SplitMix63, 27, 0.357)
        assert lis._initRandClass == SplitMix63
        assert lis._STATE_SIZE == 27
        assert lis._index == 0
        assert len(lis._state) == 27
        assert lis._state[1]  == 0x954faf5a9ad49cf8 >> 1
        assert lis._state[4]  == 0xa3aac457d81d552c >> 1
        assert lis._state[7]  == 0xe6b536617ee8b60c >> 1
        assert lis._state[10] == 0x0df3d30dc1390db9 >> 1
        assert lis._state[13] == 0xee8fd4bfccca5ee3 >> 1
        assert lis._state[16] == 0x63be72f7c7521c27 >> 1

        lis = ListIndexState(SplitMix32, 27, 1.0)
        assert lis._initRandClass == SplitMix32
        assert lis._STATE_SIZE == 27
        assert lis._index == 0
        assert len(lis._state) == 27
        assert all(isinstance(s, int) for s in lis._state)
        assert all(0 < s < (1 << 64) for s in lis._state)  # type: ignore

        with pytest.raises(ValueError):
            lis = ListIndexState(SplitMix64, 27, -0.0001)
        with pytest.raises(ValueError):
            lis = ListIndexState(SplitMix31, 27, 1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lis = ListIndexState(SplitMix32, 5, tuple(i+1 for i in range(5)))  # type: ignore
        assert lis._initRandClass == SplitMix32
        assert lis._STATE_SIZE == 5
        assert lis._index == 0
        assert len(lis._state) == 5
        assert lis._state == [i+1 for i in range(5)] 

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix31, 7, [i+11 for i in range(7)])  # type: ignore
        else:
            lis = ListIndexState(SplitMix31, 7, [i+11 for i in range(7)])  # type: ignore
            assert lis._initRandClass == SplitMix31
            assert lis._STATE_SIZE == 7
            assert lis._index == 0
            assert len(lis._state) == 7
            assert lis._state == [i+11 for i in range(7)] 

        lis = ListIndexState(SplitMix32, 5, (tuple(i+1 for i in range(5)), 8))  # type: ignore
        assert lis._initRandClass == SplitMix32
        assert lis._STATE_SIZE == 5
        assert lis._index == 3
        assert len(lis._state) == 5
        assert lis._state == [i+1 for i in range(5)] 

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix31, 7, ([i+11 for i in range(7)], 11))  # type: ignore
        else:
            lis = ListIndexState(SplitMix31, 7, ([i+11 for i in range(7)], 11))  # type: ignore
            assert lis._initRandClass == SplitMix31
            assert lis._STATE_SIZE == 7
            assert lis._index == 4
            assert len(lis._state) == 7
            assert lis._state == [i+11 for i in range(7)] 

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix31, 7, [i+11 for i in range(7)])  # type: ignore
        else:
            lis = ListIndexState(SplitMix32, 5, [tuple(i+1 for i in range(5)), 8])  # type: ignore
            assert lis._initRandClass == SplitMix32
            assert lis._STATE_SIZE == 5
            assert lis._index == 3
            assert len(lis._state) == 5
            assert lis._state == [i+1 for i in range(5)] 

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix31, 7, [[i+11 for i in range(7)], 11])  # type: ignore
        else:
            lis = ListIndexState(SplitMix31, 7, [[i+11 for i in range(7)], 11])  # type: ignore
            assert lis._initRandClass == SplitMix31
            assert lis._STATE_SIZE == 7
            assert lis._index == 4
            assert len(lis._state) == 7
            assert lis._state == [i+11 for i in range(7)]

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix64, 17, [])
        else:
            lis = ListIndexState(SplitMix64, 17, [])
            assert lis._initRandClass == SplitMix64
            assert lis._STATE_SIZE == 17
            assert lis._index == 0
            assert len(lis._state) == 17
            assert all(0 <= s < (1 << 64) for s in lis._state)  # type: ignore

        lis = ListIndexState(SplitMix64, 17, tuple())
        assert lis._initRandClass == SplitMix64
        assert lis._STATE_SIZE == 17
        assert lis._index == 0
        assert len(lis._state) == 17
        assert all(0 <= s < (1 << 64) for s in lis._state)  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix64, 11, [tuple(), 16])  # type: ignore
        else:
            with pytest.raises(ValueError):
                lis = ListIndexState(SplitMix64, 11, [tuple(), 16])  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lis = ListIndexState(SplitMix64, 11, [[], 9])  # type: ignore
        else:
            with pytest.raises(ValueError):
                lis = ListIndexState(SplitMix64, 11, [[], 9])  # type: ignore

        with pytest.raises(ValueError):
            lis = ListIndexState(SplitMix31, 5, ((1, 2, 3), 7))  # type: ignore
        with pytest.raises(TypeError):
            lis = ListIndexState(SplitMix32, 5, (1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lis = ListIndexState(SplitMix32, 5, (i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            llisfib = ListIndexState(SplitMix32, 5, [1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lis = ListIndexState(SplitMix32, 5, [i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            lis = ListIndexState(SplitMix32, 5, set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_getstate(self):
        state = (tuple(i+1 for i in range(17)), 16)
        lis = ListIndexState(SplitMix31, 17, state)  # type: ignore
        lis_state = lis.getstate()
        assert all(s == t for (s, t) in zip(state[0], lis_state[0]))  # type: ignore
        assert lis_state[1] == state[1] % 17  # type: ignore

        state33 = (tuple(i+1 for i in range(17)), 33)
        lis = ListIndexState(SplitMix31, 17, state33)  # type: ignore
        lis_state = lis.getstate()
        assert all(s == t for (s, t) in zip(state33[0], lis_state[0]))  # type: ignore
        assert lis_state[1] == state33[1] % 17  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_index(self):
        lis = ListIndexState(SplitMix31, 17)
        for i in range(-17, 33):
            lis._initindex(i)
            assert lis._index == i % 17
        
        with pytest.raises(TypeError):
            lis._initindex(1.2345)  # type: ignore
        with pytest.raises(TypeError):
            lis._initindex([0, 1])  # type: ignore
        with pytest.raises(TypeError):
            lis._initindex(set())  # type: ignore
