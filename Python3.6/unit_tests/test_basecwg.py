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

from PyRandLib.basecwg import BaseCWG


#=============================================================================
class TestBaseCwg:
    """Tests the base class BaseCWG.
    """
    
    python_version_39: bool = platform.python_version_tuple()[:2] == ('3', '9')

    #-------------------------------------------------------------------------
    def test_init_empty(self):
        b_cwg = BaseCWG()
        assert b_cwg.gauss_next is None  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_int(self):
        b_cwg = BaseCWG(0X1234_5678_9abc_def0)
        assert b_cwg.gauss_next is None  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_float(self):
        b_cwg = BaseCWG(0.1)
        assert b_cwg.gauss_next is None  # type: ignore
        
    #-------------------------------------------------------------------------
    def test_init_tuple(self):
        with pytest.raises(NotImplementedError):
            b_cwg = BaseCWG((0, 1, 0X1234_5678_9abc_def0, 0X1234_5678_9abc_def0))  # type: ignore
                
    #-------------------------------------------------------------------------
    def test_init_list(self):
        with pytest.raises(TypeError if self.python_version_39 else  NotImplementedError):  # notice: tests have been processed w. Python 3.9
            b_cwg = BaseCWG([0, 1, 0X1234_5678_9abc_def0, 0X1234_5678_9abc_def0])
                
    #-------------------------------------------------------------------------
    def test_init_tuple_int(self):
        with pytest.raises(NotImplementedError):
            b_cwg = BaseCWG( ((0, 1, 0X1234_5678_9abc_def0, 0X1234_5678_9abc_def0), 11) )  # type: ignore

    #-------------------------------------------------------------------------
    def test_init_list_int(self):
        with pytest.raises(TypeError if self.python_version_39 else  NotImplementedError):  # notice: tests have been processed w. Python 3.9
            b_cwg = BaseCWG( ([0, 1, 0X1234_5678_9abc_def0, 0X1234_5678_9abc_def0], 11))
                
    #-------------------------------------------------------------------------
    def test_getstate(self):
        b_cwg = BaseCWG()
        with pytest.raises(AttributeError):
            a, weyl, s, state = b_cwg.getstate()  # type: ignore
