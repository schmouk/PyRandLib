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

from PyRandLib.melg19937 import Melg19937


#=============================================================================
class TestMelg19937:
    """Tests class Melg19937.
    """
    
    Melg19937_STATE_SIZE = 312

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Melg19937._NORMALIZE == 1.0 / (1 << 64)
        assert Melg19937._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        melg = Melg19937()
        assert melg._STATE_SIZE == TestMelg19937.Melg19937_STATE_SIZE
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        melg = Melg19937(1)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  1] == 0xbeeb8da1658eec67
        assert melg._state[ 63] == 0x88b894e1401ed25b
        assert melg._state[125] == 0x32647003725b6ed3
        assert melg._state[187] == 0xeaeb4814b3a728d7
        assert melg._state[249] == 0x3e17e6dfc3cb0bac
        assert melg._state[311] == 0xe9316fe9c2c04c2d

        melg = Melg19937(-2)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 60] == 0xfaebc45a40c96857
        assert melg._state[122] == 0x8f1841b5ba07c168
        assert melg._state[184] == 0x0aa802900261ebcf
        assert melg._state[246] == 0xf9eb62c0b405ceef
        assert melg._state[308] == 0xabe17a9b9affd4c2
        assert melg._state[311] == 0xbc8964c3874e4207

        melg = Melg19937(0x0123_4567_89ab_cdef)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 61] == 0xc79841f4a60c9b64
        assert melg._state[123] == 0x49a17debdb062ce4
        assert melg._state[185] == 0xb568f29ddb496c83
        assert melg._state[247] == 0x7e07ab8606a92cfc
        assert melg._state[309] == 0xc4c23a6e338d6a6e
        assert melg._state[311] == 0x8c3b5029dac57ba8

        melg = Melg19937(-8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 58] == 0xe40640323ee3c568
        assert melg._state[120] == 0xaa478927b114ab8c
        assert melg._state[182] == 0xe331abee50258b0a
        assert melg._state[244] == 0xffaaf04c2b0d84e9
        assert melg._state[306] == 0xea019e7bb100fef9
        assert melg._state[311] == 0xe1b94c7c698e0d1d

        melg = Melg19937(8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  4] == 0xe1b0fb2c7e764cdb
        assert melg._state[ 66] == 0x170c62c362d3fc96
        assert melg._state[128] == 0xbf6832f228c09d7a
        assert melg._state[190] == 0xfae814b8b37adbd3
        assert melg._state[252] == 0x0d069f480330275a
        assert melg._state[311] == 0x396bcd270b364e2c

        melg = Melg19937(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 51] == 0x7915a8a138203cdb
        assert melg._state[113] == 0xdc4c3bc7f395318f
        assert melg._state[175] == 0x7a272b00b69cf47d
        assert melg._state[237] == 0x78f88cbf6920a5a7
        assert melg._state[299] == 0x68f0cee92ea416ea
        assert melg._state[311] == 0x01490dff1371e896

    #-------------------------------------------------------------------------
    def test_init_float(self):
        melg = Melg19937(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  0] == 0x5fee464f36fc42c3
        assert melg._state[ 62] == 0x847e1c96f63aadf2
        assert melg._state[124] == 0xa3e2c96ef9705f8a
        assert melg._state[186] == 0x6ab908c535def3ff
        assert melg._state[248] == 0x0d99e1061e0c196b
        assert melg._state[310] == 0x89bb9f67b51ff62a
        assert melg._state[311] == 0x02659929a25fa4dd

        melg = Melg19937(1.0)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

        with pytest.raises(ValueError):
            melg = Melg19937(-0.0001)
        with pytest.raises(ValueError):
            melg = Melg19937(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        melg = Melg19937(tuple(i for i in range(TestMelg19937.Melg19937_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg = Melg19937(list(i+10 for i in range(TestMelg19937.Melg19937_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == list(i+10 for i in range(TestMelg19937.Melg19937_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            melg = Melg19937((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg19937((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg19937([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg19937([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg19937(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        melg = Melg19937(0x0123_4567_89ab_cdef)
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 61] == 0xc79841f4a60c9b64
        assert melg._state[123] == 0x49a17debdb062ce4
        assert melg._state[185] == 0xb568f29ddb496c83
        assert melg._state[247] == 0x7e07ab8606a92cfc
        assert melg._state[309] == 0xc4c23a6e338d6a6e
        assert melg._state[311] == 0x8c3b5029dac57ba8

        for v in [0xe6fc8387bf0c4793, 0x1c14b3d27dd7fbd9, 0x3319dba9ee4fc6ae, 0x81f9e8038014de15, 0x8bf4406be63716de]:
            assert melg.next() == v

        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 5
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 30] == 0x09193ec65cf7a972
        assert melg._state[ 92] == 0xb2a8d8135941cab2
        assert melg._state[154] == 0x1dc7ebca191a4f9f
        assert melg._state[216] == 0x42ff9df57c595809
        assert melg._state[278] == 0xd049b13564d10022
        assert melg._state[311] == 0x221c86a9577b017c

    #-------------------------------------------------------------------------
    def test_seed(self):
        melg = Melg19937()
        
        melg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[ 51] == 0x7915a8a138203cdb
        assert melg._state[113] == 0xdc4c3bc7f395318f
        assert melg._state[175] == 0x7a272b00b69cf47d
        assert melg._state[237] == 0x78f88cbf6920a5a7
        assert melg._state[299] == 0x68f0cee92ea416ea
        assert melg._state[311] == 0x01490dff1371e896

        melg.seed(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[  0] == 0x5fee464f36fc42c3
        assert melg._state[ 62] == 0x847e1c96f63aadf2
        assert melg._state[124] == 0xa3e2c96ef9705f8a
        assert melg._state[186] == 0x6ab908c535def3ff
        assert melg._state[248] == 0x0d99e1061e0c196b
        assert melg._state[310] == 0x89bb9f67b51ff62a
        assert melg._state[311] == 0x02659929a25fa4dd

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
        melg = Melg19937()

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

        melg.setstate((tuple(i+31 for i in range(TestMelg19937.Melg19937_STATE_SIZE)), 3))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+31 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg.setstate([[i+41 for i in range(TestMelg19937.Melg19937_STATE_SIZE)], TestMelg19937.Melg19937_STATE_SIZE + 8])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+41 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg.setstate([tuple(i+51 for i in range(TestMelg19937.Melg19937_STATE_SIZE)), 3])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+51 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg.setstate(([i+61 for i in range(TestMelg19937.Melg19937_STATE_SIZE)], TestMelg19937.Melg19937_STATE_SIZE + 8))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+61 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg.setstate(tuple(i+11 for i in range(TestMelg19937.Melg19937_STATE_SIZE)))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+11 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

        melg.setstate([i+21 for i in range(TestMelg19937.Melg19937_STATE_SIZE)])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+21 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore
            _state[TestMelg19937.Melg19937_STATE_SIZE - 2] = -1
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore
            _state[TestMelg19937.Melg19937_STATE_SIZE - 3] = 0.321
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg19937.Melg19937_STATE_SIZE)]  # type: ignore
            _state[TestMelg19937.Melg19937_STATE_SIZE - 5] = {1, 2}
            melg.setstate(_state)  # type: ignore
