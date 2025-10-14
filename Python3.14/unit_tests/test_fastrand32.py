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

from PyRandLib.fastrand32 import FastRand32


#=============================================================================
class TestFastRand32:
    """Tests class FastRand32.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert FastRand32._NORMALIZE == 1.0 / (1 << 32)
        assert FastRand32._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lcg = FastRand32()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0  # notice: should mostly be non-zero, while it could (but 1 over 2^32)

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lcg = FastRand32(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x910a2dec

        lcg = FastRand32(-2)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xf3203e90

        lcg = FastRand32(0x0123_4567_89ab_cdef)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x157a3807

        lcg = FastRand32(-8_870_000_000_000_000_000)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x48bbc5b8

        lcg = FastRand32(8_870_000_000_000_000_000)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xeede014d

        lcg = FastRand32(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xf75f04cb


    #-------------------------------------------------------------------------
    def test_init_float(self):
        lcg = FastRand32(0.357)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x5fee464f

        lcg = FastRand32(1.0)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0

        with pytest.raises(ValueError):
            lcg = FastRand32(-0.0001)
        with pytest.raises(ValueError):
            lcg = FastRand32(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lcg = FastRand32(1)  # type: ignore
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x910a2dec

        with pytest.raises(TypeError):
            lcg = FastRand32((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand32((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand32([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand32([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand32(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lcg = FastRand32(0x0123_4567_89ab_cdef)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x157a3807

        for v in [0x9fbe389c, 0xcccf40ed, 0xc93006ca, 0x9297b1c3, 0xc9434028]:
            assert lcg.next() == v

        assert lcg._state == 0xc9434028

    #-------------------------------------------------------------------------
    def test_seed(self):  # Notice: tests seed() and _seed() also
        lcg = FastRand32()
        
        lcg.seed()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0

        lcg.seed(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x910a2dec

        lcg.seed(-2)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xf3203e90

        lcg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xf75f04cb

        lcg.seed(0.357)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x5fee464f

        lcg.seed(1.0)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0

        with pytest.raises(ValueError):
            lcg.seed(-0.0001)
        with pytest.raises(ValueError):
            lcg.seed(1.001)

        with pytest.raises(TypeError):
            lcg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lcg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            lcg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lcg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            lcg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        lcg = FastRand32()

        lcg.setstate()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0
    
        lcg.setstate(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x910a2dec

        with pytest.raises(TypeError):
            lcg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            lcg.setstate("123")  # type: ignore

        with pytest.raises(TypeError):
            lcg.setstate((31, 32, 34, 33))  # type: ignore
        with pytest.raises(TypeError):
            lcg.setstate([41, 42, 44, 43])  # type: ignore
        with pytest.raises(TypeError):
            lcg.setstate([1])  # type: ignore
        with pytest.raises(TypeError):
            lcg.setstate((1,))  # type: ignore
