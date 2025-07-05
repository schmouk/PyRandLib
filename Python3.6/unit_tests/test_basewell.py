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
import platform
import pytest

from PyRandLib.basewell import BaseWELL
from PyRandLib.splitmix import SplitMix32


#=============================================================================
class TestBaseWELL:
    """Tests the base class BaseWELL.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')
    
    #-------------------------------------------------------------------------
    def test_class_WELL(self):
        assert BaseWELL._NORMALIZE == 1.0 / (1 << 32)
        assert BaseWELL._OUT_BITS == 32
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        STATE_SIZE = 15
        b_wll = BaseWELL(STATE_SIZE)
        assert b_wll._STATE_SIZE == STATE_SIZE
        assert b_wll._initRandClass is SplitMix32
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0
        assert len(b_wll._state) == STATE_SIZE
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        STATE_SIZE = 17
        b_wll = BaseWELL(STATE_SIZE, 0X1234_5678_9abc_def0)
        assert b_wll._STATE_SIZE == STATE_SIZE
        assert b_wll._initRandClass is SplitMix32
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0
        assert len(b_wll._state) == STATE_SIZE
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_wll = BaseWELL(STATE_SIZE, 0.1)
        assert b_wll._STATE_SIZE == STATE_SIZE
        assert b_wll._initRandClass is SplitMix32
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0
        assert len(b_wll._state) == STATE_SIZE
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        STATE_SIZE = 19
        b_wll = BaseWELL(STATE_SIZE, tuple(i+1 for i in range(STATE_SIZE)))  # type: ignore
        assert b_wll._STATE_SIZE == STATE_SIZE
        assert b_wll._initRandClass is SplitMix32
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0
        assert len(b_wll._state) == STATE_SIZE
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        STATE_SIZE = 21
        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                b_wll = BaseWELL(STATE_SIZE, [23, 163])
        else:
            b_wll = BaseWELL(STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
            assert b_wll._STATE_SIZE == STATE_SIZE
            assert b_wll._initRandClass is SplitMix32
            assert b_wll.gauss_next is None  # type: ignore
            assert b_wll._index == 0
            assert len(b_wll._state) == STATE_SIZE
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        STATE_SIZE = 23
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor until Python 3.11
            b_wll = BaseWELL(STATE_SIZE, tuple(STATE_SIZE-1, tuple(i+1 for i in range(STATE_SIZE))))  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        STATE_SIZE = 25
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor until Python 3.11
            b_wll = BaseWELL( STATE_SIZE, tuple(STATE_SIZE-1, [i+1 for i in range(STATE_SIZE)]) )  # type: ignore

    #-------------------------------------------------------------------------
    def test_seed(self):
        b_wll = BaseWELL(5)
        assert b_wll._STATE_SIZE == 5
        assert b_wll._initRandClass is SplitMix32
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0
        assert len(b_wll._state) == 5
        assert all(0 < s < (1 << b_wll._OUT_BITS) for s in b_wll._state)  # type: ignore

        with pytest.raises(TypeError):
            b_wll.seed((1, 2, 3, 4, 5))  # type: ignore
            assert b_wll._state == [1, 2, 3, 4, 5]
            assert b_wll.gauss_next is None  # type: ignore
            assert b_wll._index == 0

        with pytest.raises(TypeError):
            b_wll.seed([11, 12, 13, 14, 15])  # type: ignore
            assert b_wll._state == [11, 12, 13, 14, 15]
            assert b_wll.gauss_next is None  # type: ignore
            assert b_wll._index == 0

        with pytest.raises(TypeError):
            b_wll.seed([[31, 32, 33, 34, 35], 2])  # type: ignore
            assert b_wll._state == [31, 32, 33, 34, 35]
            assert b_wll.gauss_next is None  # type: ignore
            assert b_wll._index == 2

        with pytest.raises(TypeError):
            b_wll.seed(((21, 22, 23, 24, 25), 3))  # type: ignore
            assert b_wll._state == [21, 22, 23, 24, 25]
            assert b_wll.gauss_next is None  # type: ignore
            assert b_wll._index == 3

        with pytest.raises(ValueError):
            b_wll.seed(8.87e+18)
        with pytest.raises(ValueError):
            b_wll.seed(-0.987)
        with pytest.raises(TypeError):
            b_wll.seed([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(TypeError):
            b_wll.seed((31, 32, 33, 34, 35.1))  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        b_wll = BaseWELL(5)

        with pytest.raises(TypeError):
            b_wll.setstate(-1)  # type: ignore

        with pytest.raises(TypeError):
            b_wll.setstate(28031)  # type: ignore

        with pytest.raises(TypeError):
            b_wll.setstate(0xffff_ffff_ffff_ffff)  # type: ignore

        with pytest.raises(TypeError):
            b_wll.setstate(0.187)  # type: ignore

        with pytest.raises(TypeError):
            b_wll.setstate(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)  # type: ignore

        b_wll.setstate((1, 2, 3, 4, 5))  # type: ignore
        assert b_wll._state == [1, 2, 3, 4, 5]
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0

        b_wll.setstate([11, 12, 13, 14, 15])
        assert b_wll._state == [11, 12, 13, 14, 15]
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 0

        b_wll.setstate([[31, 32, 33, 34, 35], 2])  # type: ignore
        assert b_wll._state == [31, 32, 33, 34, 35]
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 2

        b_wll.setstate(((21, 22, 23, 24, 25), 3))  # type: ignore
        assert b_wll._state == [21, 22, 23, 24, 25]
        assert b_wll.gauss_next is None  # type: ignore
        assert b_wll._index == 3

        with pytest.raises(TypeError):
            b_wll.setstate(8.87e+18)  # type: ignore
        with pytest.raises(TypeError):
            b_wll.setstate(-0.987)  # type: ignore

        with pytest.raises(ValueError):
            b_wll.setstate([31, 32, 33.5, 34, 35.1])  # type: ignore
        with pytest.raises(ValueError):
            b_wll.setstate((31, 32.6, 33, 34, 35.1))  # type: ignore
            
        with pytest.raises(ValueError):
            b_wll.setstate([-31, 32, 33, 34, -35])
        with pytest.raises(ValueError):
            b_wll.setstate((31, -32, 33, 34, 35))  # type: ignore

        with pytest.raises(ValueError):
            b_wll.setstate([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(ValueError):
            b_wll.setstate(([31, 32, 33, 34.0, 35.1], 2))
        with pytest.raises(ValueError):
            b_wll.setstate([(31, 32, 33, 34, -35), 1])  # type: ignore
        with pytest.raises(ValueError):
            b_wll.setstate(((31, 32, 33, -34, -35), 1))  # type: ignore

    #-------------------------------------------------------------------------
    def test_M0(self):
        for x in range(-1, 1000, 7):
            assert BaseWELL._M0(x) == 0

    #-------------------------------------------------------------------------
    def test_M1(self):
        for x in range(0, 1000, 7):
            assert BaseWELL._M1(x) == x

    #-------------------------------------------------------------------------
    def test_M2pos(self):
        x = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M2_pos(x, t) == x >> t

    #-------------------------------------------------------------------------
    def test_M2neg(self):
        x = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M2_neg(x, t) == (x << t) & 0xffff_ffff

    #-------------------------------------------------------------------------
    def test_M3pos(self):
        x = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M3_pos(x, t) == x ^(x >> t)

    #-------------------------------------------------------------------------
    def test_M3neg(self):
        x = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M3_neg(x, t) == (x ^(x << t)) & 0xffff_ffff

    #-------------------------------------------------------------------------
    def test_M4(self):
        a = 0b10100101_01011010_10100101_01011010
        x1 = 0x8000_ffff
        x2 = 0x7fed_cba9
        assert BaseWELL._M4(x1, a) == (x1 >> 1) ^ a
        assert BaseWELL._M4(x2, a) == (x2 >> 1)

    #-------------------------------------------------------------------------
    def test_M5neg(self):
        x = 0x7fed_cba9_8654_0123
        a = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M5_neg(x, t, a) == x ^ (((x << t) & 0xffff_ffff) & a)

    #-------------------------------------------------------------------------
    def test_M5pos(self):
        x = 0x7fed_cba9_8654_0123
        a = 0b10100101_01011010_10100101_01011010
        for t in range(34):
            assert BaseWELL._M5_pos(x, t, a) == x ^ ((x >> t) & a)

    #-------------------------------------------------------------------------
    def test_M6(self):
        d_s = (0xffff_fffe, 0xffff_fffd, 0xffff_fffb, 0xffff_fff7,
               0xffff_ffef, 0xffff_ffdf, 0xffff_ffbf, 0xffff_ff7f, 
               0xffff_feff, 0xffff_fdff, 0xffff_fbff, 0xffff_f7ff,
               0xffff_efff, 0xffff_dfff, 0xffff_bfff, 0xffff_7fff,
               0xfffe_ffff, 0xfffd_ffff, 0xfffb_ffff, 0xfff7_ffff,
               0xffef_ffff, 0xffdf_ffff, 0xffbf_ffff, 0xff7f_ffff,
               0xfeff_ffff, 0xfdff_ffff, 0xfbff_ffff, 0xf7ff_ffff,
               0xefff_ffff, 0xdfff_ffff, 0xbfff_ffff, 0x7fff_ffff)
        x = 0x7fed_cba9
        a = 0b10100101_01011010_10100101_01011010
        for s in range(32):
            for q in range(32):
                for t in range(32):
                    y = (((x << q) & 0xffff_ffff) ^ (x >> (32-q))) & d_s[s]
                    if x & (1<<t) != 0:
                        assert BaseWELL._M6(x, q, t, s, a) == y ^ a
                    else:
                        assert BaseWELL._M6(x, q, t, s, a) == y

    #-------------------------------------------------------------------------
    def test_d(self):
        expected = (0xffff_fffe, 0xffff_fffd, 0xffff_fffb, 0xffff_fff7,
                    0xffff_ffef, 0xffff_ffdf, 0xffff_ffbf, 0xffff_ff7f, 
                    0xffff_feff, 0xffff_fdff, 0xffff_fbff, 0xffff_f7ff,
                    0xffff_efff, 0xffff_dfff, 0xffff_bfff, 0xffff_7fff,
                    0xfffe_ffff, 0xfffd_ffff, 0xfffb_ffff, 0xfff7_ffff,
                    0xffef_ffff, 0xffdf_ffff, 0xffbf_ffff, 0xff7f_ffff,
                    0xfeff_ffff, 0xfdff_ffff, 0xfbff_ffff, 0xf7ff_ffff,
                    0xefff_ffff, 0xdfff_ffff, 0xbfff_ffff, 0x7fff_ffff)
        for s in range(32):
            assert BaseWELL._d(s) == expected[s]

    #-------------------------------------------------------------------------
    def test_tempering(self):
        b = (0xe46e_1700, 0x93dd_1400)
        c = (0x9b86_8000, 0xfa11_8000)

        for x in range(0, 0xffff_ffff, 0x12_6543):
            for i in range(2):
                y = x ^ (((x << 7) & 0xffff_ffff) & b[i])
                assert BaseWELL._tempering(x, b[i], c[i]) == y ^ (((y << 15) & 0xffff_ffff) & c[i])
