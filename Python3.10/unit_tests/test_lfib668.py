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

from PyRandLib.lfib668 import LFib668


#=============================================================================
class TestLFib668:
    """Tests class LFib668.
    """
    
    LFib668_STATE_SIZE = 607

    #-------------------------------------------------------------------------
    def test_class(self):
        assert LFib668._NORMALIZE == 1.0 / (1 << 64)
        assert LFib668._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lfib = LFib668()
        assert lfib._STATE_SIZE == TestLFib668.LFib668_STATE_SIZE
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lfib = LFib668(1)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 34] == 0x40d6824e2ef3fc17
        assert lfib._state[135] == 0x0bf99fe6cbdde2d6
        assert lfib._state[236] == 0x2d1d63dad4a646be
        assert lfib._state[337] == 0xf021a06c3994c719
        assert lfib._state[438] == 0xbc82fc84cf39a3d5
        assert lfib._state[539] == 0x16f44cde26568725

        lfib = LFib668(-2)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 31] == 0x5575497b9a16aed3
        assert lfib._state[132] == 0x85655d04487d0761
        assert lfib._state[233] == 0xe09472b54f8e7fbb
        assert lfib._state[334] == 0xaae39a74a86ffb0b
        assert lfib._state[435] == 0xccea4a74623415b8
        assert lfib._state[536] == 0xab9d474e0f54e203

        lfib = LFib668(0x0123_4567_89ab_cdef)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  4] == 0x01404ce914938008
        assert lfib._state[105] == 0xe7cf4ae1ccc855ee
        assert lfib._state[206] == 0xccf850c57a705cd6
        assert lfib._state[307] == 0x3822f2eb098d4c15
        assert lfib._state[408] == 0xb1147de017060044
        assert lfib._state[509] == 0xd0171502d4408191

        lfib = LFib668(-8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 55] == 0x0ae6185bdfe16a2b
        assert lfib._state[156] == 0x906b0e9a2ebe39f4
        assert lfib._state[257] == 0xa1f04b27bd2c2bc1
        assert lfib._state[358] == 0xa19853dd7cfa899c
        assert lfib._state[459] == 0x6ad5898368d6d393
        assert lfib._state[560] == 0xc677f2594b231d78

        lfib = LFib668(8_870_000_000_000_000_000)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 11] == 0xff42f03c6e8cba89
        assert lfib._state[112] == 0x836c808fba21e190
        assert lfib._state[213] == 0xdba3cc01687a3ed9
        assert lfib._state[314] == 0xb771fcfd28ab59fb
        assert lfib._state[415] == 0x18996ed40fb43cc1
        assert lfib._state[516] == 0xf734350d707383d9

        lfib = LFib668(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 31] == 0xb83e988fc0cd7c45
        assert lfib._state[132] == 0x165be770d0e2db3d
        assert lfib._state[233] == 0x116482f314d44886
        assert lfib._state[334] == 0x8136d7f63fddb8c1
        assert lfib._state[435] == 0x0672cbd2265d70ff
        assert lfib._state[536] == 0x07cc37398fdd730d

    #-------------------------------------------------------------------------
    def test_init_float(self):
        lfib = LFib668(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 33] == 0xd394e8454bdb01ba
        assert lfib._state[134] == 0x5f2cb7df658e2b39
        assert lfib._state[235] == 0x6dc81aab3925d369
        assert lfib._state[336] == 0xa57b09f2d2d85743
        assert lfib._state[437] == 0x5c330aad92d95d4c
        assert lfib._state[538] == 0x842fc05b58add847

        lfib = LFib668(1.0)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in lfib._state)
        assert all(0 < s < (1 << 64) for s in lfib._state)  # type: ignore

        with pytest.raises(ValueError):
            lfib = LFib668(-0.0001)
        with pytest.raises(ValueError):
            lfib = LFib668(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lfib = LFib668(tuple(i for i in range(TestLFib668.LFib668_STATE_SIZE)))  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            # due to unhashalbe lists bug in Python 3.10
            lfib = LFib668(list(i+10 for i in range(TestLFib668.LFib668_STATE_SIZE)))  # type: ignore
            assert lfib._index == 0
            assert lfib.gauss_next is None  # type: ignore
            assert lfib._state == list(i+10 for i in range(TestLFib668.LFib668_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            lfib = LFib668((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib668((i for i in range(TestLFib668.LFib668_STATE_SIZE+1)))  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib668([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib668([i for i in range(TestLFib668.LFib668_STATE_SIZE+1)])  # type: ignore
        with pytest.raises(TypeError):
            lfib = LFib668(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lfib = LFib668(0x0123_4567_89ab_cdef)
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[  4] == 0x01404ce914938008
        assert lfib._state[105] == 0xe7cf4ae1ccc855ee
        assert lfib._state[206] == 0xccf850c57a705cd6
        assert lfib._state[307] == 0x3822f2eb098d4c15
        assert lfib._state[408] == 0xb1147de017060044
        assert lfib._state[509] == 0xd0171502d4408191

        for v in [0x66d94c71cf6c9734, 0x31e154b04f01d4a6, 0x9d1e21a3cf797025, 0x96b803c37236482b, 0x9b2e73147b19ff21]:
            assert lfib.next() == v

        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 38] == 0xbfd57627fe350937
        assert lfib._state[139] == 0x4e68e26636092c9a
        assert lfib._state[240] == 0x443ca02ab33c4c1f
        assert lfib._state[341] == 0x309546ff7bfd72fb
        assert lfib._state[442] == 0xaab04d23fc88a152
        assert lfib._state[543] == 0x0891f7d38d26c8fb

    #-------------------------------------------------------------------------
    def test_seed(self):
        lfib = LFib668()
        
        lfib.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 31] == 0xb83e988fc0cd7c45
        assert lfib._state[132] == 0x165be770d0e2db3d
        assert lfib._state[233] == 0x116482f314d44886
        assert lfib._state[334] == 0x8136d7f63fddb8c1
        assert lfib._state[435] == 0x0672cbd2265d70ff
        assert lfib._state[536] == 0x07cc37398fdd730d

        lfib.seed(0.357)
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state[ 33] == 0xd394e8454bdb01ba
        assert lfib._state[134] == 0x5f2cb7df658e2b39
        assert lfib._state[235] == 0x6dc81aab3925d369
        assert lfib._state[336] == 0xa57b09f2d2d85743
        assert lfib._state[437] == 0x5c330aad92d95d4c
        assert lfib._state[538] == 0x842fc05b58add847

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
        lfib = LFib668()

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

        lfib.setstate((tuple(i+31 for i in range(TestLFib668.LFib668_STATE_SIZE)), 3))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+31 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        lfib.setstate([[i+41 for i in range(TestLFib668.LFib668_STATE_SIZE)], TestLFib668.LFib668_STATE_SIZE+5])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 5
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+41 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        lfib.setstate([tuple(i+51 for i in range(TestLFib668.LFib668_STATE_SIZE)), 3])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 3
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+51 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        lfib.setstate(([i+61 for i in range(TestLFib668.LFib668_STATE_SIZE)], TestLFib668.LFib668_STATE_SIZE+11))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 11
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+61 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        lfib.setstate(tuple(i+11 for i in range(TestLFib668.LFib668_STATE_SIZE)))  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+11 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

        lfib.setstate([i+21 for i in range(TestLFib668.LFib668_STATE_SIZE)])  # type: ignore
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._index == 0
        assert lfib.gauss_next is None  # type: ignore
        assert lfib._state == [i+21 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore
            _state[15] = -1
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore
            _state[12] = 0.321
            lfib.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestLFib668.LFib668_STATE_SIZE)]  # type: ignore
            _state[12] = {1, 2}
            lfib.setstate(_state)  # type: ignore
