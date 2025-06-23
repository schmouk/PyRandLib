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

from PyRandLib.pcg64_32 import Pcg64_32


#=============================================================================
class TestCwg64:
    """Tests class Pcg64_32.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert Pcg64_32._NORMALIZE == 1.0 / (1 << 32)
        assert Pcg64_32._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        pcg = Pcg64_32()
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state != 0  # notice: may be 0 but shouldn't

    #-------------------------------------------------------------------------
    def test_init_int(self):
        pcg = Pcg64_32(1)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 1

        pcg = Pcg64_32(-2)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xfffffffffffffffe

        pcg = Pcg64_32(0x0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x0123_4567_89ab_cdef

        pcg = Pcg64_32(-8_870_000_000_000_000_000)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x84e76dfeca490000

        pcg = Pcg64_32(8_870_000_000_000_000_000)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x7b18920135b70000

        pcg = Pcg64_32(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xfffffffffffffffd

    #-------------------------------------------------------------------------
    def test_init_float(self):
        pcg = Pcg64_32(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b645a1cac083000

        pcg = Pcg64_32(1.0)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == int(1.0 * 0xffff_ffff_ffff_ffff)

        with pytest.raises(ValueError):
            pcg = Pcg64_32(-0.0001)
        with pytest.raises(ValueError):
            pcg = Pcg64_32(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        pcg = Pcg64_32(3)  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 3

        pcg = Pcg64_32(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b645a1cac083000

        with pytest.raises(TypeError):
            pcg = Pcg64_32((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg64_32((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg64_32([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg64_32([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg64_32(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        pcg = Pcg64_32(0x0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x0123_4567_89ab_cdef

        for v in [0x8d158c12, 0xc65b2172, 0xa18de728, 0x83d45f91, 0x1094d283]:
            assert pcg.next() == v

        assert pcg._state == 0xc60c9ae76aeb1026

    #-------------------------------------------------------------------------
    def test_seed(self):
        pcg = Pcg64_32()
        
        pcg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xfffffffffffffffd

        pcg.seed(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b645a1cac083000

        with pytest.raises(ValueError):
            pcg.seed(-0.0001)
        with pytest.raises(ValueError):
            pcg.seed(1.001)

        pcg.seed()
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state != 0

        with pytest.raises(TypeError):
            pcg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            pcg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        pcg = Pcg64_32()

        pcg.setstate()
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state != 0
    
        pcg.setstate(1)  # type: ignore
        assert pcg._state == 1

        with pytest.raises(TypeError):
            pcg.setstate(0.1)  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate("123")  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate((31, 32, 34, 33))  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([41, 42, 44, 43])  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([1, 2])  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(TypeError):
            pcg.setstate([11, 12, 13.1, 14])  # type: ignore
