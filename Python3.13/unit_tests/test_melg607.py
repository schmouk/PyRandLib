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

from PyRandLib.melg607 import Melg607


#=============================================================================
class TestMelg607:
    """Tests class Melg607.
    """
    
    Melg607_STATE_SIZE = 10

    #-------------------------------------------------------------------------
    def test_class(self):
        assert Melg607._NORMALIZE == 1.0 / (1 << 64)
        assert Melg607._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        melg = Melg607()
        assert melg._STATE_SIZE == TestMelg607.Melg607_STATE_SIZE
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        melg = Melg607(1)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x910a2dec89025cc1
        assert melg._state[2] == 0xf893a2eefb32555e
        assert melg._state[4] == 0x71bb54d8d101b5b9
        assert melg._state[6] == 0xe099ec6cd7363ca5
        assert melg._state[8] == 0x491718de357e3da8
        assert melg._state[9] == 0xcb435c8e74616796

        melg = Melg607(-2)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0xf3203e9039f4a821
        assert melg._state[2] == 0xd0d5127a96e8d90d
        assert melg._state[4] == 0x7842841591543f1d
        assert melg._state[6] == 0xea909a92e113bf3c
        assert melg._state[8] == 0x24b37710c55c43d9
        assert melg._state[9] == 0x19fbbd62c13ae39f

        melg = Melg607(0x0123_4567_89ab_cdef)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x157a3807a48faa9d
        assert melg._state[2] == 0x2f90b72e996dccbe
        assert melg._state[4] == 0x01404ce914938008
        assert melg._state[6] == 0xb8fc5b1060708c05
        assert melg._state[8] == 0xf984db4ef14fde1b
        assert melg._state[9] == 0x2680d065cb73ece7

        melg = Melg607(-8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x48bbc5b84275f3ca
        assert melg._state[2] == 0x86ce19a135fba0de
        assert melg._state[4] == 0x2a03b9aff2bfd421
        assert melg._state[6] == 0x95d0c8e531644d42
        assert melg._state[8] == 0x2a6e10124e1efad4
        assert melg._state[9] == 0x5f29354ebb479e63

        melg = Melg607(8_870_000_000_000_000_000)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0xeede014d9a5a6108
        assert melg._state[2] == 0x4246cbb1a64bf70c
        assert melg._state[4] == 0xe1b0fb2c7e764cdb
        assert melg._state[6] == 0x1408795faf81b73d
        assert melg._state[8] == 0x13d184a1443e3dbe
        assert melg._state[9] == 0x04443a1051eede9a

        melg = Melg607(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0xf75f04cbb5a1a1dd
        assert melg._state[2] == 0xfed9eeb4936de39d
        assert melg._state[4] == 0x260ffb0260bbbe5f
        assert melg._state[6] == 0x7a5f67e38e997e3f
        assert melg._state[8] == 0x4f6d6a273422e220
        assert melg._state[9] == 0x56a7458a6eece57b

    #-------------------------------------------------------------------------
    def test_init_float(self):
        melg = Melg607(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x5fee464f36fc42c3
        assert melg._state[2] == 0xa985465a4a5fc644
        assert melg._state[4] == 0xa3aac457d81d552c
        assert melg._state[6] == 0x1c4d126a40f3f8a9
        assert melg._state[8] == 0x89b7be31ad4c739f
        assert melg._state[9] == 0xe8f9525bf6c56aef

        melg = Melg607(1.0)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert all(isinstance(s, int) for s in melg._state)
        assert all(0 < s < (1 << 64) for s in melg._state)  # type: ignore

        with pytest.raises(ValueError):
            melg = Melg607(-0.0001)
        with pytest.raises(ValueError):
            melg = Melg607(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        melg = Melg607(tuple(i for i in range(TestMelg607.Melg607_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg = Melg607(list(i+10 for i in range(TestMelg607.Melg607_STATE_SIZE)))  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == list(i+10 for i in range(TestMelg607.Melg607_STATE_SIZE))  # type: ignore

        with pytest.raises(TypeError):
            melg = Melg607((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg607((i for i in range(18)))  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg607([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg607([i for i in range(18)])  # type: ignore
        with pytest.raises(TypeError):
            melg = Melg607(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        melg = Melg607(0x0123_4567_89ab_cdef)
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x157a3807a48faa9d
        assert melg._state[2] == 0x2f90b72e996dccbe
        assert melg._state[4] == 0x01404ce914938008
        assert melg._state[6] == 0xb8fc5b1060708c05
        assert melg._state[8] == 0xf984db4ef14fde1b
        assert melg._state[9] == 0x2680d065cb73ece7

        for v in [0x6d1c8dcc2f39eb32, 0x2b3d47b953db5234, 0x4c5d559f75fbd847, 0x77acf1a2b79c185e, 0x758119c3447e5459]:
            assert melg.next() == v

        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 5
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0xb606e72be779ab16
        assert melg._state[2] == 0xcf05f78e1fd39065
        assert melg._state[4] == 0xa659e8df4fe6d459
        assert melg._state[6] == 0xb8fc5b1060708c05
        assert melg._state[8] == 0xf984db4ef14fde1b
        assert melg._state[9] == 0xa719a436712eacad

    #-------------------------------------------------------------------------
    def test_seed(self):
        melg = Melg607()
        
        melg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0xf75f04cbb5a1a1dd
        assert melg._state[2] == 0xfed9eeb4936de39d
        assert melg._state[4] == 0x260ffb0260bbbe5f
        assert melg._state[6] == 0x7a5f67e38e997e3f
        assert melg._state[8] == 0x4f6d6a273422e220
        assert melg._state[9] == 0x56a7458a6eece57b

        melg.seed(0.357)
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state[0] == 0x5fee464f36fc42c3
        assert melg._state[2] == 0xa985465a4a5fc644
        assert melg._state[4] == 0xa3aac457d81d552c
        assert melg._state[6] == 0x1c4d126a40f3f8a9
        assert melg._state[8] == 0x89b7be31ad4c739f
        assert melg._state[9] == 0xe8f9525bf6c56aef

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
        melg = Melg607()

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

        melg.setstate((tuple(i+31 for i in range(TestMelg607.Melg607_STATE_SIZE)), 3))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+31 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg.setstate([[i+41 for i in range(TestMelg607.Melg607_STATE_SIZE)], 18])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+41 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg.setstate([tuple(i+51 for i in range(TestMelg607.Melg607_STATE_SIZE)), 3])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 3
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+51 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg.setstate(([i+61 for i in range(TestMelg607.Melg607_STATE_SIZE)], 18))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 8
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+61 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg.setstate(tuple(i+11 for i in range(TestMelg607.Melg607_STATE_SIZE)))  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+11 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

        melg.setstate([i+21 for i in range(TestMelg607.Melg607_STATE_SIZE)])  # type: ignore
        assert melg.gauss_next is None  # type: ignore
        assert melg._index == 0
        assert melg.gauss_next is None  # type: ignore
        assert melg._state == [i+21 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore

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
            _state = [i+1 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore
            _state[TestMelg607.Melg607_STATE_SIZE - 2] = -1
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore
            _state[TestMelg607.Melg607_STATE_SIZE - 3] = 0.321
            melg.setstate(_state)  # type: ignore
        with pytest.raises(ValueError):
            _state = [i+1 for i in range(TestMelg607.Melg607_STATE_SIZE)]  # type: ignore
            _state[TestMelg607.Melg607_STATE_SIZE - 5] = {1, 2}
            melg.setstate(_state)  # type: ignore
