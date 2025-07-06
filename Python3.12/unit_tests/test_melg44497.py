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

from PyRandLib.melg44497 import Melg44497


#=============================================================================
class TestMelg44497:
    """Tests class Melg44497.
    """
    
    Melg44497_STATE_SIZE = 696

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Melg44497._NORMALIZE == 1.0 / (1 << 64)
        assert Melg44497._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        melg = Melg44497()
        assert melg._STATE_SIZE == TestMelg44497.Melg44497_STATE_SIZE
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        melg = Melg44497(1)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  1] == 0xbeeb8da1658eec67
        assert melg._state[140] == 0xa6fefb55c353a1ea
        assert melg._state[279] == 0xb762715eb23cd3d7
        assert melg._state[418] == 0x041fe2b35f3a75fd
        assert melg._state[557] == 0x6698b211b671b46f
        assert melg._state[695] == 0x6bbc0a80a7487e21

        melg = Melg44497(-2)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[137] == 0x1f4aea7af6513705
        assert melg._state[276] == 0x74345ae408f3d48a
        assert melg._state[415] == 0x9f1b299ea71cb462
        assert melg._state[554] == 0x803ab216bda954f7
        assert melg._state[693] == 0x0a8f137c062ac922
        assert melg._state[695] == 0x79a6b61c50037b24

        melg = Melg44497(0x0123_4567_89ab_cdef)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 61] == 0xc79841f4a60c9b64
        assert melg._state[123] == 0x49a17debdb062ce4
        assert melg._state[185] == 0xb568f29ddb496c83
        assert melg._state[247] == 0x7e07ab8606a92cfc
        assert melg._state[309] == 0xc4c23a6e338d6a6e
        assert melg._state[311] == 0x8c3b5029dac57ba8

        melg = Melg44497(-8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 30] == 0x23ef9d9e302b0672
        assert melg._state[169] == 0x5094e18722769c12
        assert melg._state[308] == 0x8bab6be09cbdcc0e
        assert melg._state[447] == 0x4dd2b81fbbd6db3a
        assert melg._state[586] == 0x1dcf6ae042f2df4e
        assert melg._state[695] == 0x9598d0afcf36edcf

        melg = Melg44497(8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[109] == 0x8d72a9d4ef692c9f
        assert melg._state[248] == 0xd0c40d7c017a67a9
        assert melg._state[387] == 0x4450c907cea976ad
        assert melg._state[526] == 0x05f9fc1655c71da5
        assert melg._state[665] == 0xd303031f8d6093e4
        assert melg._state[695] == 0x76c82ac41f7c0e44

        melg = Melg44497(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 14] == 0xe189cea064a6f2ec
        assert melg._state[153] == 0xd0ad13dad13c2a5e
        assert melg._state[292] == 0x0bbb6b2e84548ecd
        assert melg._state[431] == 0xbc6657fe06f2e294
        assert melg._state[570] == 0xaf4a5e323cd715c5
        assert melg._state[695] == 0x0986697ff828bfdf

    #-------------------------------------------------------------------------
    def test_init_float(self):
        melg = Melg44497(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  0] == 0x5fee464f36fc42c3
        assert melg._state[139] == 0xd823f5cb86381fa6
        assert melg._state[278] == 0x65be0e01a9329abd
        assert melg._state[417] == 0x1ba644087d1e8937
        assert melg._state[556] == 0x3468d12e0ed446b8
        assert melg._state[695] == 0xa046f7cca1c0b35c

        melg = Melg44497(1.0)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

        with pytest.raises(ValueError):
            melg = Melg44497(-0.0001)
        with pytest.raises(ValueError):
            melg = Melg44497(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        melg = Melg44497(tuple(i for i in range(TestMelg44497.Melg44497_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg = Melg44497(list(i+10 for i in range(TestMelg44497.Melg44497_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == list(i+10 for i in range(TestMelg44497.Melg44497_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            melg = Melg44497((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg44497((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg44497([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg44497([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg44497(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        melg = Melg44497(0x0123_4567_89ab_cdef)
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 61] == 0xc79841f4a60c9b64
        assert melg._state[123] == 0x49a17debdb062ce4
        assert melg._state[185] == 0xb568f29ddb496c83
        assert melg._state[247] == 0x7e07ab8606a92cfc
        assert melg._state[309] == 0xc4c23a6e338d6a6e
        assert melg._state[311] == 0x8c3b5029dac57ba8

        for v in [0x9907105396f37998, 0x580d9d1d30bf41b9, 0x4bdba4870acb0784, 0x161ada0c406c26c8, 0x345eb35a58ba5a7e]:
            assert melg.next() == v

        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 5
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[131] == 0x43856098c604fda6
        assert melg._state[270] == 0x7c33528010383106
        assert melg._state[409] == 0xc1432f2d5a7ca12e
        assert melg._state[548] == 0x5b1cb64a20b14d85
        assert melg._state[687] == 0xe5822e6f04b94654
        assert melg._state[695] == 0x48bcfda3458883ef

    #-------------------------------------------------------------------------
    def test_seed(self):
        melg = Melg44497()
        
        melg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 14] == 0xe189cea064a6f2ec
        assert melg._state[153] == 0xd0ad13dad13c2a5e
        assert melg._state[292] == 0x0bbb6b2e84548ecd
        assert melg._state[431] == 0xbc6657fe06f2e294
        assert melg._state[570] == 0xaf4a5e323cd715c5
        assert melg._state[695] == 0x0986697ff828bfdf

        melg.seed(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  0] == 0x5fee464f36fc42c3
        assert melg._state[139] == 0xd823f5cb86381fa6
        assert melg._state[278] == 0x65be0e01a9329abd
        assert melg._state[417] == 0x1ba644087d1e8937
        assert melg._state[556] == 0x3468d12e0ed446b8
        assert melg._state[695] == 0xa046f7cca1c0b35c

        with pytest.raises(ValueError):
            melg.seed(-0.0001)
        with pytest.raises(ValueError):
            melg.seed(1.001)

        melg.seed()
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

        with pytest.raises(TypeError):
            melg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            melg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            melg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            melg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            melg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        melg = Melg44497()

        melg.setstate()
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore
    
        with pytest.raises(TypeError):
            melg.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            melg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            melg.setstate("123")  # type: ignore

        melg.setstate((tuple(i+31 for i in range(TestMelg44497.Melg44497_STATE_SIZE)), 3))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+31 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg.setstate([[i+41 for i in range(TestMelg44497.Melg44497_STATE_SIZE)], TestMelg44497.Melg44497_STATE_SIZE + 8])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+41 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg.setstate([tuple(i+51 for i in range(TestMelg44497.Melg44497_STATE_SIZE)), 3])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+51 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg.setstate(([i+61 for i in range(TestMelg44497.Melg44497_STATE_SIZE)], TestMelg44497.Melg44497_STATE_SIZE + 8))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+61 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg.setstate(tuple(i+11 for i in range(TestMelg44497.Melg44497_STATE_SIZE)))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+11 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        melg.setstate([i+21 for i in range(TestMelg44497.Melg44497_STATE_SIZE)])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+21 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore

        with pytest.raises(TypeError):
            melg.setstate([1, 2])
        with pytest.raises(TypeError):
            melg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            melg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            melg.setstate([11, 12, 13.1, 14])  # type: ignore
        _state: list[Any]
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore
            _state[TestMelg44497.Melg44497_STATE_SIZE - 2] = -1
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore
            _state[TestMelg44497.Melg44497_STATE_SIZE - 3] = 0.321
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg44497.Melg44497_STATE_SIZE)]  # type: ignore
            _state[TestMelg44497.Melg44497_STATE_SIZE - 5] = {1, 2}
            melg.setstate(_state)  # type: ignore
