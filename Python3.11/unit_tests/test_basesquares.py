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

from PyRandLib.basesquares import BaseSquares


#=============================================================================
class TestBaseSquares:
    """Tests the base class BaseSquares"""
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        b_sqr = BaseSquares()
        assert b_sqr.gauss_next is None
        assert b_sqr._counter == 0
        assert b_sqr._key & 1 == 1
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

    #-------------------------------------------------------------------------
    def test_init_int(self):
        b_sqr = BaseSquares(0x0123_4567_89ab_cdef)
        assert b_sqr.gauss_next is None
        assert b_sqr._counter == 0
        assert b_sqr._key & 1 == 1
        assert b_sqr._key == 0x2c38_1b75_cd1e_96f3
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_sqr = BaseSquares(0.357)
        assert b_sqr.gauss_next is None
        assert b_sqr._counter == 0
        assert b_sqr._key == 0x69ef_8b1a_6eda_9b27
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)  # should be (1 << 31), but not set after construction of base class BaseSquares
        assert b_sqr._OUT_BITS == 32                # should be 31, but not set after construction of base class BaseSquares

        with pytest.raises(ValueError):
            b_sqr = BaseSquares(-0.1)
        with pytest.raises(ValueError):
            b_sqr = BaseSquares(1.0001)

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        b_sqr = BaseSquares((21, 160,))
        assert b_sqr.gauss_next is None
        assert b_sqr._counter == 21
        assert b_sqr._key == 161  # i.e. 160 | 1
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

        with pytest.raises(ValueError):
            b_sqr = BaseSquares((21, 160, 3))
        with pytest.raises(ValueError):
            b_sqr = BaseSquares((21,))

    #-------------------------------------------------------------------------
    def test_init_list(self):
        b_sqr = BaseSquares([23, 162])
        assert b_sqr.gauss_next is None
        assert b_sqr._counter == 23
        assert b_sqr._key == 163  # i.e. 162 | 1
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

        with pytest.raises(ValueError):
            b_sqr = BaseSquares([23, 162, 3])
        with pytest.raises(ValueError):
            b_sqr = BaseSquares([23])

    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        with pytest.raises(ValueError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_sqr = BaseSquares(((21, 161,), 11))

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        with pytest.raises(ValueError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_sqr = BaseSquares(([23, 163], 13))

    #-------------------------------------------------------------------------
    def test_getstate(self):
        b_sqr = BaseSquares([23, 163])
        counter, key = b_sqr.getstate()
        assert counter == b_sqr._counter
        assert key == b_sqr._key
        assert counter == 23
        assert key == 163
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

    #-------------------------------------------------------------------------
    def test_seed(self):
        b_sqr = BaseSquares()

        b_sqr.seed()
        assert b_sqr._counter == 0
        assert b_sqr._key & 1 == 1
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

        b_sqr.seed(0x0123_4567_89ab_cdef)
        assert b_sqr._counter == 0
        assert b_sqr._key == 0x2c38_1b75_cd1e_96f3
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

        b_sqr.seed(-8_870_000_000_000_000_000)
        assert b_sqr._counter == 0
        assert b_sqr._key == 0x5d7f_2468_39ae_54f3
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        b_sqr.seed(8_870_000_000_000_000_000)
        assert b_sqr._counter == 0
        assert b_sqr._key == 0xea49_fd18_2c19_435d
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        b_sqr.seed(0.357)
        assert b_sqr._counter == 0
        assert b_sqr._key == 0x69ef_8b1a_6eda_9b27
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        b_sqr.seed(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef)
        assert b_sqr._counter == 0
        assert b_sqr._key == 0x2c38_1b75_cd1e_96f3
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        with pytest.raises(TypeError):
            b_sqr.seed((1, 2))
        with pytest.raises(TypeError):
            b_sqr.seed([11, 12])
        with pytest.raises(TypeError):
            b_sqr.seed([21, 22, 23])
        with pytest.raises(TypeError):
            b_sqr.seed((31, 32, 33, 34))
        with pytest.raises(ValueError):
            b_sqr.seed(-0.1)
        with pytest.raises(ValueError):
            b_sqr.seed(1.0001)
        with pytest.raises(TypeError):
            b_sqr.seed([31, 32.1])
        with pytest.raises(TypeError):
            b_sqr.seed((34, 35.1))

    #-------------------------------------------------------------------------
    def test_setstate(self):
        b_sqr = BaseSquares()

        b_sqr.setstate()
        assert b_sqr._counter == 0
        assert b_sqr._key & 1 == 1
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS == 32

        b_sqr.setstate((1, 2))
        assert b_sqr._counter == 1
        assert b_sqr._key == 2 | 1
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        b_sqr.setstate([11, 12])
        assert b_sqr._counter == 11
        assert b_sqr._key == 12 | 1
        assert b_sqr.gauss_next is None
        assert b_sqr._NORMALIZE == 1.0 / (1 << 32)
        assert b_sqr._OUT_BITS

        with pytest.raises(TypeError):
            b_sqr.setstate(-0.1)
        with pytest.raises(TypeError):
            b_sqr.setstate(1.0001)
        with pytest.raises(ValueError):
            b_sqr.setstate([31, 32.1])
        with pytest.raises(ValueError):
            b_sqr.setstate((34, 35.1))

    #-------------------------------------------------------------------------
    def test__initkey(self):
        b_sqr = BaseSquares()
        assert b_sqr._initKey(0x0123_4567_89ab_cdef) == 0x2c38_1b75_cd1e_96f3
        assert b_sqr._initKey(-8_870_000_000_000_000_000) == 0x5d7f_2468_39ae_54f3
        assert b_sqr._initKey(8_870_000_000_000_000_000) == 0xea49_fd18_2c19_435d
        assert b_sqr._initKey(0.357) == 0x69ef_8b1a_6eda_9b27
        assert b_sqr._initKey(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef) == 0x2c38_1b75_cd1e_96f3
