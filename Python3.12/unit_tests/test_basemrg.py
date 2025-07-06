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

from PyRandLib.basemrg import BaseMRG
from PyRandLib.splitmix import SplitMix31, SplitMix32


#=============================================================================
class TestBaseMRG:
    """Tests the base class BaseMRG.
    """
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        STATE_SIZE = 15
        b_mrg = BaseMRG(SplitMix31, STATE_SIZE)
        assert b_mrg._STATE_SIZE == STATE_SIZE
        assert b_mrg._initRandClass is SplitMix31
        assert b_mrg.gauss_next is None  # type: ignore
        assert b_mrg._index == 0
        assert len(b_mrg._state) == STATE_SIZE
        assert all(0 < s < (1 << b_mrg._OUT_BITS) for s in b_mrg._state)  # type: ignore
        assert b_mrg._NORMALIZE == 1.0 / (1 << 32)  # should be (1 << 31), but not set after construction of base class BaseMRG
        assert b_mrg._OUT_BITS == 32                # should be 31, but not set after construction of base class BaseMRG

    #-------------------------------------------------------------------------
    def test_init_int(self):
        STATE_SIZE = 17
        b_mrg = BaseMRG(SplitMix32, STATE_SIZE, 0X1234_5678_9abc_def0)
        assert b_mrg._STATE_SIZE == STATE_SIZE
        assert b_mrg._initRandClass is SplitMix32
        assert b_mrg.gauss_next is None  # type: ignore
        assert b_mrg._index == 0
        assert len(b_mrg._state) == STATE_SIZE
        assert all(0 < s < (1 << b_mrg._OUT_BITS) for s in b_mrg._state)  # type: ignore
        assert b_mrg._NORMALIZE == 1.0 / (1 << 32)
        assert b_mrg._OUT_BITS == 32

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_mrg = BaseMRG(SplitMix31, STATE_SIZE, 0.1)
        assert b_mrg._STATE_SIZE == STATE_SIZE
        assert b_mrg._initRandClass is SplitMix31
        assert b_mrg.gauss_next is None  # type: ignore
        assert b_mrg._index == 0
        assert len(b_mrg._state) == STATE_SIZE
        assert all(0 < s < (1 << b_mrg._OUT_BITS) for s in b_mrg._state)  # type: ignore
        assert b_mrg._NORMALIZE == 1.0 / (1 << 32)  # should be (1 << 31), but not set after construction of base class BaseMRG
        assert b_mrg._OUT_BITS == 32                # should be 31, but not set after construction of base class BaseMRG

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        STATE_SIZE = 19
        b_mrg = BaseMRG(SplitMix32, STATE_SIZE, tuple(i+1 for i in range(STATE_SIZE)))  # type: ignore
        assert b_mrg._STATE_SIZE == STATE_SIZE
        assert b_mrg._initRandClass is SplitMix32
        assert b_mrg.gauss_next is None  # type: ignore
        assert b_mrg._index == 0
        assert len(b_mrg._state) == STATE_SIZE
        assert all(0 < s < (1 << b_mrg._OUT_BITS) for s in b_mrg._state)  # type: ignore
        assert b_mrg._NORMALIZE == 1.0 / (1 << 32)
        assert b_mrg._OUT_BITS == 32
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        STATE_SIZE = 21
        b_mrg = BaseMRG(SplitMix31, STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
        assert b_mrg._STATE_SIZE == STATE_SIZE
        assert b_mrg._initRandClass is SplitMix31
        assert b_mrg.gauss_next is None  # type: ignore
        assert b_mrg._index == 0
        assert len(b_mrg._state) == STATE_SIZE
        assert all(0 < s < (1 << b_mrg._OUT_BITS) for s in b_mrg._state)  # type: ignore
        assert b_mrg._NORMALIZE == 1.0 / (1 << 32)  # should be (1 << 31), but not set after construction of base class BaseMRG
        assert b_mrg._OUT_BITS == 32                # should be 31, but not set after construction of base class BaseMRG
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        STATE_SIZE = 23
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_mrg = BaseMRG(SplitMix32, STATE_SIZE, tuple(STATE_SIZE-1, tuple(i+1 for i in range(STATE_SIZE))))  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        STATE_SIZE = 25
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor since Python 3.11
            b_mrg = BaseMRG( SplitMix31, STATE_SIZE, tuple(STATE_SIZE-1, [i+1 for i in range(STATE_SIZE)]) )  # type: ignore
