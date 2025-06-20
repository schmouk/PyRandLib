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

from PyRandLib.fastrand63 import FastRand63


#=============================================================================
class TestFastRand63:
    """Tests class FastRand63.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert FastRand63._NORMALIZE == 1.0 / (1 << 63)
        assert FastRand63._OUT_BITS == 63
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        lcg = FastRand63()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0  # notice: should mostly be non-zero, while it could (but 1 over 2^32)

    #-------------------------------------------------------------------------
    def test_init_int(self):
        lcg = FastRand63(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x488516f644812e60

        lcg = FastRand63(-2)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x79901f481cfa5410

        lcg = FastRand63(0x0123_4567_89ab_cdef)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xabd1c03d247d54e

        lcg = FastRand63(-8_870_000_000_000_000_000)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x245de2dc213af9e5

        lcg = FastRand63(8_870_000_000_000_000_000)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x776f00a6cd2d3084

        lcg = FastRand63(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x7baf8265dad0d0ee


    #-------------------------------------------------------------------------
    def test_init_float(self):
        lcg = FastRand63(0.357)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x2ff723279b7e2161

        lcg = FastRand63(1.0)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0

        with pytest.raises(ValueError):
            lcg = FastRand63(-0.0001)
        with pytest.raises(ValueError):
            lcg = FastRand63(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        lcg = FastRand63(1)  # type: ignore
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x488516f644812e60

        with pytest.raises(TypeError):
            lcg = FastRand63((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand63((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand63([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand63([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            lcg = FastRand63(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        lcg = FastRand63(0x0123_4567_89ab_cdef)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0xabd1c03d247d54e

        for v in [0x3f518f7da727aa7, 0x589fb832e7310d54, 0x77dbcffa81e88b65, 0x2e702905e2ada22a, 0x7190c03af2215733]:
            assert lcg.next() == v

        assert lcg._state == 0x7190c03af2215733

    #-------------------------------------------------------------------------
    def test_seed(self):  # Notice: tests seed() and _seed() also
        lcg = FastRand63()
        
        lcg.seed()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0

        lcg.seed(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x488516f644812e60

        lcg.seed(-2)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x79901f481cfa5410

        lcg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x7baf8265dad0d0ee

        lcg.seed(0.357)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x2ff723279b7e2161

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
        lcg = FastRand63()

        lcg.setstate()
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state != 0
    
        lcg.setstate(1)
        assert lcg.gauss_next is None  # type: ignore
        assert lcg._state == 0x488516f644812e60

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
