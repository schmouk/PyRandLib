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

from PyRandLib.basemelg import BaseMELG
from PyRandLib.splitmix import SplitMix64


#=============================================================================
class TestBaseMELG:
    """Tests the base class BaseMELG.
    """
    
    #-------------------------------------------------------------------------
    def test_class_MELG(self):
        assert BaseMELG._NORMALIZE == 1.0 / (1 << 64)
        assert BaseMELG._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        STATE_SIZE = 15
        b_melg = BaseMELG(STATE_SIZE)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        STATE_SIZE = 17
        b_melg = BaseMELG(STATE_SIZE, 0X1234_5678_9abc_def0)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_melg = BaseMELG(STATE_SIZE, 0.1)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        STATE_SIZE = 19
        b_melg = BaseMELG(STATE_SIZE, tuple(i+1 for i in range(STATE_SIZE)))  # type: ignore
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        STATE_SIZE = 21
        b_melg = BaseMELG(STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        STATE_SIZE = 23
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_melg = BaseMELG(STATE_SIZE, tuple(STATE_SIZE-1, tuple(i+1 for i in range(STATE_SIZE))))  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        STATE_SIZE = 25
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_melg = BaseMELG( STATE_SIZE, tuple(STATE_SIZE-1, [i+1 for i in range(STATE_SIZE)]) )  # type: ignore

    #-------------------------------------------------------------------------
    def test_seed(self):
        b_melg = BaseMELG(5)
        assert b_melg._STATE_SIZE == 5
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0
        assert len(b_melg._state) == 5
        assert all( 0 < s <= (1 << 64) for s in b_melg._state )  # type: ignore

        with pytest.raises(TypeError):
            b_melg.seed((1, 2, 3, 4, 5))  # type: ignore
            assert b_melg._state == [1, 2, 3, 4, 5]
            assert b_melg.gauss_next is None  # type: ignore
            assert b_melg._index == 0

        with pytest.raises(TypeError):
            b_melg.seed([11, 12, 13, 14, 15])  # type: ignore
            assert b_melg._state == [11, 12, 13, 14, 15]
            assert b_melg.gauss_next is None  # type: ignore
            assert b_melg._index == 0

        with pytest.raises(TypeError):
            b_melg.seed([[31, 32, 33, 34, 35], 2])  # type: ignore
            assert b_melg._state == [31, 32, 33, 34, 35]
            assert b_melg.gauss_next is None  # type: ignore
            assert b_melg._index == 2

        with pytest.raises(TypeError):
            b_melg.seed(((21, 22, 23, 24, 25), 3))  # type: ignore
            assert b_melg._state == [21, 22, 23, 24, 25]
            assert b_melg.gauss_next is None  # type: ignore
            assert b_melg._index == 3

        with pytest.raises(ValueError):
            b_melg.seed(8.87e+18)
        with pytest.raises(ValueError):
            b_melg.seed(-0.987)
        with pytest.raises(TypeError):
            b_melg.seed([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(TypeError):
            b_melg.seed((31, 32, 33, 34, 35.1))  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        b_melg = BaseMELG(5)

        with pytest.raises(TypeError):
            b_melg.setstate(-1)  # type: ignore

        with pytest.raises(TypeError):
            b_melg.setstate(28031)  # type: ignore

        with pytest.raises(TypeError):
            b_melg.setstate(0xffff_ffff_ffff_ffff)  # type: ignore

        with pytest.raises(TypeError):
            b_melg.setstate(0.187)  # type: ignore

        with pytest.raises(TypeError):
            b_melg.setstate(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)  # type: ignore

        b_melg.setstate((1, 2, 3, 4, 5))  # type: ignore
        assert b_melg._state == [1, 2, 3, 4, 5]
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0

        b_melg.setstate([11, 12, 13, 14, 15])
        assert b_melg._state == [11, 12, 13, 14, 15]
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 0

        b_melg.setstate([[31, 32, 33, 34, 35], 2])  # type: ignore
        assert b_melg._state == [31, 32, 33, 34, 35]
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 2

        b_melg.setstate(((21, 22, 23, 24, 25), 3))  # type: ignore
        assert b_melg._state == [21, 22, 23, 24, 25]
        assert b_melg.gauss_next is None  # type: ignore
        assert b_melg._index == 3

        with pytest.raises(TypeError):
            b_melg.setstate(8.87e+18)  # type: ignore
        with pytest.raises(TypeError):
            b_melg.setstate(-0.987)  # type: ignore

        with pytest.raises(ValueError):
            b_melg.setstate([31, 32, 33.5, 34, 35.1])  # type: ignore
        with pytest.raises(ValueError):
            b_melg.setstate((31, 32.6, 33, 34, 35.1))  # type: ignore
            
        with pytest.raises(ValueError):
            b_melg.setstate([-31, 32, 33, 34, -35])
        with pytest.raises(ValueError):
            b_melg.setstate((31, -32, 33, 34, 35))  # type: ignore

        with pytest.raises(ValueError):
            b_melg.setstate([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(ValueError):
            b_melg.setstate(([31, 32, 33, 34.0, 35.1], 2))
        with pytest.raises(ValueError):
            b_melg.setstate([(31, 32, 33, 34, -35), 1])  # type: ignore
        with pytest.raises(ValueError):
            b_melg.setstate(((31, 32, 33, -34, -35), 1))  # type: ignore
