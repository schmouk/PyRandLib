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

from PyRandLib.lfib116 import LFib116


#=============================================================================
class TestLFib116:
    """Tests class LFib116.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')
    LFib116_STATE_SIZE = 55

    #-------------------------------------------------------------------------
    def test_class(self):
        assert LFib116._NORMALIZE == 1.0 / (1 << 64)
        assert LFib116._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lfib = LFib116()
        assert lfib._STATE_SIZE == TestLFib116.LFib116_STATE_SIZE
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lfib = LFib116(1)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 4] == 0x71bb54d8d101b5b9
        assert lfib._state[14] == 0x6f9b6dae6f4c57a8
        assert lfib._state[24] == 0x497305c5d1aab99f
        assert lfib._state[34] == 0x40d6824e2ef3fc17
        assert lfib._state[44] == 0xde70d1019fc66081
        assert lfib._state[54] == 0x64c70b0b0c5b4a8f

        lfib = LFib116(-2)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 1] == 0xba56949915dcf9e9
        assert lfib._state[11] == 0xf79e3f6d8cc3172a
        assert lfib._state[21] == 0x95439471158019f4
        assert lfib._state[31] == 0x5575497b9a16aed3
        assert lfib._state[41] == 0x19750724928a9c3d
        assert lfib._state[51] == 0xfd2b90429b71400b

        lfib = LFib116(0x0123_4567_89ab_cdef)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0xa2d419334c4667ec
        assert lfib._state[13] == 0x97f6c69811cfb13b
        assert lfib._state[23] == 0xf7e9ff7484731d95
        assert lfib._state[33] == 0xa3c27a0df00dbde8
        assert lfib._state[43] == 0x374ca94be4ab03ac
        assert lfib._state[53] == 0x597bee355c27a849

        lfib = LFib116(-8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0x637c87187035ea06
        assert lfib._state[13] == 0xfbe6cd715ff52a4a
        assert lfib._state[23] == 0x2b47cdf0d48354fb
        assert lfib._state[33] == 0x68489cc40e3b45a7
        assert lfib._state[43] == 0x081d1c195787bcaa
        assert lfib._state[53] == 0xdfad412cf84777b3

        lfib = LFib116(8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0xaf6aa8f43ebb8659
        assert lfib._state[13] == 0x39390f80db89e31d
        assert lfib._state[23] == 0x3e2bc8837ce7ec22
        assert lfib._state[33] == 0xd2c9c36a8585312d
        assert lfib._state[43] == 0x4ab4eb00216eb318
        assert lfib._state[53] == 0x4048712b5ed9d636

        lfib = LFib116(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 0] == 0xf75f04cbb5a1a1dd
        assert lfib._state[10] == 0x71da8c61bc0cfda9
        assert lfib._state[20] == 0xed6e859bfa5e8dcc
        assert lfib._state[30] == 0xd1de816e066fa972
        assert lfib._state[40] == 0x5353e264bb834579
        assert lfib._state[50] == 0x5ba1c1d335e210df

    #-------------------------------------------------------------------------
    def test_init_float(self):
        lfib = LFib116(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0x77714db9e870d702
        assert lfib._state[13] == 0xee8fd4bfccca5ee3
        assert lfib._state[23] == 0x57988e812351fc14
        assert lfib._state[33] == 0xd394e8454bdb01ba
        assert lfib._state[43] == 0x6d59ad10fc02d912
        assert lfib._state[53] == 0x2a2852b20445bdd9

        lfib = LFib116(1.0)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

        with pytest.raises(ValueError):
            lfib = LFib116(-0.0001)
        with pytest.raises(ValueError):
            lfib = LFib116(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lfib = LFib116(tuple(i for i in range(TestLFib116.LFib116_STATE_SIZE)))  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                lfib = LFib116(list(i+10 for i in range(TestLFib116.LFib116_STATE_SIZE)))  # type: ignore
        else:
            lfib = LFib116(list(i+10 for i in range(TestLFib116.LFib116_STATE_SIZE)))  # type: ignore
            assert lfib._index == 0
            assert lfib.gauss_next is None  # type: ignore
            assert lfib._state == list(i+10 for i in range(TestLFib116.LFib116_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            lfib = LFib116((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib116((i for i in range(TestLFib116.LFib116_STATE_SIZE+1)))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib116([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib116([i for i in range(TestLFib116.LFib116_STATE_SIZE+1)])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib116(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lfib = LFib116(0x0123_4567_89ab_cdef)
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0xa2d419334c4667ec
        assert lfib._state[13] == 0x97f6c69811cfb13b
        assert lfib._state[23] == 0xf7e9ff7484731d95
        assert lfib._state[33] == 0xa3c27a0df00dbde8
        assert lfib._state[43] == 0x374ca94be4ab03ac
        assert lfib._state[53] == 0x597bee355c27a849

        for v in [0x5ed07fdb39cacf94, 0x5b95dda2595d5fdb, 0xd353313c897b8aa6, 0x9a76e5c13ef92ce2, 0x42e3075999073f4b]:
            assert lfib.next() == v

        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 4] == 0x42e3075999073f4b
        assert lfib._state[14] == 0x380e8b5c685039cf
        assert lfib._state[24] == 0x5e4d770f93e9e90a
        assert lfib._state[34] == 0xf7a2cc8df2b2c4f6
        assert lfib._state[44] == 0xa659ac05d6767b6f
        assert lfib._state[54] == 0xfadc7d62c4f8c2f9

    #-------------------------------------------------------------------------
    def test_seed(self):
        lfib = LFib116()
        
        lfib.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 0] == 0xf75f04cbb5a1a1dd
        assert lfib._state[10] == 0x71da8c61bc0cfda9
        assert lfib._state[20] == 0xed6e859bfa5e8dcc
        assert lfib._state[30] == 0xd1de816e066fa972
        assert lfib._state[40] == 0x5353e264bb834579
        assert lfib._state[50] == 0x5ba1c1d335e210df

        lfib.seed(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 3] == 0x77714db9e870d702
        assert lfib._state[13] == 0xee8fd4bfccca5ee3
        assert lfib._state[23] == 0x57988e812351fc14
        assert lfib._state[33] == 0xd394e8454bdb01ba
        assert lfib._state[43] == 0x6d59ad10fc02d912
        assert lfib._state[53] == 0x2a2852b20445bdd9

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
        lfib = LFib116()

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

        lfib.setstate((tuple(i+31 for i in range(TestLFib116.LFib116_STATE_SIZE)), 3))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+31 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        lfib.setstate([[i+41 for i in range(TestLFib116.LFib116_STATE_SIZE)], TestLFib116.LFib116_STATE_SIZE+5])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+41 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        lfib.setstate([tuple(i+51 for i in range(TestLFib116.LFib116_STATE_SIZE)), 3])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+51 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        lfib.setstate(([i+61 for i in range(TestLFib116.LFib116_STATE_SIZE)], TestLFib116.LFib116_STATE_SIZE+11))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 11
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+61 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        lfib.setstate(tuple(i+11 for i in range(TestLFib116.LFib116_STATE_SIZE)))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+11 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

        lfib.setstate([i+21 for i in range(TestLFib116.LFib116_STATE_SIZE)])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+21 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore
            _state[15] = -1
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore
            _state[12] = 0.321
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib116.LFib116_STATE_SIZE)]  # type: ignore
            _state[12] = {1, 2}
            lfib.setstate(_state)  # type: ignore
