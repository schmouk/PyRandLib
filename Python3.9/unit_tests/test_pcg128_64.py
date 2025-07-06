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

from PyRandLib.pcg128_64 import Pcg128_64


#=============================================================================
class TestPcg128_64:
    """Tests class Pcg128_64.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert Pcg128_64._NORMALIZE == 1.0 / (1 << 64)
        assert Pcg128_64._OUT_BITS == 64
        assert Pcg128_64._A == 0x2360_ed05_1fc6_5da4_4385_df64_9fcc_f645
        assert Pcg128_64._C == 0x5851_f42d_4c95_7f2d_1405_7b7e_f767_814f
        assert Pcg128_64._MODULO_128 == (1 << 128) - 1

    #-------------------------------------------------------------------------
    def test_init_empty(self):
        pcg = Pcg128_64()
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state != 0  # notice: may be 0 but shouldn't

    #-------------------------------------------------------------------------
    def test_init_int(self):
        pcg = Pcg128_64(1)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x1_ffff_ffff_ffff_fffe

        pcg = Pcg128_64(-2)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xffff_ffff_ffff_fffe_0000_0000_0000_0001

        pcg = Pcg128_64(0x0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x0123_4567_89ab_cdef_fedc_ba98_7654_3210

        pcg = Pcg128_64(-8_870_000_000_000_000_000)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x84e7_6dfe_ca49_0000_7b18_9201_35b6_ffff

        pcg = Pcg128_64(8_870_000_000_000_000_000)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x7b18_9201_35b7_0000_84e7_6dfe_ca48_ffff

        pcg = Pcg128_64(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd

    #-------------------------------------------------------------------------
    def test_init_float(self):
        pcg = Pcg128_64(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b64_5a1c_ac08_3000_0000_0000_0000_0000

        pcg = Pcg128_64(1.0)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == int(1.0 * 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff)

        with pytest.raises(ValueError):
            pcg = Pcg128_64(-0.0001)
        with pytest.raises(ValueError):
            pcg = Pcg128_64(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        pcg = Pcg128_64(3)  # type: ignore
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x3_ffff_ffff_ffff_fffc

        pcg = Pcg128_64(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b64_5a1c_ac08_3000_0000_0000_0000_0000

        with pytest.raises(TypeError):
            pcg = Pcg128_64((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg128_64((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg128_64([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg128_64([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            pcg = Pcg128_64(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        pcg = Pcg128_64(0x0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x0123_4567_89ab_cdef_fedc_ba98_7654_3210

        for v in [0xffffffffffffffff, 0x13c49fecdee35f71, 0x4ee9574cc31f57d2, 0x718b9867b2c7ef05, 0xa9b3898995846d5c]:
            assert pcg.next() == v

        assert pcg._state == 0x08ab_2233_cb87_c6d6_2bf1_6123_1d0f_c8d3

    #-------------------------------------------------------------------------
    def test_seed(self):
        pcg = Pcg128_64()
        
        pcg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd

        pcg.seed(-0x1_0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == (1 << 128) - 0x1_0123_4567_89ab_cdef

        pcg.seed(-0x3_1000_0012_3456_789f_0123_4567_89ab_cdef)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == (1 << 128) - 0x1000_0012_3456_789f_0123_4567_89ab_cdef

        pcg.seed(0.357)
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state == 0x5b64_5a1c_ac08_3000_0000_0000_0000_0000

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
        pcg = Pcg128_64()

        pcg.setstate()
        assert pcg.gauss_next is None  # type: ignore
        assert pcg._state != 0
    
        pcg.setstate(1)  # type: ignore
        assert pcg._state == 0x1_ffff_ffff_ffff_fffe

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
