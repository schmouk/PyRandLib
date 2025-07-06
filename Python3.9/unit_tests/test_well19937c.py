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

from PyRandLib.well19937c import Well19937c


#=============================================================================
class TestWell19937c:
    """Tests class Well19937c.
    """
    
    Well19937c_STATE_SIZE = 624

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Well19937c._NORMALIZE == 1.0 / (1 << 32)
        assert Well19937c._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        wll = Well19937c()
        assert wll._STATE_SIZE == TestWell19937c.Well19937c_STATE_SIZE
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 32) for s in wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        wll = Well19937c(1)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[  1] == 0xbeeb8da1
        assert wll._state[104] == 0x764176e3
        assert wll._state[207] == 0x116a7537
        assert wll._state[310] == 0xafff2161
        assert wll._state[413] == 0x4cdddfb3
        assert wll._state[516] == 0xc9788c94
        assert wll._state[619] == 0x2a93b073

        wll = Well19937c(-2)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[106] == 0x4e2f3186
        assert wll._state[209] == 0x3175c25a
        assert wll._state[312] == 0x19880db1
        assert wll._state[415] == 0x9f1b299e
        assert wll._state[518] == 0x0537578d
        assert wll._state[621] == 0xf2fd44a7

        wll = Well19937c(0x0123_4567_89ab_cdef)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 87] == 0xaf9321d7
        assert wll._state[190] == 0x19f5a875
        assert wll._state[293] == 0xf2805263
        assert wll._state[396] == 0x98dd341e
        assert wll._state[499] == 0xe9512ec1
        assert wll._state[602] == 0x2736fee2

        wll = Well19937c(-8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 40] == 0xbad5b1a4
        assert wll._state[143] == 0xf06ea580
        assert wll._state[246] == 0x0fb469ce
        assert wll._state[349] == 0xcee933c0
        assert wll._state[452] == 0x2db9dbaf
        assert wll._state[555] == 0xcac8d27f

        wll = Well19937c(8_870_000_000_000_000_000)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 68] == 0x1870948e
        assert wll._state[171] == 0x417a54c5
        assert wll._state[274] == 0xad464210
        assert wll._state[377] == 0xb3c666a4
        assert wll._state[480] == 0x5ca8aae2
        assert wll._state[583] == 0xb6794803

        wll = Well19937c(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 57] == 0x06eb55fc
        assert wll._state[160] == 0xf5f8ddc6
        assert wll._state[263] == 0x79406d2f
        assert wll._state[366] == 0x92eefa95
        assert wll._state[469] == 0xba090bad
        assert wll._state[572] == 0x95f11813

    #-------------------------------------------------------------------------
    def test_init_float(self):
        wll = Well19937c(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[  0] == 0x5fee464f
        assert wll._state[103] == 0x1d890ddc
        assert wll._state[206] == 0x95c03c83
        assert wll._state[309] == 0x92964cbc
        assert wll._state[412] == 0xd24c1d7d
        assert wll._state[515] == 0x9993f3e8
        assert wll._state[618] == 0xeb7f4250

        wll = Well19937c(1.0)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in wll._state)
        assert all(0 <= s < (1 << 64) for s in wll._state)  # type: ignore

        with pytest.raises(ValueError):
            wll = Well19937c(-0.0001)
        with pytest.raises(ValueError):
            wll = Well19937c(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        wll = Well19937c(tuple(i for i in range(TestWell19937c.Well19937c_STATE_SIZE)))  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.9
            wll = Well19937c(list(i+10 for i in range(TestWell19937c.Well19937c_STATE_SIZE)))  # type: ignore
            assert wll._index == 0
            assert wll.gauss_next is None  # type: ignore
            assert wll._state == list(i+10 for i in range(TestWell19937c.Well19937c_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            wll = Well19937c((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well19937c((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            wll = Well19937c([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well19937c([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            wll = Well19937c(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        wll = Well19937c(0x0123_4567_89ab_cdef)
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll._state[ 87] == 0xaf9321d7
        assert wll._state[190] == 0x19f5a875
        assert wll._state[293] == 0xf2805263
        assert wll._state[396] == 0x98dd341e
        assert wll._state[499] == 0xe9512ec1
        assert wll._state[602] == 0x2736fee2

        for v in [0xec5c8d8b, 0x79358173, 0xe15b206b, 0x4a10e5e0, 0x3a0973cc]:
            assert wll.next() == v

        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 619
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 35] == 0x41a2ba70
        assert wll._state[138] == 0x42808a00
        assert wll._state[241] == 0x922a5840
        assert wll._state[344] == 0xfb76130a
        assert wll._state[447] == 0xb910bdc8
        assert wll._state[550] == 0xda35f666

        wll._index = 1
        wll.next()
        assert wll._index == 0

    #-------------------------------------------------------------------------
    def test_seed(self):
        wll = Well19937c()
        
        wll.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[ 57] == 0x06eb55fc
        assert wll._state[160] == 0xf5f8ddc6
        assert wll._state[263] == 0x79406d2f
        assert wll._state[366] == 0x92eefa95
        assert wll._state[469] == 0xba090bad
        assert wll._state[572] == 0x95f11813

        wll.seed(0.357)
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state[  0] == 0x5fee464f
        assert wll._state[103] == 0x1d890ddc
        assert wll._state[206] == 0x95c03c83
        assert wll._state[309] == 0x92964cbc
        assert wll._state[412] == 0xd24c1d7d
        assert wll._state[515] == 0x9993f3e8
        assert wll._state[618] == 0xeb7f4250

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
        wll = Well19937c()

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

        wll.setstate((tuple(i+31 for i in range(TestWell19937c.Well19937c_STATE_SIZE)), 3))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+31 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        wll.setstate([[i+41 for i in range(TestWell19937c.Well19937c_STATE_SIZE)], TestWell19937c.Well19937c_STATE_SIZE + 8])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+41 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        wll.setstate([tuple(i+51 for i in range(TestWell19937c.Well19937c_STATE_SIZE)), 3])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 3
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+51 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        wll.setstate(([i+61 for i in range(TestWell19937c.Well19937c_STATE_SIZE)], TestWell19937c.Well19937c_STATE_SIZE + 8))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 8
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+61 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        wll.setstate(tuple(i+11 for i in range(TestWell19937c.Well19937c_STATE_SIZE)))  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+11 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

        wll.setstate([i+21 for i in range(TestWell19937c.Well19937c_STATE_SIZE)])  # type: ignore
        assert wll.gauss_next is None  # type: ignore
        assert wll._index == 0
        assert wll.gauss_next is None  # type: ignore
        assert wll._state == [i+21 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore
            _state[TestWell19937c.Well19937c_STATE_SIZE - 2] = -1
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore
            _state[TestWell19937c.Well19937c_STATE_SIZE - 3] = 0.321
            wll.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestWell19937c.Well19937c_STATE_SIZE)]  # type: ignore
            _state[TestWell19937c.Well19937c_STATE_SIZE - 5] = {1, 2}
            wll.setstate(_state)  # type: ignore
