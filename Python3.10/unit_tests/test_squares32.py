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

from PyRandLib.squares32 import Squares32


#=============================================================================
class TestSquares32:
    """Tests class Squares32.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert Squares32._NORMALIZE == 1.0 / (1 << 32)
        assert Squares32._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        sqr = Squares32()
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key & 1 == 1

    #-------------------------------------------------------------------------
    def test_init_int(self):
        sqr = Squares32(1)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0x9bd658ae46c9d5e3

        sqr = Squares32(-2)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0xfbe269a13c127d8f

        sqr = Squares32(0x0123_4567_89ab_cdef)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0x2c381b75cd1e96f3

        sqr = Squares32(-8_870_000_000_000_000_000)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0x5d7f246839ae54f3

        sqr = Squares32(8_870_000_000_000_000_000)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0xea49fd182c19435d

        sqr = Squares32(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0xfde6215797c8adf3

    #-------------------------------------------------------------------------
    def test_init_float(self):
        sqr = Squares32(0.357)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0x69ef8b1a6eda9b27

        sqr = Squares32(1.0)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._counter == 0
        assert sqr._key == 0xe71c24bfa7641285

        with pytest.raises(ValueError):
            sqr = Squares32(-0.0001)
        with pytest.raises(ValueError):
            sqr = Squares32(1.001)

    #-------------------------------------------------------------------------
    def test_next(self):
        sqr = Squares32(0x0123_4567_89ab_cdef)
        assert sqr.gauss_next is None  # type: ignore
        assert sqr._key == 0x2c381b75cd1e96f3

        expected: list = [0xc65a6688, 0xea057f03, 0x107ab4e2, 0xfc483b91, 0x8ce1c591]
        for v in expected:
            assert sqr.next() == v

        assert sqr._counter == len(expected)
        assert sqr._key == 0x2c381b75cd1e96f3
