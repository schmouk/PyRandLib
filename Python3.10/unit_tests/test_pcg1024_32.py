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

from PyRandLib.pcg1024_32 import Pcg1024_32


#=============================================================================
class TestPcg1024_32:
    """Tests class Pcg1024_32.
    """
    
    Pcg1024_32_EXTENDED_STATE_SIZE = 1024

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Pcg1024_32._NORMALIZE == 1.0 / (1 << 32)
        assert Pcg1024_32._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        pcg = Pcg1024_32()
        assert pcg._EXTENDED_STATE_SIZE == TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE
        assert len(pcg._extendedState) == TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState != 0
        assert all(isinstance(s, int) for s in pcg._extendedState)
        assert all(0 <= s < (1 << 32) for s in pcg._extendedState)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        pcg = Pcg1024_32(1)
        assert pcg._state == 1
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   1] == 0xbeeb8da1
        assert pcg._extendedState[ 171] == 0x6c5cc4ca
        assert pcg._extendedState[ 341] == 0x299c7163
        assert pcg._extendedState[ 511] == 0x619b42a2
        assert pcg._extendedState[ 681] == 0x30119338
        assert pcg._extendedState[ 851] == 0x06d5c6fe
        assert pcg._extendedState[1021] == 0xa4bcae83

        pcg = Pcg1024_32(-2)
        assert pcg._state == 0xffff_ffff_ffff_fffe
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   2] == 0xd0d5127a
        assert pcg._extendedState[ 172] == 0x107b5555
        assert pcg._extendedState[ 342] == 0x50553132
        assert pcg._extendedState[ 512] == 0xaf98cf4a
        assert pcg._extendedState[ 682] == 0x6f84b49b
        assert pcg._extendedState[ 852] == 0x38fd4a1f
        assert pcg._extendedState[1022] == 0xaee1bb4c

        pcg = Pcg1024_32(0x0123_4567_89ab_cdef)
        assert pcg._state == 0x0123_4567_89ab_cdef
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   3] == 0xa2d41933
        assert pcg._extendedState[ 173] == 0x3ac4288a
        assert pcg._extendedState[ 343] == 0x5fabd717
        assert pcg._extendedState[ 513] == 0xbab3def7
        assert pcg._extendedState[ 683] == 0xb6665fdc
        assert pcg._extendedState[ 853] == 0x407040cf
        assert pcg._extendedState[1023] == 0x1a8aec91

        pcg = Pcg1024_32(-8_870_000_000_000_000_000)
        assert pcg._state == 0x84e7_6dfe_ca49_0000
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   0] == 0x48bbc5b8
        assert pcg._extendedState[ 170] == 0xfb57d0fb
        assert pcg._extendedState[ 340] == 0x5306c566
        assert pcg._extendedState[ 510] == 0x99371619
        assert pcg._extendedState[ 680] == 0x4820d8be
        assert pcg._extendedState[ 850] == 0x80274781
        assert pcg._extendedState[1020] == 0xa69891d2

        pcg = Pcg1024_32(8_870_000_000_000_000_000)
        assert pcg._state == 0x7b18_9201_35b7_0000
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   0] == 0xeede014d
        assert pcg._extendedState[ 170] == 0xaf64f516
        assert pcg._extendedState[ 340] == 0xe53c8982
        assert pcg._extendedState[ 510] == 0xd27c5157
        assert pcg._extendedState[ 680] == 0x48ede633
        assert pcg._extendedState[ 850] == 0x19078a53
        assert pcg._extendedState[1020] == 0x138889f7

        pcg = Pcg1024_32(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg._state == 0xffff_ffff_ffff_fffd
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   1] == 0xec779c36
        assert pcg._extendedState[ 171] == 0x0ae1d8ad
        assert pcg._extendedState[ 341] == 0x9e0740e7
        assert pcg._extendedState[ 511] == 0x5d88abb1
        assert pcg._extendedState[ 681] == 0x32e7dd3a
        assert pcg._extendedState[ 851] == 0x0eadef97
        assert pcg._extendedState[1021] == 0x86e22c5c

    #-------------------------------------------------------------------------
    def test_init_float(self):
        pcg = Pcg1024_32(0.357)
        assert pcg._state == 0x5b64_5a1c_ac08_3000
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   0] == 0x5fee464f
        assert pcg._extendedState[ 170] == 0x2084fa3f
        assert pcg._extendedState[ 340] == 0x489eef92
        assert pcg._extendedState[ 510] == 0xd233535b
        assert pcg._extendedState[ 680] == 0x6f6dd894
        assert pcg._extendedState[ 850] == 0x515faa34
        assert pcg._extendedState[1020] == 0xff1a726d

        pcg = Pcg1024_32(1.0)
        assert pcg._state == int(1.0 * 0xffff_ffff_ffff_ffff)
        assert pcg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in pcg._extendedState)
        assert pcg._state != 0
        assert all(0 <= s < (1 << 32) for s in pcg._extendedState)  # type: ignore

        with pytest.raises(ValueError):
            pcg = Pcg1024_32(-0.0001)
        with pytest.raises(ValueError):
            pcg = Pcg1024_32(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        pcg = Pcg1024_32((tuple(i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3))  # type: ignore
        assert pcg._state == 3
        assert all(s == t for s, t in zip(pcg._extendedState, (i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))))
        
        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            pcg = Pcg1024_32((list(i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3))  # type: ignore
            assert pcg._state == 3
            assert all(s == t for s, t in zip(pcg._extendedState, (i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))))
        
        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            pcg = Pcg1024_32((list(i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3))  # type: ignore
            assert pcg._state == 3
            assert all(s == t for s, t in zip(pcg._extendedState, (i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))))

        with pytest.raises(TypeError):
            # due to unhashable lists bug in Python 3.10
            pcg = Pcg1024_32([list(i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3])  # type: ignore
            assert pcg._state == 3
            assert all(s == t for s, t in zip(pcg._extendedState, (i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))))

        with pytest.raises(ValueError):
            pcg = Pcg1024_32(((1, 2, 3), 1))  # type: ignore

        extended_state = tuple(i if i != 15 else -1 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))
        with pytest.raises(ValueError):
            pcg = Pcg1024_32((extended_state, 5))  # type: ignore

        extended_state = tuple(i if i != 150 else 0.789 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))
        with pytest.raises(ValueError):
            pcg = Pcg1024_32((extended_state, 5))  # type: ignore

        extended_state = tuple(i if i != 150 else set() for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE))
        with pytest.raises(TypeError):
            # TypeError here due to unhashable set in Python 3.10
            pcg = Pcg1024_32((extended_state, 5))  # type: ignore

        with pytest.raises(TypeError):
            pcg = Pcg1024_32(tuple(i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32(list(i+10 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg1024_32(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        pcg = Pcg1024_32(0x0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x0123456789abcdef
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   3] == 0xa2d41933
        assert pcg._extendedState[ 173] == 0x3ac4288a
        assert pcg._extendedState[ 343] == 0x5fabd717
        assert pcg._extendedState[ 513] == 0xbab3def7
        assert pcg._extendedState[ 683] == 0xb6665fdc
        assert pcg._extendedState[ 853] == 0x407040cf
        assert pcg._extendedState[1023] == 0x1a8aec91

        for v in [0x57207a74, 0x77abc3ae, 0xafe24cef, 0xbac4f59f, 0x5b7e3bd4]:
            assert pcg.next() == v

        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xc60c9ae76aeb1026
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[ 88] == 0x6f42e684
        assert pcg._extendedState[258] == 0xce160356
        assert pcg._extendedState[428] == 0x055754b9
        assert pcg._extendedState[598] == 0xc4ecf79a
        assert pcg._extendedState[768] == 0xe7c3ca1e
        assert pcg._extendedState[938] == 0xfe7f5216

        pcg = Pcg1024_32(0x0123_4567_89ab_cdef)
        pcg._state &= 0xffff_ffff_0000_0000
        assert pcg.next() == 0x45a0cf80

    #-------------------------------------------------------------------------
    def test_seed(self):
        pcg = Pcg1024_32()
        
        pcg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg._state == 0xffff_ffff_ffff_fffd
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   1] == 0xec779c36
        assert pcg._extendedState[ 171] == 0x0ae1d8ad
        assert pcg._extendedState[ 341] == 0x9e0740e7
        assert pcg._extendedState[ 511] == 0x5d88abb1
        assert pcg._extendedState[ 681] == 0x32e7dd3a
        assert pcg._extendedState[ 851] == 0x0eadef97
        assert pcg._extendedState[1021] == 0x86e22c5c

        pcg.seed(0.357)
        assert pcg._state == int(0.357 * 0xffff_ffff_ffff_ffff)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState[   0] == 0x5fee464f
        assert pcg._extendedState[ 170] == 0x2084fa3f
        assert pcg._extendedState[ 340] == 0x489eef92
        assert pcg._extendedState[ 510] == 0xd233535b
        assert pcg._extendedState[ 680] == 0x6f6dd894
        assert pcg._extendedState[ 850] == 0x515faa34
        assert pcg._extendedState[1020] == 0xff1a726d

        with pytest.raises(ValueError):
            pcg.seed(-0.0001)
        with pytest.raises(ValueError):
            pcg.seed(1.001)

        pcg.seed()
        assert 0 <= pcg._state < (1 << 64)
        assert pcg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in pcg._extendedState)
        assert all(0 <= s < (1 << 32) for s in pcg._extendedState)  # type: ignore

        with pytest.raises(TypeError):
            pcg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_getstate(self):
        pcg = Pcg1024_32()
        pcg_state = pcg.getstate()
        assert isinstance(pcg_state, tuple)
        assert isinstance(pcg_state[0], list)
        assert isinstance(pcg_state[1], int)  # type: ignore
        assert pcg_state[1] >= 0  # type: ignore 
        assert len(pcg_state) == 2
        assert len(pcg_state[0]) == Pcg1024_32._EXTENDED_STATE_SIZE
        assert pcg_state[0] == pcg._extendedState
        assert pcg_state[1] == pcg._state


    #-------------------------------------------------------------------------
    def test_setstate(self):
        pcg = Pcg1024_32()

        pcg.setstate()
        assert 0 <= pcg._state < (1 << 64)
        assert pcg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in pcg._extendedState)
        assert all(0 < s < (1 << 64) for s in pcg._extendedState)  # type: ignore
    
        with pytest.raises(TypeError):
            pcg.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            pcg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            pcg.setstate("123")  # type: ignore

        pcg.setstate((tuple(i+31 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3))  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 3
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState == [i+31 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore

        pcg.setstate([[i+41 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)], TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE + 8])  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 8 + TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState == [i+41 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore

        pcg.setstate([tuple(i+51 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)), 3])  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 3
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState == [i+51 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore

        pcg.setstate(([i+61 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)], TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE + 8))  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 8 + TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._extendedState == [i+61 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore

        with pytest.raises(ValueError):
            pcg.setstate(([TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE-i-10 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)], 11))
        with pytest.raises(ValueError):
            pcg.setstate(([i for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)], -11))

        with pytest.raises(TypeError):
            pcg.setstate(tuple(i+11 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)))  # type: ignore

        with pytest.raises(TypeError):
            pcg.setstate([i+21 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)])  # type: ignore

        with pytest.raises(TypeError):
            pcg.setstate([1, 2])
        with pytest.raises(TypeError):
            pcg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(TypeError):
            _state = [i+1 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore
            _state[TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE - 2] = -1
            pcg.setstate(_state)  # type: ignore
        with pytest.raises(TypeError):
            _state = [i+1 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore
            _state[TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE - 3] = 0.321
            pcg.setstate(_state)  # type: ignore
        with pytest.raises(TypeError):
            _state = [i+1 for i in range(TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE)]  # type: ignore
            _state[TestPcg1024_32.Pcg1024_32_EXTENDED_STATE_SIZE - 5] = {1, 2}
            pcg.setstate(_state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_advancetable(self):
        pcg = Pcg1024_32(0)
        # notice: the next two lines force the two branching of method '_advancetable()' 
        pcg._extendedState = [i for i in range(Pcg1024_32._EXTENDED_STATE_SIZE)]
        pcg._extendedState[1] = 0
        pcg._advancetable()
        for i, v in {0: 0x2, 204: 0x2cb62d6a, 408: 0x4b67bfa9, 612: 0x4a72c999, 816: 0xe99bb689, 1020: 0x75598ba}.items():
            assert pcg._extendedState[i] == v

    #-------------------------------------------------------------------------
    def test_invxrs(self):
        pcg = Pcg1024_32()
        
        assert pcg._invxrs(0x00001331, 32, 4) == 0x00001210
        assert pcg._invxrs(0x5124120d, 32, 4) == 0x5462311c
        assert pcg._invxrs(0xa24810e9, 32, 4) == 0xa8c455b2
        assert pcg._invxrs(0xf36c0fc5, 32, 4) == 0xfca66950
        
        assert pcg._invxrs(0x00001331, 32, 19) == 0x00001331
        assert pcg._invxrs(0x5124120d, 32, 19) == 0x51241829
        assert pcg._invxrs(0xa24810e9, 32, 19) == 0xa24804a0
        assert pcg._invxrs(0xf36c0fc5, 32, 19) == 0xf36c11a8
