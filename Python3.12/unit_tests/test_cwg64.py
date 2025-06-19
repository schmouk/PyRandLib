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

from PyRandLib.cwg64 import Cwg64


#=============================================================================
class TestCwg64:
    """Tests class Cwg64.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert Cwg64._NORMALIZE == 1.0 / (1 << 64)
        assert Cwg64._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        cwg = Cwg64()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0  # notice: may be 0 but shouldn't

    #-------------------------------------------------------------------------
    def test_init_int(self):
        cwg = Cwg64(1)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x910a2dec89025cc1
        assert cwg._state == 0xbeeb8da1658eec67

        cwg = Cwg64(-2)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf3203e9039f4a821
        assert cwg._state == 0xba56949915dcf9e9

        cwg = Cwg64(0x0123_4567_89ab_cdef)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x157a3807a48faa9d
        assert cwg._state == 0xd573529b34a1d093

        cwg = Cwg64(-8_870_000_000_000_000_000)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x48bbc5b84275f3cb
        assert cwg._state == 0xe2fbc345a799b5aa

        cwg = Cwg64(8_870_000_000_000_000_000)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xeede014d9a5a6109
        assert cwg._state == 0xa6eb6466bac9f251

        cwg = Cwg64(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf75f04cbb5a1a1dd
        assert cwg._state == 0xec779c3693f88501

    #-------------------------------------------------------------------------
    def test_init_float(self):
        cwg = Cwg64(0.357)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x5fee464f36fc42c3
        assert cwg._state == 0x954faf5a9ad49cf8

        cwg = Cwg64(1.0)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0

        with pytest.raises(ValueError):
            cwg = Cwg64(-0.0001)
        with pytest.raises(ValueError):
            cwg = Cwg64(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        cwg = Cwg64((1, 2, 4, 3))  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 1
        assert cwg._weyl == 2
        assert cwg._s == 4 | 1
        assert cwg._state == 3

        cwg = Cwg64([11, 12, 14, 13])  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 11
        assert cwg._weyl == 12
        assert cwg._s == 14 | 1
        assert cwg._state == 13

        with pytest.raises(ValueError):
            cwg = Cwg64((1, 2, 3))  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg64((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg64([1, 2, 3])  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg64([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            cwg = Cwg64(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        cwg = Cwg64(0x0123_4567_89ab_cdef)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x157a3807a48faa9d
        assert cwg._state == 0xd573529b34a1d093

        for v in [0xdbfaff32e796ce05, 0x4ab030b1e0e73bc7, 0x33dbb1ac8abdb275, 0x2c6c9c56c4ce3f8f, 0x81a05875df4bf239]:
            assert cwg.next() == v

        assert cwg._a == 0x5c66d0834caad592
        assert cwg._weyl == 0x6b63182636ce5511
        assert cwg._s == 0x157a3807a48faa9d
        assert cwg._state == 0x81a05875df4bae5f

    #-------------------------------------------------------------------------
    def test_seed(self):
        cwg = Cwg64()
        
        cwg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf75f04cbb5a1a1dd
        assert cwg._state == 0xec779c3693f88501

        cwg.seed(0.357)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x5fee464f36fc42c3
        assert cwg._state == 0x954faf5a9ad49cf8

        with pytest.raises(ValueError):
            cwg.seed(-0.0001)
        with pytest.raises(ValueError):
            cwg.seed(1.001)

        cwg.seed()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0

        with pytest.raises(TypeError):
            cwg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        cwg = Cwg64()

        cwg.setstate()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0
    
        with pytest.raises(TypeError):
            cwg.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            cwg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            cwg.setstate("123")  # type: ignore

        cwg.setstate((31, 32, 34, 33))  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 31
        assert cwg._weyl == 32
        assert cwg._s == 34 | 1
        assert cwg._state == 33

        cwg.setstate([41, 42, 44, 43])  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 41
        assert cwg._weyl == 42
        assert cwg._s == 44 | 1
        assert cwg._state == 43

        with pytest.raises(ValueError):
            cwg.setstate([1, 2])
        with pytest.raises(ValueError):
            cwg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate([11, 12, 13.1, 14])  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate((21, 22, 23, -24))  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate((21, 22, 23, -24))  # type: ignore
