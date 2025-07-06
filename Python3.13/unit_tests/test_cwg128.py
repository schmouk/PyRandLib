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

from PyRandLib.cwg128 import Cwg128


#=============================================================================
class TestCwg128:
    """Tests class Cwg128.
    """
    
    #-------------------------------------------------------------------------
    def test_class(self):
        assert Cwg128._NORMALIZE == 1.0 / (1 << 128)
        assert Cwg128._OUT_BITS == 128
    
    #-------------------------------------------------------------------------
    def test_init_empty(self):
        cwg = Cwg128()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0  # notice: should mostly be non-zero, while it could (but 1 over 2^128)

    #-------------------------------------------------------------------------
    def test_init_int(self):
        cwg = Cwg128(1)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x910a2dec89025cc1beeb8da1658eec67
        assert cwg._state == 0xf893a2eefb32555e71c18690ee42c90b

        cwg = Cwg128(-2)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf3203e9039f4a821ba56949915dcf9e9
        assert cwg._state == 0xd0d5127a96e8d90d1ef156bb76650c37

        cwg = Cwg128(0x0123_4567_89ab_cdef)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x157a3807a48faa9dd573529b34a1d093
        assert cwg._state == 0x2f90b72e996dccbea2d419334c4667ec

        cwg = Cwg128(-8_870_000_000_000_000_000)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x48bbc5b84275f3cae2fbc345a799b5ab
        assert cwg._state == 0x86ce19a135fba0de637c87187035ea06

        cwg = Cwg128(8_870_000_000_000_000_000)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xeede014d9a5a6108a6eb6466bac9f251
        assert cwg._state == 0x4246cbb1a64bf70caf6aa8f43ebb8659

        cwg = Cwg128(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf3203e9039f4a821f75f04cbb5a1a1dd
        assert cwg._state == 0xba56949915dcf9e9ec779c3693f88501


    #-------------------------------------------------------------------------
    def test_init_float(self):
        cwg = Cwg128(0.357)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x5fee464f36fc42c3954faf5a9ad49cf9
        assert cwg._state == 0xa985465a4a5fc64477714db9e870d702

        cwg = Cwg128(1.0)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0

        with pytest.raises(ValueError):
            cwg = Cwg128(-0.0001)
        with pytest.raises(ValueError):
            cwg = Cwg128(1.001)

    #-------------------------------------------------------------------------
    def test_init_state(self):
        cwg = Cwg128((1, 2, 4, 3))  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 1
        assert cwg._weyl == 2
        assert cwg._s == 4 | 1
        assert cwg._state == 3

        cwg = Cwg128([11, 12, 14, 13])  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 11
        assert cwg._weyl == 12
        assert cwg._s == 14 | 1
        assert cwg._state == 13

        with pytest.raises(ValueError):
            cwg = Cwg128((1, 2, 3))  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg128((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg128([1, 2, 3])  # type: ignore
        with pytest.raises(ValueError):
            cwg = Cwg128([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            cwg = Cwg128(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_next(self):
        cwg = Cwg128(0x0123_4567_89ab_cdef)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x157a3807a48faa9dd573529b34a1d093
        assert cwg._state == 0x2f90b72e996dccbea2d419334c4667ec

        for v in [0x4b5456b801cefdb28310efbd2ef27303,
                  0x5939ecb468a992f5ac7642257f12f0e6,
                  0x6dd81cbc1e016fadbab05196fd25d1a2,
                  0x8b10c583d21efb141656addf154ee48f,
                  0x4e21c10a0b2187a97ab330ef2a1e94a1]:
            assert cwg.next() == v

        assert cwg._a == 0xcd07dcdaf406c828a3624a8ad196482a
        assert cwg._weyl == 0x6b63182636ce55152b409d08072912df
        assert cwg._s == 0x157a3807a48faa9dd573529b34a1d093
        assert cwg._state == 0x4e21c10a0b2187a97ab330efe719487b

    #-------------------------------------------------------------------------
    def test_seed(self):  # Notice: tests seed() and _seed() also
        cwg = Cwg128()
        
        cwg.seed()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0

        cwg.seed(1)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x910a2dec89025cc1beeb8da1658eec67
        assert cwg._state == 0xf893a2eefb32555e71c18690ee42c90b

        cwg.seed(-2)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf3203e9039f4a821ba56949915dcf9e9
        assert cwg._state == 0xd0d5127a96e8d90d1ef156bb76650c37

        cwg.seed(0xffff_ffff_ffff_fffe_ffff_ffff_ffff_fffd)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0xf3203e9039f4a821f75f04cbb5a1a1dd
        assert cwg._state == 0xba56949915dcf9e9ec779c3693f88501

        cwg.seed(0.357)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s == 0x5fee464f36fc42c3954faf5a9ad49cf9
        assert cwg._state == 0xa985465a4a5fc64477714db9e870d702

        cwg.seed(1.0)
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0

        with pytest.raises(ValueError):
            cwg.seed(-0.0001)
        with pytest.raises(ValueError):
            cwg.seed(1.001)

        with pytest.raises(TypeError):
            cwg.seed((1, 2, 3))  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed([1, 2, 3])  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed([1, 2, 3, 4, 5])  # type: ignore
        with pytest.raises(TypeError):
            cwg.seed(set())  # type: ignore

    #-------------------------------------------------------------------------
    def test_setstate(self):
        cwg = Cwg128()

        cwg.setstate()
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 0
        assert cwg._weyl == 0
        assert cwg._s & 1 == 1
        assert cwg._state != 0
    
        with pytest.raises(TypeError):
            cwg.setstate(1)  # type: ignore

        with pytest.raises(TypeError):
            cwg.setstate(0.1)  # type: ignore

        with pytest.raises(TypeError):
            cwg.setstate("123")  # type: ignore

        cwg.setstate((31, 32, 34, 33))  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 31
        assert cwg._weyl == 32
        assert cwg._s == 34 | 1
        assert cwg._state == 33

        cwg.setstate([41, 42, 44, 43])  # type: ignore
        assert cwg.gauss_next is None  # type: ignore
        assert cwg._a == 41
        assert cwg._weyl == 42
        assert cwg._s == 44 | 1
        assert cwg._state == 43

        with pytest.raises(ValueError):
            cwg.setstate([1, 2])
        with pytest.raises(ValueError):
            cwg.setstate((1, 2, 3, 4, 5))  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate([1, 2, '3', 4])  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate([11, 12, 13.1, 14])  # type: ignore
        with pytest.raises(ValueError):
            cwg.setstate((21, 22, 23, -24))  # type: ignore
