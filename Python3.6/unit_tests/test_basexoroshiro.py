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

from PyRandLib.basexoroshiro import BaseXoroshiro
from PyRandLib.splitmix      import SplitMix64


#=============================================================================
class TestBaseXoroshiro:
    """Tests the base class BaseXoroshiro.
    """
        
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')

    #-------------------------------------------------------------------------
    def test_class_BaseXoroshiro(self):
        assert BaseXoroshiro._NORMALIZE == 1.0 / (1 << 64)
        assert BaseXoroshiro._OUT_BITS == 64
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        STATE_SIZE = 15
        b_xrsr = BaseXoroshiro(STATE_SIZE)
        assert b_xrsr._STATE_SIZE == STATE_SIZE
        assert b_xrsr._initRandClass is SplitMix64
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0
        assert len( b_xrsr._state ) == STATE_SIZE
        assert all( s != 0 for s in b_xrsr._state )

    #-------------------------------------------------------------------------
    def test_init_int(self):
        STATE_SIZE = 17
        b_xrsr = BaseXoroshiro(STATE_SIZE, 0X1234_5678_9abc_def0)
        assert b_xrsr._STATE_SIZE == STATE_SIZE
        assert b_xrsr._initRandClass is SplitMix64
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0
        assert len( b_xrsr._state ) == STATE_SIZE
        assert all( s != 0 for s in b_xrsr._state )

    #-------------------------------------------------------------------------
    def test_init_float(self):
        STATE_SIZE = 17
        b_xrsr = BaseXoroshiro(STATE_SIZE, 0.1)
        assert b_xrsr._STATE_SIZE == STATE_SIZE
        assert b_xrsr._initRandClass is SplitMix64
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0
        assert len( b_xrsr._state ) == STATE_SIZE
        assert all( s != 0 for s in b_xrsr._state )

    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        STATE_SIZE = 19
        b_xrsr = BaseXoroshiro(STATE_SIZE, tuple(i+1 for i in range(STATE_SIZE)))  # type: ignore
        assert b_xrsr._STATE_SIZE == STATE_SIZE
        assert b_xrsr._initRandClass is SplitMix64
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0
        assert len( b_xrsr._state ) == STATE_SIZE
        assert all( s != 0 for s in b_xrsr._state )
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        STATE_SIZE = 21
        if self.python_version_39:  # notice: tests have been processed w. Python 3.9
            with pytest.raises(TypeError):
                # unhashable list bug in Python 3.9
                b_xrsr = BaseXoroshiro(STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
        else:
            b_xrsr = BaseXoroshiro(STATE_SIZE, [i+1 for i in range(STATE_SIZE)])
            assert b_xrsr._STATE_SIZE == STATE_SIZE
            assert b_xrsr._initRandClass is SplitMix64
            assert b_xrsr.gauss_next is None  # type: ignore
            assert b_xrsr._index == 0
            assert len( b_xrsr._state ) == STATE_SIZE
            assert all( s != 0 for s in b_xrsr._state )
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        STATE_SIZE = 23
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor
            b_xrsr = BaseXoroshiro(STATE_SIZE, tuple(STATE_SIZE-1, tuple(i+1 for i in range(STATE_SIZE))))  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        STATE_SIZE = 25
        with pytest.raises(TypeError):
            # notice: no 2 arguments accepted in tuple with base class random.Random constructor
            b_xrsr = BaseXoroshiro( STATE_SIZE, tuple(STATE_SIZE-1, [i+1 for i in range(STATE_SIZE)]) )  # type: ignore

    #-------------------------------------------------------------------------
    def test_seed(self):
        b_xrsr = BaseXoroshiro(5)
        assert b_xrsr._STATE_SIZE == 5
        assert b_xrsr._initRandClass is SplitMix64
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0
        assert len(b_xrsr._state) == 5
        assert all(s != 0 for s in b_xrsr._state)

        b_xrsr.seed(-1)
        assert b_xrsr._state == [0xe4d971771b652c20, 0xe99ff867dbf682c9, 0x382ff84cb27281e9, 0x6d1db36ccba982d2, 0xb4a0472e578069ae]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.seed(28031)
        assert b_xrsr._state == [0x2705aecd4f8c9690, 0x72100965d36abc80, 0x663e44c5f050c8fb, 0x975621c9151333a5, 0xc269b7b2092500b7]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.seed(0xffff_ffff_ffff_ffff)
        assert b_xrsr._state == [0xe4d971771b652c20, 0xe99ff867dbf682c9, 0x382ff84cb27281e9, 0x6d1db36ccba982d2, 0xb4a0472e578069ae]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.seed(0.187)
        assert b_xrsr._state == [0x2b18160c0a9f05b4, 0xc8197d13a4d6d45f, 0xaca007e67e920ed1, 0xf0e779fe3279121f, 0xcd551efd3099f223]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert b_xrsr._state == [0xf75f04cbb5a1a1dd, 0xec779c3693f88501, 0xfed9eeb4936de39d, 0x6f9fb04b092bd30a, 0x260ffb0260bbbe5f]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        with pytest.raises(TypeError):
            b_xrsr.seed((1, 2, 3, 4, 5))  # type: ignore
            assert b_xrsr._state == [1, 2, 3, 4, 5]
            assert b_xrsr.gauss_next is None  # type: ignore
            assert b_xrsr._index == 0

        with pytest.raises(TypeError):
            b_xrsr.seed([11, 12, 13, 14, 15])  # type: ignore
            assert b_xrsr._state == [11, 12, 13, 14, 15]
            assert b_xrsr.gauss_next is None  # type: ignore
            assert b_xrsr._index == 0

        with pytest.raises(TypeError):
            b_xrsr.seed([[31, 32, 33, 34, 35], 2])  # type: ignore
            assert b_xrsr._state == [31, 32, 33, 34, 35]
            assert b_xrsr.gauss_next is None  # type: ignore
            assert b_xrsr._index == 2

        with pytest.raises(TypeError):
            b_xrsr.seed(((21, 22, 23, 24, 25), 3))  # type: ignore
            assert b_xrsr._state == [21, 22, 23, 24, 25]
            assert b_xrsr.gauss_next is None  # type: ignore
            assert b_xrsr._index == 3

        with pytest.raises(ValueError):
            b_xrsr.seed(8.87e+18)
        with pytest.raises(ValueError):
            b_xrsr.seed(-0.987)
        with pytest.raises(TypeError):
            b_xrsr.seed([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(TypeError):
            b_xrsr.seed((31, 32, 33, 34, 35.1))  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        b_xrsr = BaseXoroshiro(5)

        with pytest.raises(TypeError):
            b_xrsr.setstate(-1)  # type: ignore

        with pytest.raises(TypeError):
            b_xrsr.setstate(28031)  # type: ignore

        with pytest.raises(TypeError):
            b_xrsr.setstate(0xffff_ffff_ffff_ffff)  # type: ignore

        with pytest.raises(TypeError):
            b_xrsr.setstate(0.187)  # type: ignore

        with pytest.raises(TypeError):
            b_xrsr.setstate(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)  # type: ignore

        b_xrsr.setstate((1, 2, 3, 4, 5))  # type: ignore
        assert b_xrsr._state == [1, 2, 3, 4, 5]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.setstate([11, 12, 13, 14, 15])
        assert b_xrsr._state == [11, 12, 13, 14, 15]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 0

        b_xrsr.setstate([[31, 32, 33, 34, 35], 2])  # type: ignore
        assert b_xrsr._state == [31, 32, 33, 34, 35]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 2

        b_xrsr.setstate(((21, 22, 23, 24, 25), 3))  # type: ignore
        assert b_xrsr._state == [21, 22, 23, 24, 25]
        assert b_xrsr.gauss_next is None  # type: ignore
        assert b_xrsr._index == 3

        with pytest.raises(TypeError):
            b_xrsr.setstate(8.87e+18)  # type: ignore
        with pytest.raises(TypeError):
            b_xrsr.setstate(-0.987)  # type: ignore

        with pytest.raises(ValueError):
            b_xrsr.setstate([31, 32, 33.5, 34, 35.1])  # type: ignore
        with pytest.raises(ValueError):
            b_xrsr.setstate((31, 32.6, 33, 34, 35.1))  # type: ignore
            
        with pytest.raises(ValueError):
            b_xrsr.setstate([-31, 32, 33, 34, -35])
        with pytest.raises(ValueError):
            b_xrsr.setstate((31, -32, 33, 34, 35))  # type: ignore

        with pytest.raises(ValueError):
            b_xrsr.setstate([[31, 32, 33, 34, 35.1], 1])  # type: ignore
        with pytest.raises(ValueError):
            b_xrsr.setstate(([31, 32, 33, 34.0, 35.1], 2))  # type: ignore
        with pytest.raises(ValueError):
            b_xrsr.setstate([(31, 32, 33, 34, -35), 1])  # type: ignore
        with pytest.raises(ValueError):
            b_xrsr.setstate(((31, 32, 33, -34, -35), 1))  # type: ignore
