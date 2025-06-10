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
    """Tests the base class BaseMELG"""
    
    #-------------------------------------------------------------------------
    def test_class_BaseMELG(self):
        assert BaseMELG._NORMALIZE == 1.0 / (1 << 64)
        assert BaseMELG._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        STATE_SIZE = 15
        b_melg = BaseMELG(STATE_SIZE)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all(s != 0 for s in b_melg._state)

    #-------------------------------------------------------------------------
    def test_init_int(self):
        STATE_SIZE = 17
        b_melg = BaseMELG(STATE_SIZE, 0X1234_5678_9abc_def0)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all(s != 0 for s in b_melg._state)

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_melg = BaseMELG(STATE_SIZE, 0.1)
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all(s != 0 for s in b_melg._state)

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        STATE_SIZE = 19
        b_melg = BaseMELG(STATE_SIZE, tuple(i+1 for i in range(STATE_SIZE)))
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all(s != 0 for s in b_melg._state)
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        STATE_SIZE = 21
        b_melg = BaseMELG(STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
        assert b_melg._STATE_SIZE == STATE_SIZE
        assert b_melg._initRandClass is SplitMix64
        assert b_melg.gauss_next is None
        assert b_melg._index == 0
        assert len(b_melg._state) == STATE_SIZE
        assert all(s != 0 for s in b_melg._state)
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        STATE_SIZE = 23
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_melg = BaseMELG(STATE_SIZE, tuple(STATE_SIZE-1, tuple(i+1 for i in range(STATE_SIZE))))

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        STATE_SIZE = 25
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_melg = BaseMELG( STATE_SIZE, tuple(STATE_SIZE-1, [i+1 for i in range(STATE_SIZE)]) )
