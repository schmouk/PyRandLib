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

from PyRandLib.mrg1457 import Mrg1457


#=============================================================================
class TestMrg1457:
    """Tests class Mrg1457.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')
    Mrg1457_STATE_SIZE = 47

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Mrg1457._NORMALIZE == 1.0 / (1 << 31)
        assert Mrg1457._OUT_BITS == 31
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        mrg = Mrg1457()
        assert mrg._STATE_SIZE == TestMrg1457.Mrg1457_STATE_SIZE
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        mrg = Mrg1457(1)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 1] == 0x5f75c6d0
        assert mrg._state[ 8] == 0x248b8c6f
        assert mrg._state[15] == 0x1561670b
        assert mrg._state[22] == 0x3f78fe87
        assert mrg._state[29] == 0x7fb633f4
        assert mrg._state[36] == 0x45970122
        assert mrg._state[43] == 0x53ff869c

        mrg = Mrg1457(-2)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 5] == 0x6c2d5bd1
        assert mrg._state[12] == 0x470f871c
        assert mrg._state[19] == 0x6422863b
        assert mrg._state[26] == 0x59d7f561
        assert mrg._state[33] == 0x72f3a638
        assert mrg._state[40] == 0x7854c5c6

        mrg = Mrg1457(0x0123_4567_89ab_cdef)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 6] == 0x5c7e2d88
        assert mrg._state[13] == 0x4bfb634c
        assert mrg._state[20] == 0x2d159a4f
        assert mrg._state[27] == 0x2c8d3baa
        assert mrg._state[34] == 0x7bd16646
        assert mrg._state[41] == 0x3fd8cb74

        mrg = Mrg1457(-8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 1] == 0x717de1a2
        assert mrg._state[ 8] == 0x15370809
        assert mrg._state[15] == 0x7f5b31cc
        assert mrg._state[22] == 0x00971099
        assert mrg._state[29] == 0x31117f8c
        assert mrg._state[36] == 0x50c40395
        assert mrg._state[43] == 0x040e8e0c

        mrg = Mrg1457(8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 6] == 0x0a043caf
        assert mrg._state[13] == 0x1c9c87c0
        assert mrg._state[20] == 0x1441a9fd
        assert mrg._state[27] == 0x253d0f34
        assert mrg._state[34] == 0x21c338cc
        assert mrg._state[41] == 0x035dae05

        mrg = Mrg1457(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 6] == 0x3d2fb3f1
        assert mrg._state[13] == 0x34f8bf70
        assert mrg._state[20] == 0x76b742cd
        assert mrg._state[27] == 0x500eecfc
        assert mrg._state[34] == 0x227a9b47
        assert mrg._state[41] == 0x1dacc61b

    #-------------------------------------------------------------------------
    def test_init_float(self):
        mrg = Mrg1457(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 0] == 0x2ff72327
        assert mrg._state[ 7] == 0x735a9b30
        assert mrg._state[14] == 0x0fcc7e29
        assert mrg._state[21] == 0x177d97f7
        assert mrg._state[28] == 0x0cd45b20
        assert mrg._state[35] == 0x023a8f66
        assert mrg._state[42] == 0x4c4169e8

        mrg = Mrg1457(1.0)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

        with pytest.raises(ValueError):
            mrg = Mrg1457(-0.0001)
        with pytest.raises(ValueError):
            mrg = Mrg1457(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        mrg = Mrg1457(tuple(i for i in range(TestMrg1457.Mrg1457_STATE_SIZE)))  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                mrg = Mrg1457(list(i+10 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)))  # type: ignore
        else:
            mrg = Mrg1457(list(i+10 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)))  # type: ignore
            assert mrg._index == 0
            assert mrg.gauss_next is None  # type: ignore
            assert mrg._state == list(i+10 for i in range(TestMrg1457.Mrg1457_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            mrg = Mrg1457((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg1457((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg1457([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg1457([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg1457(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        mrg = Mrg1457(0x0123_4567_89ab_cdef)
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 6] == 0x5c7e2d88
        assert mrg._state[13] == 0x4bfb634c
        assert mrg._state[20] == 0x2d159a4f
        assert mrg._state[27] == 0x2c8d3baa
        assert mrg._state[34] == 0x7bd16646
        assert mrg._state[41] == 0x3fd8cb74

        for v in [0x5b9a0a70, 0x11db2b21, 0x762504bd, 0x48cacaca, 0x0af720ea]:
            assert mrg.next() == v

        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 5
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 2] == 0x762504bd
        assert mrg._state[ 9] == 0x13406832
        assert mrg._state[16] == 0x155c6271
        assert mrg._state[23] == 0x7bf4ffba
        assert mrg._state[30] == 0x048c9f63
        assert mrg._state[37] == 0x1efd7e94
        assert mrg._state[44] == 0x532cd602

    #-------------------------------------------------------------------------
    def test_seed(self):
        mrg = Mrg1457()
        
        mrg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 6] == 0x3d2fb3f1
        assert mrg._state[13] == 0x34f8bf70
        assert mrg._state[20] == 0x76b742cd
        assert mrg._state[27] == 0x500eecfc
        assert mrg._state[34] == 0x227a9b47
        assert mrg._state[41] == 0x1dacc61b

        mrg.seed(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 0] == 0x2ff72327
        assert mrg._state[ 7] == 0x735a9b30
        assert mrg._state[14] == 0x0fcc7e29
        assert mrg._state[21] == 0x177d97f7
        assert mrg._state[28] == 0x0cd45b20
        assert mrg._state[35] == 0x023a8f66
        assert mrg._state[42] == 0x4c4169e8

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
        mrg = Mrg1457()

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

        mrg.setstate((tuple(i+31 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)), 3))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+31 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        mrg.setstate([[i+41 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)], TestMrg1457.Mrg1457_STATE_SIZE + 8])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+41 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        mrg.setstate([tuple(i+51 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)), 3])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+51 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        mrg.setstate(([i+61 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)], TestMrg1457.Mrg1457_STATE_SIZE + 8))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+61 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        mrg.setstate(tuple(i+11 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+11 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

        mrg.setstate([i+21 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+21 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore
            _state[TestMrg1457.Mrg1457_STATE_SIZE - 2] = -1
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore
            _state[TestMrg1457.Mrg1457_STATE_SIZE - 3] = 0.321
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg1457.Mrg1457_STATE_SIZE)]  # type: ignore
            _state[TestMrg1457.Mrg1457_STATE_SIZE - 5] = {1, 2}
            mrg.setstate(_state)  # type: ignore
