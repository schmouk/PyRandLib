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

from PyRandLib.mrg49507 import Mrg49507


#=============================================================================
class TestMrg49507:
    """Tests class Mrg49507.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')
    Mrg49507_STATE_SIZE = 1597

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Mrg49507._NORMALIZE == 1.0 / (1 << 31)
        assert Mrg49507._OUT_BITS == 31
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        mrg = Mrg49507()
        assert mrg._STATE_SIZE == TestMrg49507.Mrg49507_STATE_SIZE
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        mrg = Mrg49507(1)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[   1] == 0x5f75c6d0
        assert mrg._state[ 267] == 0x18eff17e
        assert mrg._state[ 533] == 0x55a11f7f
        assert mrg._state[ 799] == 0x74965c80
        assert mrg._state[1065] == 0x6460da87
        assert mrg._state[1331] == 0x4a7fad07

        mrg = Mrg49507(-2)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 264] == 0x5239e9e0
        assert mrg._state[ 530] == 0x24411a1a
        assert mrg._state[ 796] == 0x3f0a3f55
        assert mrg._state[1062] == 0x1ec33a01
        assert mrg._state[1328] == 0x6e2f037f
        assert mrg._state[1594] == 0x50768912

        mrg = Mrg49507(0x0123_4567_89ab_cdef)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 195] == 0x22161e6c
        assert mrg._state[ 461] == 0x2c540f50
        assert mrg._state[ 727] == 0x3dd37934
        assert mrg._state[ 993] == 0x322564a4
        assert mrg._state[1259] == 0x338c2677
        assert mrg._state[1525] == 0x214ccbe7

        mrg = Mrg49507(-8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 176] == 0x3a2a1d02
        assert mrg._state[ 442] == 0x290ae9c8
        assert mrg._state[ 708] == 0x23a1f3ef
        assert mrg._state[ 974] == 0x501cfb6f
        assert mrg._state[1240] == 0x23247fa1
        assert mrg._state[1506] == 0x141b3fde

        mrg = Mrg49507(8_870_000_000_000_000_000)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  90] == 0x52c8b378
        assert mrg._state[ 356] == 0x03cb6c1e
        assert mrg._state[ 622] == 0x5bb1be93
        assert mrg._state[ 888] == 0x22e6f2ce
        assert mrg._state[1154] == 0x7a3e53b6
        assert mrg._state[1420] == 0x42faeace

        mrg = Mrg49507(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  41] == 0x1dacc61b
        assert mrg._state[ 307] == 0x7d78f872
        assert mrg._state[ 573] == 0x132a5660
        assert mrg._state[ 839] == 0x59ea938c
        assert mrg._state[1105] == 0x21161c1b
        assert mrg._state[1371] == 0x0a371094

    #-------------------------------------------------------------------------
    def test_init_float(self):
        mrg = Mrg49507(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[   0] == 0x2ff72327
        assert mrg._state[ 266] == 0x0d50b0c0
        assert mrg._state[ 532] == 0x156820b8
        assert mrg._state[ 798] == 0x24a731ed
        assert mrg._state[1064] == 0x505a1c7e
        assert mrg._state[1330] == 0x18dca9e2

        mrg = Mrg49507(1.0)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in mrg._state)
        assert all(0 < s < (1 << 64) for s in mrg._state)  # type: ignore

        with pytest.raises(ValueError):
            mrg = Mrg49507(-0.0001)
        with pytest.raises(ValueError):
            mrg = Mrg49507(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        mrg = Mrg49507(tuple(i for i in range(TestMrg49507.Mrg49507_STATE_SIZE)))  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                mrg = Mrg49507(list(i+10 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)))  # type: ignore
        else:
            mrg = Mrg49507(list(i+10 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)))  # type: ignore
            assert mrg._index == 0
            assert mrg.gauss_next is None  # type: ignore
            assert mrg._state == list(i+10 for i in range(TestMrg49507.Mrg49507_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            mrg = Mrg49507((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg49507((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg49507([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg49507([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            mrg = Mrg49507(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        mrg = Mrg49507(0x0123_4567_89ab_cdef)
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[ 195] == 0x22161e6c
        assert mrg._state[ 461] == 0x2c540f50
        assert mrg._state[ 727] == 0x3dd37934
        assert mrg._state[ 993] == 0x322564a4
        assert mrg._state[1259] == 0x338c2677
        assert mrg._state[1525] == 0x214ccbe7

        for v in [0x142cabde, 0x616d6b20, 0x665602d0, 0x51eb821a, 0x129949ef]:
            assert mrg.next() == v

        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 5
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  62] == 0x3c1055e0
        assert mrg._state[ 328] == 0x2c69c157
        assert mrg._state[ 594] == 0x48128c13
        assert mrg._state[ 860] == 0x76d1e78c
        assert mrg._state[1126] == 0x6d472f68
        assert mrg._state[1392] == 0x21476161

    #-------------------------------------------------------------------------
    def test_seed(self):
        mrg = Mrg49507()
        
        mrg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[  41] == 0x1dacc61b
        assert mrg._state[ 307] == 0x7d78f872
        assert mrg._state[ 573] == 0x132a5660
        assert mrg._state[ 839] == 0x59ea938c
        assert mrg._state[1105] == 0x21161c1b
        assert mrg._state[1371] == 0x0a371094

        mrg.seed(0.357)
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state[   0] == 0x2ff72327
        assert mrg._state[ 266] == 0x0d50b0c0
        assert mrg._state[ 532] == 0x156820b8
        assert mrg._state[ 798] == 0x24a731ed
        assert mrg._state[1064] == 0x505a1c7e
        assert mrg._state[1330] == 0x18dca9e2

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
        mrg = Mrg49507()

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

        mrg.setstate((tuple(i+31 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)), 3))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+31 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        mrg.setstate([[i+41 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)], TestMrg49507.Mrg49507_STATE_SIZE + 8])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+41 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        mrg.setstate([tuple(i+51 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)), 3])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 3
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+51 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        mrg.setstate(([i+61 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)], TestMrg49507.Mrg49507_STATE_SIZE + 8))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 8
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+61 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        mrg.setstate(tuple(i+11 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)))  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+11 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

        mrg.setstate([i+21 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)])  # type: ignore
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._index == 0
        assert mrg.gauss_next is None  # type: ignore
        assert mrg._state == [i+21 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore
            _state[TestMrg49507.Mrg49507_STATE_SIZE - 2] = -1
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore
            _state[TestMrg49507.Mrg49507_STATE_SIZE - 3] = 0.321
            mrg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMrg49507.Mrg49507_STATE_SIZE)]  # type: ignore
            _state[TestMrg49507.Mrg49507_STATE_SIZE - 5] = {1, 2}
            mrg.setstate(_state)  # type: ignore
