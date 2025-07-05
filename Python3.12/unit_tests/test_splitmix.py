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

from PyRandLib.splitmix import SplitMix31, SplitMix32, SplitMix63, SplitMix64


#=============================================================================
class TestSplitMix64:
    """Tests class SplitMix64.
    """

    #-------------------------------------------------------------------------
    def test_empty(self):
        splt = SplitMix64()
        prec = splt()
        assert 0 <= prec <= 0xffff_ffff_ffff_ffff
        for i in range(100_000):
            val = splt()
            assert 0 <= val <= 0xffff_ffff_ffff_ffff
            assert prec != val
            prec = val

    #-------------------------------------------------------------------------
    def test_int(self):
        splt = SplitMix64(1)
        for v in [0x910a2dec89025cc1, 0xbeeb8da1658eec67, 0xf893a2eefb32555e, 0x71c18690ee42c90b, 0x71bb54d8d101b5b9]:
            assert splt() == v
        
        splt = SplitMix64(-1)
        for v in [0xe4d971771b652c20, 0xe99ff867dbf682c9, 0x382ff84cb27281e9, 0x6d1db36ccba982d2, 0xb4a0472e578069ae]:
            assert splt() == v
                
        splt = SplitMix64(-8_870_000_000_000_000_000)
        for v in [0x48bbc5b84275f3ca, 0xe2fbc345a799b5aa, 0x86ce19a135fba0de, 0x637c87187035ea06, 0x2a03b9aff2bfd421]:
            assert splt
                
        splt = SplitMix64(8_870_000_000_000_000_000)
        for v in [0xeede014d9a5a6108, 0xa6eb6466bac9f251, 0x4246cbb1a64bf70c, 0xaf6aa8f43ebb8659, 0xe1b0fb2c7e764cdb]:
            assert splt

        splt = SplitMix64(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef)
        for v in [0x157a3807a48faa9d, 0xd573529b34a1d093, 0x2f90b72e996dccbe, 0xa2d419334c4667ec, 0x1404ce914938008]:
            assert splt

    #-------------------------------------------------------------------------
    def test_float(self):
        splt = SplitMix64(0.357)
        for v in [0x5fee464f36fc42c3, 0x954faf5a9ad49cf8, 0xa985465a4a5fc644, 0x77714db9e870d702, 0xa3aac457d81d552c]:
            assert splt() == v

        with pytest.raises(ValueError):
            splt = SplitMix64(-0.001)
        with pytest.raises(ValueError):
            splt = SplitMix64(1.001)

    #-------------------------------------------------------------------------
    def test_not_none(self):
        with pytest.raises(TypeError):
            splt = SplitMix64((1, 2))  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix64([1, 2])  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix64("123")  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix64(SplitMix64())  # type: ignore

    #-------------------------------------------------------------------------
    def test_call_int(self):
        splt = SplitMix64()

        assert splt(1) == 0x910a2dec89025cc1
        assert splt(-1) == 0xe4d971771b652c20
        assert splt(-8_870_000_000_000_000_000) == 0x48bbc5b84275f3ca
        assert splt(8_870_000_000_000_000_000) == 0xeede014d9a5a6108
        assert splt(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef) == 0x157a3807a48faa9d


#=============================================================================
class TestSplitMix63:
    """Tests class SplitMix63.
    """

    #-------------------------------------------------------------------------
    def test_empty(self):
        splt = SplitMix63()
        prec = splt()
        assert 0 <= prec <= 0xffff_ffff_ffff_ffff
        for i in range(100_000):
            val = splt()
            assert 0 <= val <= 0xffff_ffff_ffff_ffff
            assert prec != val
            prec = val

    #-------------------------------------------------------------------------
    def test_int(self):
        splt = SplitMix63(1)
        for v in [0x910a2dec89025cc1 >> 1, 0xbeeb8da1658eec67 >> 1, 0xf893a2eefb32555e >> 1, 0x71c18690ee42c90b >> 1, 0x71bb54d8d101b5b9 >> 1]:
            assert splt() == v
        
        splt = SplitMix63(-1)
        for v in [0xe4d971771b652c20 >> 1, 0xe99ff867dbf682c9 >> 1, 0x382ff84cb27281e9 >> 1, 0x6d1db36ccba982d2 >> 1, 0xb4a0472e578069ae >> 1]:
            assert splt() == v
                
        splt = SplitMix63(-8_870_000_000_000_000_000)
        for v in [0x48bbc5b84275f3ca >> 1, 0xe2fbc345a799b5aa >> 1, 0x86ce19a135fba0de >> 1, 0x637c87187035ea06 >> 1, 0x2a03b9aff2bfd421 >> 1]:
            assert splt
                
        splt = SplitMix63(8_870_000_000_000_000_000)
        for v in [0xeede014d9a5a6108 >> 1, 0xa6eb6466bac9f251 >> 1, 0x4246cbb1a64bf70c >> 1, 0xaf6aa8f43ebb8659 >> 1, 0xe1b0fb2c7e764cdb >> 1]:
            assert splt

        splt = SplitMix63(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef)
        for v in [0x157a3807a48faa9d >> 1, 0xd573529b34a1d093 >> 1, 0x2f90b72e996dccbe >> 1, 0xa2d419334c4667ec >> 1, 0x1404ce914938008 >> 1]:
            assert splt

    #-------------------------------------------------------------------------
    def test_float(self):
        splt = SplitMix63(0.357)
        for v in [0x5fee464f36fc42c3 >> 1, 0x954faf5a9ad49cf8 >> 1, 0xa985465a4a5fc644 >> 1, 0x77714db9e870d702 >> 1, 0xa3aac457d81d552c >> 1]:
            assert splt() == v

        with pytest.raises(ValueError):
            splt = SplitMix63(-0.001)
        with pytest.raises(ValueError):
            splt = SplitMix63(1.001)

    #-------------------------------------------------------------------------
    def test_not_none(self):
        with pytest.raises(TypeError):
            splt = SplitMix63((1, 2))  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix63([1, 2])  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix63("123")  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix63(SplitMix63())  # type: ignore

    #-------------------------------------------------------------------------
    def test_call_int(self):
        splt = SplitMix63()

        assert splt(1) == 0x910a2dec89025cc1 >> 1
        assert splt(-1) == 0xe4d971771b652c20 >> 1
        assert splt(-8_870_000_000_000_000_000) == 0x48bbc5b84275f3ca >> 1
        assert splt(8_870_000_000_000_000_000) == 0xeede014d9a5a6108 >> 1
        assert splt(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef) == 0x157a3807a48faa9d >> 1


#=============================================================================
class TestSplitMix32:
    """Tests class SplitMix32.
    """

    #-------------------------------------------------------------------------
    def test_empty(self):
        splt = SplitMix32()
        prec = splt()
        assert 0 <= prec <= 0xffff_ffff_ffff_ffff
        for i in range(100_000):
            val = splt()
            assert 0 <= val <= 0xffff_ffff_ffff_ffff
            assert prec != val
            prec = val

    #-------------------------------------------------------------------------
    def test_int(self):
        splt = SplitMix32(1)
        for v in [0x910a2dec89025cc1 >> 32, 0xbeeb8da1658eec67 >> 32, 0xf893a2eefb32555e >> 32, 0x71c18690ee42c90b >> 32, 0x71bb54d8d101b5b9 >> 32]:
            assert splt() == v
        
        splt = SplitMix32(-1)
        for v in [0xe4d971771b652c20 >> 32, 0xe99ff867dbf682c9 >> 32, 0x382ff84cb27281e9 >> 32, 0x6d1db36ccba982d2 >> 32, 0xb4a0472e578069ae >> 32]:
            assert splt() == v
                
        splt = SplitMix32(-8_870_000_000_000_000_000)
        for v in [0x48bbc5b84275f3ca >> 32, 0xe2fbc345a799b5aa >> 32, 0x86ce19a135fba0de >> 32, 0x637c87187035ea06 >> 32, 0x2a03b9aff2bfd421 >> 32]:
            assert splt
                
        splt = SplitMix32(8_870_000_000_000_000_000)
        for v in [0xeede014d9a5a6108 >> 32, 0xa6eb6466bac9f251 >> 32, 0x4246cbb1a64bf70c >> 32, 0xaf6aa8f43ebb8659 >> 32, 0xe1b0fb2c7e764cdb >> 32]:
            assert splt

        splt = SplitMix32(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef)
        for v in [0x157a3807a48faa9d >> 32, 0xd573529b34a1d093 >> 32, 0x2f90b72e996dccbe >> 32, 0xa2d419334c4667ec >> 32, 0x1404ce914938008 >> 32]:
            assert splt

    #-------------------------------------------------------------------------
    def test_float(self):
        splt = SplitMix32(0.357)
        for v in [0x5fee464f36fc42c3 >> 32, 0x954faf5a9ad49cf8 >> 32, 0xa985465a4a5fc644 >> 32, 0x77714db9e870d702 >> 32, 0xa3aac457d81d552c >> 32]:
            assert splt() == v

        with pytest.raises(ValueError):
            splt = SplitMix32(-0.001)
        with pytest.raises(ValueError):
            splt = SplitMix32(1.001)

    #-------------------------------------------------------------------------
    def test_not_none(self):
        with pytest.raises(TypeError):
            splt = SplitMix32((1, 2))  # type: ignore
        with pytest.raises(TypeError):
            splt = SpliSplitMix32tMix63([1, 2])  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix32("123")  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix32(SplitMix32())  # type: ignore

    #-------------------------------------------------------------------------
    def test_call_int(self):
        splt = SplitMix32()

        assert splt(1) == 0x910a2dec89025cc1 >> 32
        assert splt(-1) == 0xe4d971771b652c20 >> 32
        assert splt(-8_870_000_000_000_000_000) == 0x48bbc5b84275f3ca >> 32
        assert splt(8_870_000_000_000_000_000) == 0xeede014d9a5a6108 >> 32
        assert splt(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef) == 0x157a3807a48faa9d >> 32


#=============================================================================
class TestSplitMix31:
    """Tests class SplitMix31.
    """

    #-------------------------------------------------------------------------
    def test_empty(self):
        splt = SplitMix31()
        prec = splt()
        assert 0 <= prec <= 0xffff_ffff_ffff_ffff
        for i in range(100_000):
            val = splt()
            assert 0 <= val <= 0xffff_ffff_ffff_ffff
            assert prec != val
            prec = val

    #-------------------------------------------------------------------------
    def test_int(self):
        splt = SplitMix31(1)
        for v in [0x910a2dec89025cc1 >> 33, 0xbeeb8da1658eec67 >> 33, 0xf893a2eefb32555e >> 33, 0x71c18690ee42c90b >> 33, 0x71bb54d8d101b5b9 >> 33]:
            assert splt() == v
        
        splt = SplitMix31(-1)
        for v in [0xe4d971771b652c20 >> 33, 0xe99ff867dbf682c9 >> 33, 0x382ff84cb27281e9 >> 33, 0x6d1db36ccba982d2 >> 33, 0xb4a0472e578069ae >> 33]:
            assert splt() == v
                
        splt = SplitMix31(-8_870_000_000_000_000_000)
        for v in [0x48bbc5b84275f3ca >> 33, 0xe2fbc345a799b5aa >> 33, 0x86ce19a135fba0de >> 33, 0x637c87187035ea06 >> 33, 0x2a03b9aff2bfd421 >> 33]:
            assert splt
                
        splt = SplitMix31(8_870_000_000_000_000_000)
        for v in [0xeede014d9a5a6108 >> 33, 0xa6eb6466bac9f251 >> 33, 0x4246cbb1a64bf70c >> 33, 0xaf6aa8f43ebb8659 >> 33, 0xe1b0fb2c7e764cdb >> 33]:
            assert splt

        splt = SplitMix31(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef)
        for v in [0x157a3807a48faa9d >> 3332, 0xd573529b34a1d093 >> 33, 0x2f90b72e996dccbe >> 33, 0xa2d419334c4667ec >> 33, 0x1404ce914938008 >> 33]:
            assert splt

    #-------------------------------------------------------------------------
    def test_float(self):
        splt = SplitMix31(0.357)
        for v in [0x5fee464f36fc42c3 >> 33, 0x954faf5a9ad49cf8 >> 33, 0xa985465a4a5fc644 >> 33, 0x77714db9e870d702 >> 33, 0xa3aac457d81d552c >> 33]:
            assert splt() == v

        with pytest.raises(ValueError):
            splt = SplitMix31(-0.001)
        with pytest.raises(ValueError):
            splt = SplitMix31(1.001)

    #-------------------------------------------------------------------------
    def test_not_none(self):
        with pytest.raises(TypeError):
            splt = SplitMix31((1, 2))  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix31([1, 2])  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix31("123")  # type: ignore
        with pytest.raises(TypeError):
            splt = SplitMix31(SplitMix31())  # type: ignore

    #-------------------------------------------------------------------------
    def test_call_int(self):
        splt = SplitMix31()

        assert splt(1) == 0x910a2dec89025cc1 >> 33
        assert splt(-1) == 0xe4d971771b652c20 >> 33
        assert splt(-8_870_000_000_000_000_000) == 0x48bbc5b84275f3ca >> 33
        assert splt(8_870_000_000_000_000_000) == 0xeede014d9a5a6108 >> 33
        assert splt(0xfedc_ba98_7654_3210_0123_4567_89ab_cdef) == 0x157a3807a48faa9d >> 33
