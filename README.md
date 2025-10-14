# PyRandLib  [![license](http://img.shields.io/github/license/schmouk/pyrandlib.svg?style=plastic&labelColor=blueviolet&color=lightblue)](https://github.com/schmouk/pyrandlib/license)  [![Latest release](http://img.shields.io/github/release/schmouk/pyrandlib.svg?style=plastic&labelColor=blueviolet&color=success)](https://github.com/schmouk/pyrandlib/releases)  [![code_coverage](https://img.shields.io/badge/code_coverage-100%25-success?style=plastic&labelColor=blueviolet)]()  [![tests](https://img.shields.io/badge/tests-passed-success?style=plastic&labelColor=blueviolet)]()
Many best in class pseudo random generators grouped into one simple library.



## License
PyRandLib is distributed under the MIT license for its largest use.  
If you decide to use this library, please add the copyright notice to your software as stated in the LICENSE file.

```
Copyright (c) 2016-2025 Philippe Schmouker, <ph.schmouker (at) gmail.com>

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
```



## Intro
This library implements some of the best-in-class pseudo random generators as evaluated by Pierre L'Ecuyer and Richard Simard in their famous paper "TestU01:  A C library for empirical testing of random  number generators" (ACM Trans. Math. Softw. Vol. 33 N.4, August 2007 -  see reference [1]). The reader will take benefit from reading L'Ecuyer & Simard's paper. This library implements also newer pseudo random generators that have been published since then. Their exhaustive list is provided here below and is valid for versions 2.0 and above of the library (i.e. since 2025/03):

* **Collatz-Weyl Generator** (Tomasz R. Dziala, **2023**)  
 (CWG, 64 bits, 128 bits or 128/64 bits, 3 different values of periodicities, see reference [8]);
* **Linear Congruential Generator** (Georges Marsaglia, **1972**, F.B. Brown and Y. Nagaya, **2002**)  
 (LCG, or FastRand, 32 bits or 63 bits, 2 different values of periodicities, see references [12] and [13] and [1]);
* **Lagged Fibonacci Generator** (Georges Marsaglia, **1985**)  
 (LFib, 64 bits, 4 different periodicities, see reference [4]);
* **Maximally Equidistributed Long-period Linear Generator** (Shin Harase, Takamitsu Kimoto, **2018**)  
 (MELG, 64/32 bits, 3 different values of periodicities, see reference [11]);
* **Multiple Recursive Generator** (Lih-Yuan Deng & Dennis K. J. Lin., **2000**, and Lih-Yuan Deng, **2005**)  
 (MRG, 31 bits or 32 bits, 3 different values of periodicities, see references [2] and [3]);
* **Permutated Congruential Generator** (Melissa E. O'Neill, **2014**)  
 (PCG, 64, 128 bits or 64/32 bits, 3 different values of periodicities, see reference [7]);
* **Squares** (ernard Widynski, **2022**)  
 (Squares, 32 or 64 bits, 1 value of periodicity but 32- or 64-bits output values, see reference [9]);
* **Well-Equilibrated Long-period Linear generators** (François Panneton, Pierre L'Ecuyer, Makoto Matsumoto, **2006**)  
 (WELL, 32 bits, 4 different values of periodicities, see reference [6]);
* **Scrambled Linear Pseudorandom Number Generators** (David Blackman, Sebastiano Vigna, **2018**)  
 (Xoroshiro, 64 bits, 4 different values of periodicities, see reference [10]).


Each of the Pseudo Random Numbers Generator (PRNG) implemented in **PyRandLib** is self documented. Names of classes directly refer to the type of PRNG they implement augmented with some number characterizing their periodicity. All of their randomness characteristics are explained in every related module.

Latest version of **PyRandLib** is version **2.2**, released by October 2025.
* It provides implementations dedicated to different versions of Python: 3.6 (the original version of the library), 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14.
* Time performances of every PRNG and for each version of Python (starting at 3.9) have been evaluated and are provided in tables below - see section *CPU Performances*.
* Furthermore, starting from release 2.1 **PyRandLib** is **fully validated**. PyTest and PyTest-cov are now used to unit-test the code with a full 100% code coverage.



### Why not Mersenne twister?

The Mersenne twister PRNG proposed by Matsumoto and Nishimura - see [5] - is the most widely used PRNG. The Random class of module random in Python implements this PRNG. It is also implemented in C++ and Java standard libraries for instance.

It offers a very good period (2^19937, i.e. about 4.3e6001). Unfortunately, this PRNG is a little bit long to compute (up to 3 times than LCGs, 60% more than LFibs and a little bit less than MRGs, see below  at section 'Architecture overview'). Moreover, it fails four of the hardest TestU01 tests. You can still use it as your preferred PRNG but **PyRandLib** implements many other PRNGs that are either far faster or far better in terms of generated pseudo-randomness than the Mersenne twister PRNG.



## Installation
Currently, the only way to install **PyRandLib** is to download the `.zip` or `.tar.gz` archive, then to directly put sub-directory `PyRandLib\` from archive into directory `Lib\site-packages\` of your Python environment. See https://schmouk.github.io/PyRandLib/ for an easy access to downloadable versions or click on tab **releases** on the home page of this GitHub repository.

Since release **2.0** of **PyrandLib** (Mar. 2025), the root directory of the library has been splitted into directories dedicated each to a different version of Python (3.6, 3.9, 3.10, etc.) Directory `PyRandLib\` is now a sub-directory of each of these directories, with code optimized for the related Python version. Just copy into your dev environment the `PyRandLib\` directory from the version of Python of your choice.

Since release **2.1** of **PyRandLib** (Jun. 2025), the whole code has been validated with unit tests (via *pytest* and *pytest-cov*). A few bugs have been fixed (*protected method `Pcg1024_32._externalstep()` implementation, or a typo in a shifting constant in Well19937c`.next()` for instance*). The code coverage rate is 100%. Pytest coverage output results are provided in files `coverage-res.txt`.  
Release **2.0** of **PyRandLib** is nevertheless still available **but it should no more be used**.

Release **2.2** (Oct. 2025) provides code for Python 3.14. This code is identical to the one provided for Python 3.13, with a very few optimizations on some generators implementation. Notice: the CPU performance tests show that Python 3.14 runs faster than Python 3.13 on same PyRandLib code.

**Notice**: distribution version to be installed via pip or easy-install in cmd tool or in console is still to come (no date yet, expected with release **3.0** of **PyRandLib**).



## Testing PyRandLib
The unit tests code is available for every Python standard version (3.6, 3.9 and above), in dedicated subdirectory `unit-tests` of every Python version directories.

### Install pytest and pytest-cov
To run the unit tests by your own, you have to install first pytest and pytest-cov in your Python environment (or virtual environment, recommended). The procedure is desribed below.

#### Either in a Virtual environment
In a console, create a new virtual environment in a path of your choice on disk:

    > python -m venv <path to the newly created virtual environment>

Activate it:

    > <path to the newly created virtual environment>/Scripts/Activate.ps1 (for Windows Powershell)
    or
    > <path to the newly created virtual environment>/Scripts/activate.bat (for Windows console)
    or
    $ source <path to the newly created virtual environment>/bin/activate (on Linux)

Install pytest:

    > python -m pip install --upgrade pip (not mandatory but always good to check)
    > python -m pip install pytest

Install pytest-cov:

    > python -m pip install pytest-cov

#### Or in your Python environment:
Install pytest:

    > python -m pip install --upgrade pip
    > python -m pip install pytest

Install pytest-cov:

    > python -m pip install pytest-cov


### Run the tests
Tests have been written to run in the context of a single Python standard version. Make the directory of your choice the working directory. For instance to test the Python3.13 version of PyRandLib just type:

    > cd <path to your PyRandLib directory>/Python3.13

Then either run

    > pytest --cov-config=.coveragerc --cov=. unit_tests

to get a full display of the code coverage and the detected failed tests (there should be none).

or run

    > pytest --cov-config=.coveragerc --cov=. unit_tests --cov-report=html

to get an HTML version of the report, to be displayed by double-clicking on file `<path to your PyRandLib directory>/Python3.13/htmlcov/index.html`. This file will automatically open itself in your favorite web browser. Click on any not fully covered file to get a whole view of their code with highlighted missed statements (there should be none in official releases, just on current dev).


### Expected results
In each of the subdirectories `Python3.xx` a text file `tests-cov.txt` contains a screen copy of the expected results.


## Randomness evaluation
In [1], every known PRNG at the time of the editing has been tested according to three different sets of tests:
* **_small crush_** is a small set of simple tests that quickly tests  some of the expected characteristics for a pretty good PRNG;
* **_crush_** is a bigger set of tests that test  more  deeply expected  random characteristics;
* **_big crush_** is the ultimate set of difficult tests that any **good**  PRNG should definitively pass.

We give you here below a copy of the resulting table for the PRNGs that have been implemented in **PyRandLib**, as provided in [1], plus the Mersenne twister one which is not implemented in **PyRandLib**.  
We add in this table the evaluations provided by the authors of every new PRNGs that have been described and published after the publication of [1]. Some fields may be missing then for them. A comparison of the computation times for all implemented PRNGs in **PyRandLib** is provided in other belowing tables.

<table>
<tr><th>PyRandLib class</th><th>TU01 generator name (1)</th><th>Memory Usage</th><th>Period</th><th>SmallCrush fails</th><th>Crush fails</th><th>BigCrush fails</th><th>time-64 bits</th><th>time-32bits</th></tr>
<tr><td>Cwg64</td><td>*CWG64*</td><td>8 x 4-bytes</td><td>>= 2^70</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Cwg128_64</td><td>*CWG128-64*</td><td>10 x 4-bytes</td><td>>= 2^71</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Cwg128</td><td>*CWG128*</td><td>16 x 4-bytes</td><td>>= 2^135</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>FastRand32</td><td>LCG(2^32, 69069, 1)</td><td>1 x 4-bytes</td><td>2^32</td><td>11</td><td>106</td><td>*too many*</td><td>0.67</td><td>3.20</td></tr>
<tr><td>FastRand63</td><td>LCG(2^63, 9219741426499971445, 1)</td><td>2 x 4-bytes</td><td>2^63</td><td>0</td><td>5</td><td>7</td><td>0.75</td><td>4.20</td></tr>
<tr><td>LFib78</td><td>LFib(2^64, 17, 5, +)</td><td>34 x 4-bytes</td><td>2^78</td><td>0</td><td>0</td><td>0</td><td>1.1</td><td>n.a.</td></tr>
<tr><td>LFib116</td><td>LFib(2^64, 55, 24, +)</td><td>110 x 4-bytes</td><td>2^116</td><td>0</td><td>0</td><td>0</td><td>1.0</td><td>n.a.</td></tr>
<tr><td>LFib668</td><td>LFib(2^64, 607, 273, +)</td><td>1,214 x 4-bytes</td><td>2^668</td><td>0</td><td>0</td><td>0</td><td>0.9</td><td>n.a.</td></tr>
<tr><td>LFib1340</td><td>LFib(2^64, 1279, 861, +)</td><td>2,558 x 4-bytes</td><td>2^1,340</td><td>0</td><td>0</td><td>0</td><td>0.9</td><td>n.a.</td></tr>
<tr><td>Melg607</td><td>*Melg607-64*</td><td>21 x 4-bytes</td><td>2^607</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a</td></tr>
<tr><td>Melg19937</td><td>*Melg19937-64*</td><td>625 x 4-bytes</td><td>2^19,937</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a</td></tr>
<tr><td>Melg44497</td><td>*Melg44497-64*</td><td>1,392 x 4-bytes</td><td>2^44,497</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a</td></tr>
<tr><td>Mrg287</td><td>Marsa-LFIB4</td><td>256 x 4-bytes</td><td>2^287</td><td>0</td><td>0</td><td>0</td><td>0.8</td><td>3.40</td></tr>
<tr><td>Mrg1457</td><td>DX-47-3</td><td>47 x 4-bytes</td><td>2^1,457</td><td>0</td><td>0</td><td>0</td><td>1.4</td><td>n.a.</td></tr>
<tr><td>Mrg49507</td><td>DX-1597-2-7</td><td>1,597 x 4-bytes</td><td>2^49,507</td><td>0</td><td>0</td><td>0</td><td>1.4</td><td>n.a.</td></tr>
<tr><td>Pcg64_32</td><td>*PCG XSH RS 64/32 (LCG)*</td><td>2 x 4 bytes</td><td>2^64</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Pcg128_64</td><td>*PCG XSL RR 128/64 (LCG)*</td><td>4 x 4 bytes</td><td>2^128</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Pcg1024_32</td><td>*PCG XSH RS 64/32 (EXT 1024)*</td><td>1,026 x 4 bytes</td><td>2^32,830</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Squares32</td><td>*squares32*</td><td>4 x 4-bytes</td><td>2^64</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Squares64</td><td>*squares64*</td><td>4 x 4-bytes</td><td>2^64</td><td>0</td><td>0</td><td>0</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Well512a</td><td>not available</td><td>16 x 4-bytes</td><td>2^512</td><td>n.a.</td><td>n.a.</td><td>n.a.</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Well1024a</td><td>WELL1024a</td><td>32 x 4-bytes</td><td>2^1,024</td><td>0</td><td>4</td><td>4</td><td>1.1</td><td>4.0</td></tr>
<tr><td>Well19937c (2)</td><td>WELL19937a</td><td>624 x 4-bytes</td><td>2^19,937</td><td>0</td><td>2</td><td>2</td><td>1.3</td><td>4.3</td></tr>
<tr><td>Well44497b (3)</td><td>not available</td><td>1,391 x 4-bytes</td><td>2^44,497</td><td>n.a.</td><td>n.a.</td><td>n.a.</td><td>n.a.</td><td>n.a.</td></tr>
<tr><td>Mersenne Twister</td><td>MT19937</td><td>624 x 4-bytes</td><td>2^19,937</td><td>0</td><td>2</td><td>2</td><td>1.6</td><td>4.30</td></tr>
<tr><td>Xoroshiro256</td><td>*xiroshiro256***</td><td>16 x 4-bytes</td><td>2^256</td><td>0</td><td>0</td><td>0</td><td>0.84</td><td>n.a.</td></tr>
<tr><td>Xoroshiro512</td><td>*xiroshiro512***</td><td>32 x 4-bytes</td><td>2^512</td><td>0</td><td>0</td><td>0</td><td>0.99</td><td>n.a.</td></tr>
<tr><td>Xoroshiro1024</td><td>*xiroshiro1024***</td><td>64 x 4-bytes</td><td>2^1,024</td><td>0</td><td>0</td><td>0</td><td>1.17</td><td>n.a.</td></tr>
</table>

(1) *or the generator original name in the related more recent paper*  
(2) The Well19937c generator provided with library PyRandLib implements the Well19937a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.  
(3) The Well44497b generator provided with library PyRandLib implements the Well44497a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.



## CPU Performances - Times evaluation

The above table provides times related to the C implementation of the specified PRNGs as measured with TestU01 [1] by the authors of the paper.  
We provide in the table below the evaluation of times spent in calling the `__call__()` method for all PRNGs implemented in library **PyRandLib**. Then, the measured elapsed time includes the calling and returning Python mechanisms and not only the computation time of the sole algorithm code. This is the duration of interest to you since this is the main use of the library you will have. It only helps comparing the performances between the implemented PRNGs and between the Python different versions.

Time unit is microsecond.  
* First table  
Tests have been run on an Intel&reg; Core&trade; i7-150U CPU @ 1.80 GHz, 10 cores, 64-bits, with 16 GB RAM and over Microsoft Windows 11 ed. Family (build 26100.4061, 18 Apr. 2025).  
* Second table  
Tests have been run on an Intel&reg; Core&trade; i5-1035G1 CPU @ 1.00 GHz, 4 cores, 8 logical processors, 64-bits, with 8 GB RAM and over Microsoft Windows 11 ed. Family.  

The evaluation script is provided at the root of **PyRandLib** repository: `testCPUPerfs.py`.

The Python versions used for these evaluations in their related virtual environment are (all 64-bits):
* 3.9.24 (Oct. 9, 2025)
* 3.10.19 (Oct. 9, 2025)
* 3.11.14 (Oct. 9, 2025)
* 3.12.12 (Oct. 9, 2025)
* 3.13.8 (Oct. 7, 2025)
* 3.14.0 (Oct. 7, 2025)

**PyRandLib** time-64 bits table, Intel&reg; Core&trade; **i7-150U** CPU @ 1.80 GHz:
<table>
<tr><th>PyRandLib class</th><th>Python 3.9</th><th>Python 3.10</th><th>Python 3.11</th><th>Python 3.12</th><th>Python 3.13</th><th>Python 3.14</th><th>SmallCrush fails</th><th>Crush fails</th><th>BigCrush fails</th></tr>
<tr><td>Cwg64</td><td>0.45</td><td>0.44</td><td>0.49</td><td>0.56</td><td>0.37</td><td>0.24</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Cwg128_64</td><td>0.47</td><td>0.46</td><td>0.50</td><td>0.59</td><td>0.38</td><td>0.26</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Cwg128</td><td>0.52</td><td>0.54</td><td>0.54</td><td>0.64</td><td>0.41</td><td>0.26</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>FastRand32</td><td>0.15</td><td>0.16</td><td>0.14</td><td>0.17</td><td>0.11</td><td>0.07</td><td>*11*</td><td>*106*</td><td>*too many*</td></tr>
<tr><td>FastRand63</td><td>0.16</td><td>0.17</td><td>0.16</td><td>0.18</td><td>0.11</td><td>0.08</td><td>*0*</td><td>*5*</td><td>*7*</td></tr>
<tr><td>LFib78</td><td>0.28</td><td>0.29</td><td>0.27</td><td>0.32</td><td>0.20</td><td>0.11</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib116</td><td>0.29</td><td>0.29</td><td>0.28</td><td>0.32</td><td>0.21</td><td>0.11</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib668</td><td>0.30</td><td>0.30</td><td>0.29</td><td>0.34</td><td>0.22</td><td>0.12</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib1340</td><td>0.31</td><td>0.31</td><td>0.30</td><td>0.35</td><td>0.22</td><td>0.13</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg607</td><td>0.73</td><td>0.74</td><td>0.73</td><td>0.79</td><td>0.61</td><td>0.50</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg19937</td><td>0.76</td><td>0.74</td><td>0.76</td><td>0.82</td><td>0.60</td><td>0.51</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg44497</td><td>0.75</td><td>0.76</td><td>0.77</td><td>0.82</td><td>0.62</td><td>0.52</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg287</td><td>0.46</td><td>0.48</td><td>0.44</td><td>0.51</td><td>0.34</td><td>0.21</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg1457</td><td>0.43</td><td>0.44</td><td>0.41</td><td>0.48</td><td>0.32</td><td>0.21</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg49507</td><td>0.44</td><td>0.45</td><td>0.42</td><td>0.48</td><td>0.34</td><td>0.24</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg64_32</td><td>0.30</td><td>0.31</td><td>0.28</td><td>0.32</td><td>0.22</td><td>0.19</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg128_64</td><td>0.45</td><td>0.46</td><td>0.44</td><td>0.49</td><td>0.34</td><td>0.30</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg1024_32</td><td>0.58</td><td>0.59</td><td>0.54</td><td>0.55</td><td>0.39</td><td>0.33</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Squares32</td><td>0.83</td><td>0.83</td><td>0.82</td><td>0.92</td><td>0.67</td><td>0.63</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Squares64</td><td>1.02</td><td>1.01</td><td>1.01</td><td>1.14</td><td>0.86</td><td>0.80</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Well512a</td><td>1.37</td><td>1.44</td><td>1.27</td><td>1.42</td><td>1.10</td><td>0.88</td><td>*n.a.*</td><td>*n.a.*</td><td>n.a.</td></tr>
<tr><td>Well1024a</td><td>1.27</td><td>1.31</td><td>1.17</td><td>1.29</td><td>1.00</td><td>0.83</td><td>*0*</td><td>*4*</td><td>*4*</td></tr>
<tr><td>Well19937c (1)</td><td>1.68</td><td>1.75</td><td>1.58</td><td>1.76</td><td>1.38</td><td>1.26</td><td>*0*</td><td>*2*</td><td>*2*</td></tr>
<tr><td>Well44497b (2)</td><td>1.91</td><td>1.99</td><td>1.80</td><td>2.02</td><td>1.63</td><td>1.43</td><td>*n.a.*</td><td>*n.a.*</td><td>n.a.</td></tr>
<tr><td>Xoroshiro256</td><td>1.39</td><td>1.38</td><td>1.31</td><td>1.47</td><td>1.06</td><td>0.98</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Xoroshiro512</td><td>1.70</td><td>1.67</td><td>1.60</td><td>1.77</td><td>1.37</td><td>1.17</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Xoroshiro1024</td><td>1.63</td><td>1.63</td><td>1.52</td><td>1.72</td><td>1.26</td><td>1.15</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
</table>

(1) The Well19937c generator provided with library PyRandLib implements the Well19937a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.  
(2) The Well44497b generator provided with library PyRandLib implements the Well44497a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.


**PyRandLib** time-64 bits table, Intel&reg; Core&trade; **i5-1035G1** CPU @ 1.00 GHz:
<table>
<tr><th>PyRandLib class</th><th>Python 3.9</th><th>Python 3.10</th><th>Python 3.11</th><th>Python 3.12</th><th>Python 3.13</th><th>Python 3.14</th><th>SmallCrush fails</th><th>Crush fails</th><th>BigCrush fails</th></tr>
<tr><td>Cwg64</td><td>0.79</td><td>0.77</td><td>0.84</td><td>0.97</td><td>0.76</td><td>0.48</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Cwg128_64</td><td>0.82</td><td>0.80</td><td>0.88</td><td>0.99</td><td>0.78</td><td>0.49</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Cwg128</td><td>0.89</td><td>0.94</td><td>0.96</td><td>1.13</td><td>0.83</td><td>0.52</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>FastRand32</td><td>0.27</td><td>0.27</td><td>0.26</td><td>0.31</td><td>0.21</td><td>0.14</td><td>*11*</td><td>*106*</td><td>*too many*</td></tr>
<tr><td>FastRand63</td><td>0.30</td><td>0.29</td><td>0.29</td><td>0.35</td><td>0.22</td><td>0.15</td><td>*0*</td><td>*5*</td><td>*7*</td></tr>
<tr><td>LFib78</td><td>0.52</td><td>0.49</td><td>0.50</td><td>0.56</td><td>0.35</td><td>0.21</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib116</td><td>0.53</td><td>0.51</td><td>0.51</td><td>0.57</td><td>0.36</td><td>0.22</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib668</td><td>0.55</td><td>0.52</td><td>0.53</td><td>0.60</td><td>0.39</td><td>0.24</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>LFib1340</td><td>0.55</td><td>0.53</td><td>0.55</td><td>0.62</td><td>0.41</td><td>0.25</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg607</td><td>1.30</td><td>1.31</td><td>1.26</td><td>1.40</td><td>1.15</td><td>0.98</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg19937</td><td>1.37</td><td>1.32</td><td>1.31</td><td>1.43</td><td>1.14</td><td>0.99</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Melg44497</td><td>1.33</td><td>1.35</td><td>1.32</td><td>1.42</td><td>1.16</td><td>0.99</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg287</td><td>0.86</td><td>0.84</td><td>0.82</td><td>0.91</td><td>0.61</td><td>0.37</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg1457</td><td>0.81</td><td>0.78</td><td>0.76</td><td>0.86</td><td>0.61</td><td>0.40</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Mrg49507</td><td>0.75</td><td>0.69</td><td>0.68</td><td>0.86</td><td>0.56</td><td>0.49</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg64_32</td><td>0.56</td><td>0.52</td><td>0.48</td><td>0.56</td><td>0.44</td><td>0.40</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg128_64</td><td>0.80</td><td>0.74</td><td>0.73</td><td>0.86</td><td>0.63</td><td>0.62</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Pcg1024_32</td><td>1.08</td><td>1.06</td><td>0.95</td><td>0.96</td><td>0.75</td><td>0.69</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Squares32</td><td>1.48</td><td>1.45</td><td>1.40</td><td>1.67</td><td>1.31</td><td>1.26</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Squares64</td><td>1.83</td><td>1.79</td><td>1.71</td><td>2.01</td><td>1.62</td><td>1.62</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Well512a</td><td>2.62</td><td>2.64</td><td>2.26</td><td>2.60</td><td>2.08</td><td>1.77</td><td>*n.a.*</td><td>*n.a.*</td><td>n.a.</td></tr>
<tr><td>Well1024a</td><td>2.28</td><td>2.36</td><td>1.98</td><td>2.24</td><td>1.87</td><td>1.60</td><td>*0*</td><td>*4*</td><td>*4*</td></tr>
<tr><td>Well19937c (1)</td><td>3.23</td><td>3.44</td><td>2.84</td><td>3.12</td><td>2.61</td><td>2.44</td><td>*0*</td><td>*2*</td><td>*2*</td></tr>
<tr><td>Well44497b (2)</td><td>3.66</td><td>3.91</td><td>3.18</td><td>3.55</td><td>2.92</td><td>2.82</td><td>*n.a.*</td><td>*n.a.*</td><td>n.a.</td></tr>
<tr><td>Xoroshiro256</td><td>2.37</td><td>2.24</td><td>2.25</td><td>2.55</td><td>1.93</td><td>1.87</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Xoroshiro512</td><td>2.94</td><td>2.81</td><td>2.72</td><td>3.04</td><td>2.30</td><td>2.27</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
<tr><td>Xoroshiro1024</td><td>2.78</td><td>2.59</td><td>2.41</td><td>3.01</td><td>2.06</td><td>2.23</td><td>*0*</td><td>*0*</td><td>*0*</td></tr>
</table>

(1) The Well19937c generator provided with library PyRandLib implements the Well19937a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.  
(2) The Well44497b generator provided with library PyRandLib implements the Well44497a algorithm augmented with an associated *tempering* algorithm - see [6] p.9.


## Implementation
Current implementation of **PyRandLib** uses Python 3.x with no Cython version.  

Note 1: **PyRandLib** version 1.1 and below should work with all versions of Python 3. In version 1.2, we have added underscores in numerical constants for the better readability of the code. This feature has been introduced in Python 3.6. If you want to use PyRandLib version 1.2 or above with Python 3.5 or below, removing these underscores should be sufficient to have the library running correctly. *N.B. You should no more use Python 3.10 or any of its previous versions since these are no more maintained (July 2025).*

Note 2: no version or **PyRandLib** will ever be provided for Python 2 which is a no more maintained version of the Python language.

Note 3: since release **2.0** of **PyRandLib** directories have been created that are each dedicated to a version of Python : 3.6, 3.9, 3.10, etc. Each of these directories contains the sub-directory `PyRandLib\` with a specific implementation of the library, optimized for the version of Python it relates to.

Note 4: since release **2.1** of **PyRandLib** unit tests are provided in subdirectories `unit-tests` for every available version of Python standard.

Note 5: a Cython version of **PyRandLib** will be delivered in a next major release (i.e. 3.0). Up today, no date is planned for this.


## New in Release 2.2
Version 2.2 of **PyRandLib** delivers a Python 3.14 version of the library. Note: no new feature introduced by Python 3.14 impacts the code of PyRandLib which is then the same for version 3.14 as for Python 3.13 - with very minor optimizations on code for a very few generators. Meanwhile, the implementation of Python 3.14 shows computation speed-ups from 6 % up to 48 % for the Intel&reg; Core&trade; i7 CPU (see related above table).


## New in Release 2.1
Version 2.1 of **PyRandLib** is now fully unit-tested. The code coverage is 100%. Test code is available in subdirectory `unit-tests` of every Python version directory.

A few bugs have then been fixed:
* protected method `Pcg1024_32._externalstep()` implementation is now correct;
* a typo in a shifting constant in Well19937c`.next()` has been fixed (19 -> 9).  
Release **2.0** of **PyRandLib** is nevertheless still available **but it should no more be used**.


### New in Release 2.0
Version 2.0 of **PyRandLib** implements some new other "recent" PRNGs - see them listed below. It also provides two test scripts, enhanced documentation and some other internal development features. Finally, it is splitted in many subdirectories each dedicated to a specific version of Python: Python3.6, Python3.9, Python3.10, etc. In each of these directories, library  **PyRandLib** code is fully copied and modified to take benefit of the improvements on new Python versions syntax and features. Copy the one version of value for your application to get all **PyRandLib** stuff at its best for your needs.

**Major 2.0 novelties are listed below:**

1. The WELL algorithm (Well-Equilibrated Long-period Linear, see [6], 2006) is now implemented in **PyRandLib**. This algorithm has proven to very quickly escape from the zeroland (up to 1,000 times faster than the Mersenne-Twister algorithm, for instance) while providing large to very large periods and rather small computation time.  
In **PyRandLib**, the WELL algorithm is provided in next forms: Well512a, Well1024a, Well19937c and Well44497b - they all generate output values coded on 32-bits.

1. The PCG algorithm (Permuted Congruential Generator, see [7], 2014) is now implemented in **PyRandLib**. This algorithm is a very fast and enhanced on randomness quality version of Linear Congruential Generators. It is based on solid Mathematics foundation and is clearly explained in technical report [7]. It offers jumping ahead, a hard to discover its internal state characteristic, and multi-streams feature. It passes all crush and big crush tests of TestU01.  
**PyRandLib** implements its 3 major versions with resp. 2^32, 2^64 and 2^128 periodicities: Pcg64_32, Pcg128_64 and Pcg1024_32 classes which generate output values coded on resp. 32-, 64- and 32- bits. The original library (C and C++) can be downloaded here: [https://www.pcg-random.org/downloads/pcg-cpp-0.98.zip](https://www.pcg-random.org/downloads/pcg-cpp-0.98.zip) as well as can its code be cloned from here: [https://github.com/imneme/pcg-cpp](https://github.com/imneme/pcg-cpp).

1. The CWG algorithm (Collatz-Weyl Generator, see [8], 2024) is now implemented in **PyRandLib**. This algorithm is fast, uses four integers as its internal state and generates chaos via multiplication and xored-shifted instructions. Periods are medium to large and the generated randomness is of up quality. It does not offer jump ahead but multi-streams feature is available via the simple modification of a well specified integer of its four integers state.  
In **PyRandLib**, the CWG algorithm is provided in next forms: Cwg64, Cwg64-128 and Cwg128 that  generate output values coded on resp. 64-, 64- and 128- bits .

1. The Squares algorithm (see "Squares: A Fast Counter-Based RNG" [9], 2022) is now implemented in **PyRandLib**. This algorithm is fast, uses two 64-bits integers as its internal state (a counter and a key), gets a period of 2^64 and runs through 4 to 5 rounds of squaring, exchanging high and low bits and xoring intermediate values. Multi-streams feature is available via the value of the key.  
In **PyRandLib**, the Squares32 and Squares64 versions of the algorithm are implemented. They provide resp. 32- and 64- bits output values. Caution: the 64-bits versions should not pass the birthday test, which is a randomness issue, while this is not mentionned in the original paper [9].

1. The xoroshiro algorithm ("Scrambled Linear Pseudorandom Number Generators", see [10], 2018) is now implemented in **PyRandLib**, in its *mult-mult* form for the output scrambler. This algorithm is fast, uses 64-bits integers as its internal state and outputs 64-bits values. It uses few memory space (4, 8 or 16 64-bits integers for resp. its 256-, 512- and 1024- versions that are implemented in **PyRandLib**. Notice: the 256 version of the algorithm is know to show close repeats flaws, with a bad Hamming weight near zero. *xoroshiro512* seems to best fit this property, according to the tables proposed by the authors in [10].

1. The MELG algorithm ("Maximally Equidistributed Long-period Linear Generators", see [11], 2018) is now implemented in **PyRandLib**. It can be considered as an extension of the WELL algorithm, with a maximization of the equidistribution of generated values, making computations on 64-bits integers and outputing 64-bits values.  
**PyRandLib** implements its versions numbered 627-64, 19937-64 and 44497-64 related to the power of 2 of their periods: Melg627, Melg19937 and Melg44497.

1. The SplitMix algorithm is now implemented in **PyRandLib**. It is used to initialize the internal state of all other PRNGs. It SHOULD NOT be used as a PRNG due to its random properties poorness.

1. Method `bytesrand()` has been added to the Python built-in class `random.Random` since Python 3.9. So, it is also available in **PyRandLib** for **all** its Python versions: in Python 3.6 its implementation has been added into base class `BaseRandom`.

1. Method `random.binomialvariate()`has been added to the Python built-in class `random.Random` since Python 3.12. So, it is also available in **PyRandLib** for **all** its Python versions: in Python -3.6, -3.9, -3.10 and -3.11 its implementation has been added into base class `BaseRandom`.

1. Since Python 3.12, a default value has been specified (i.e. = 1.0) for parameter `lambd` in method `random.Random.expovariate()`. So, it is also specified now in **PyRandLib** for **all** its Python versions: in Python -3.6, -3.9, -3.10 and -3.11 its definition has been added into base class `BaseRandom`.

1. A short script `testED.py` is now avalibale at root directory. It checks the equidistribution of every PRNG implemented in **PyRandLib** in a simple way and is used to test for their maybe bad implementation within the library. Since release 2.0 this test is run on all PRNGs.  
It is now **highly recommended** to not use previous releases of **PyRandLib**  (aka. 1.x).

1. Another short script `testCPUPerfs.py` is now avaliable for testing CPU performance of the different implemented algorithms. It has been used to enhance this documentation by providing a new *CPU Evaluations* table.

1. Documentation has been enhanced, with typos and erroneous docstrings fixed also.

1. All developments are now done under a newly created branch named `dev` (GitHub). This development branch may be derived into sub-branches for the development of new features. Merges from `dev` to branch `main` should only happen when creating new releases.  
So, if you want to see what is currently going on for next release of **PyRandLib**, just check-out branch `dev`.

1. A Github project dedicated to **PyRandLib** has been created: the [pyrandlib](https://github.com/users/schmouk/projects/14) project.


### New in Release 1.2
This is available starting at version 1.2 of **PyRandLib**.

The call  operator (i.e., '()') gets a new signature which is still backward compatible with previous versions of this library. Its new use is described here below. The implementation code can be found in class `BaseRandom`, in module `baserandom.py`.

    from fastrand63 import FastRand63
    
    rand = FastRand63()
    
    # prints a float random value ranging in [0.0, 1.0)
    print( rand() )
    
    # prints an integer random value ranging in [0, 5)
    print( rand(5) )
    
    # prints a float random value ranging in [0.0, 20.0)
    print( rand(20.0) )
    
    # prints a list of 10 integer values each ranging in [0, 5)
    print( rand(5, 10) )
    
    # prints a list of 10 float values each ranging in [0.0, 1.0)
    print( rand(times=10) )
    
    # prints a list of 4 random values ranging respectively in
    #    [0, 5), [0.0, 50.0), [0.0, 500.0) and [0, 5000)
    print( rand(5, 50.0, 500.0, 5000) )
    						
    # a more complex call which prints something like:
    #   [ [3, 11.64307079016269, 127.65395855782158, 4206, [2, 0, 1, 4, 4, 1, 2, 0]],
    #     [2, 34.22526698212995, 242.54183578253426, 2204, [5, 3, 5, 4, 2, 0, 1, 3]], 
    #     [0, 17.77303802057933, 417.70662295909983,  559, [4, 1, 5, 0, 5, 3, 0, 5]] ] 
    print( rand( (5, 50.0, 500.0, 5000, [5]*8), times=3 ) )


## Software architecture overview
Each of the implemented PRNG is described in an independent module. The  name of the module is directly related to the name of the related class.


### BaseRandom  -  the base class for all PRNGs

**BaseRandom** is the base class for every implemented PRNG in library **PyRandLib**. It inherits from the Python built-in class `random.Random`. It aims at providing simple common behavior for all PRNG classes of the library, the most noticeable one being the 'callable' nature of every implemented PRNG.

Inheriting from the Python built-in class random.Random, **BaseRandom** provides access to many useful distribution functions as described in later section **Inherited Distribution and Generic Methods**.

Furthermore, every inheriting class MUST override the next three methods (if not, they each raise a `NotImplementedError` exception when called):

* next(),
* getstate() and
* setstate()

and may override the next three methods:

* random(),
* seed(),
* getrandbits(),

Notice: starting at PyRandLib 1.2.0, a new signature is available with this base class. See previous section 'New in release 1.2' for full explanations.

Notice: Since PyRandLib 2.0, class `BaseRandom` implements the new method `next()` which is substituted to `random()`. `next()` should now contain the core of the pseudo-random numbers generator while `random()` calls it to return a float value in the interval [0.0, 1.0), just as did all previous versions of the library.  
Since version 2.0 of PyRandLib also, the newly implemented method `getrandbits()` overrides the same method of Python built-in base class `random.Random`.



### Cwg64  -  minimum 2^70 period

**Cwg64** implements the full 64 bits version of the Collatz-Weyl Generator algorithm: computations are done on 64-bits, the output generated value is coded on 64-bits also. It provides a medium period which is at minimum 2^70 (i.e. about 1.18e+21), short computation time and a four 64-bits integers internal state (x, a, weyl, s).

This version of the CGW algorithm evaluates pseudo-random suites *output(i)* as the combination of the next instructions applied to *state(i-1)*:

    a(i)      = a(i-1) + x(i-1)
    weyl(i)   = weyl(i-1) + s  // s is constant over time and must be odd, this is the value to modify to get multi-streams
    x(i)      = ((x(i-1) >> 1) * ((a(i)) | 1)) ^ (weyl(i)))
    output(i) = (a(i) >> 48) ^ x(i)



### Cwg128_64  -  minimum 2^71 period

**Cwg128_64** implements the mixed 128/64 bits version of the Collatz-Weyl Generator algorithm: computations are done on 128- and 64-bits, the output generated value is coded on 64-bits also. It provides a medium period which is at minimum 2^71 (i.e. about 2.36e+21), short computation time and a three 64-bits (a, weyl, s) plus one 128-bits integer internal state (x). 

This version of the CGW algorithm evaluates pseudo-random suites *output(i)* as the combination of the next instructions applied to *state(i-1)*:

    a(i)      = a(i-1) + x(i-1)
    weyl(i)   = weyl(i+1) + s  // s is constant over time and must be odd, this is the value to modify to get multi-streams
    x(i)      = ((x(i-1) | 1) * (a(i) >> 1)) ^ (weyl(i))
    output(i) = (a(i) >> 48) ^ x(i)



### Cwg128  -  minimum 2^135 period

**Cwg128** implements the full 128 bits version of the Collatz-Weyl Generator algorithm: computations are done on 128-bits, the output generated value is coded on 128-bits also. It provides a medium period which is at minimum 2^135 (i.e. about 4.36e+40), short computation time and a four 128-bits integers internal state (x, a, weyl, s).

This version of the CGW algorithm evaluates pseudo-random suites *output(i)* as the combination of the next instructions applied to *state(i-1)*:

    a(i)      = a(i-1) + x(i-1)
    weyl(i)   = weyl(i-1) + s  // s is constant over time and must be odd, this is the value to modify to get multi-streams
    x(i)      = ((x(i-1) >> 1) * ((a(i)) | 1)) ^ (weyl(i)))
    output(i) = (a(i) >> 96) ^ x(i)



### FastRand32  -  2^32 periodicity

**FastRand32** implements a Linear Congruential Generator dedicated to 32-bits calculations with very short period (about 4.3e+09) but very short 
time computation.

LCG models evaluate pseudo-random numbers suites *x(i)* as a simple mathematical function of *x(i-1)*:

    x(i) = ( a * x(i-1) + c ) mod m 
   
The implementation of **FastRand32** is based on  (*a*=69069, *c*=1)  since these two values have evaluated to be the 'best' ones for LCGs within TestU01 with m = 2^32.
 
Results are nevertheless considered to be poor as stated in the evaluation done by Pierre L'Ecuyer and Richard Simard. Therefore, it is not recommended to use such pseudo-random numbers generators for serious simulation applications.



### FastRand63  -  2^63 periodicity

**FastRand63** implements a Linear Congruential Generator dedicated to  63-bits calculations with a short period (about 9.2e+18) and very short time computation.

LCG model  evaluate pseudo-random numbers suites *x(i)* as a simple mathematical function of *x(i-1)*:

    x(i) = ( a * x(i-1) + c ) mod m 
   
The implementation of this LCG 63-bits model is based on (*a*=9219741426499971445, *c*=1) since these two values have evaluated to be the *best* ones for LCGs within TestU01 while *m* = 2^63.
 
Results are nevertheless considered to be poor as stated in the evaluation done by Pierre L'Ecuyer and Richard Simard. Therefore, it is not recommended to use this pseudo-random numbers generatorsfor serious simulation applications, even if FastRandom63 fails on very far less tests than does FastRandom32.



### LFibRand78  -  2^78 periodicity

**LFibRand78** implements a fast 64-bits Lagged Fibonacci generator (LFib). Lagged Fibonacci generators *LFib( m, r, k, op)* use the recurrence

    x(i) = ( x(i-r) op (x(i-k) ) mod m

where op is an operation that can be
    + (addition),
    - (substraction),
    * (multiplication),
    ^(bitwise exclusive-or).

With the + or - operation, such generators are MRGs. They offer very large periods  with the best known results in the evaluation of their randomness, as stated in the evaluation done by Pierre L'Ecuyer and Richard Simard while offering very low computation times.

The implementation of  **LFibRand78** is based on a Lagged Fibonacci generator (LFib) which uses the recurrence:

    x(i) = ( x(i-5) + x(i-17) ) mod 2^64

It offers a period of about 2^78 - i.e. 3.0e+23 - with low computation time due to the use of a 2^64 modulo (less than twice the computation time of LCGs) and low memory consumption (17 integers 32-bits coded).

Please notice that the TestU01 article states that the operator should be '*' while George Marsaglia in its original article [4] used the operator '+'. We've implemented in **PyRandLib** the original operator '+'.



### LFibRand116  -  2^116 periodicity

**LFibRand116** implements an LFib 64-bits generator proposed by George Marsaglia in [4]. This PRNG uses the recurrence

    x(i) = ( x(i-24) + x(i-55) ) mod 2^64
    
It offers a period of about 2^116 - i.e. 8.3e+34 - with low computation time due to the use of a 2^64 modulo (less than twice the computation time of LCGs) and some memory consumption (55 integers 32-bits coded).

Please notice that the TestU01 article states that the operator should be '*' while George Marsaglia in its original article [4] used the operator '+'. We've implemented in **PyRandLib**  the original operator '+'.



### LFibRand668  -  2^668 periodicity

**LFibRand668** implements an LFib 64-bits generator proposed by George Marsaglia in [4]. This PRNG uses the recurrence

    x(i) = ( x(i-273) + x(i-607) ) mod 2^64
    
It offers a period of about 2^668 - i.e. 1.2e+201 - with low computation time due to the use of a 2^64 modulo (less than twice the computation time of LCGs) and much memory consumption (607 integers 32-bits coded).

Please notice that the TestU01 article states that the operator should be '*' while George Marsaglia in its original article [4] used the operator '+'. We've implemented in **PyRandLib**  the original operator '+'.



### LFibRand1340  -  2^1,340 periodicity

**LFibRand1340** implements an LFib 64-bits generator proposed by George Marsaglia in [4]. This PRNG uses the recurrence

    x(i) = ( x(i-861) + x(i-1279) ) mod 2^64
    
It offers a period of about 2^1340 - i.e. 2.4e+403 - with low computation time due to the use of a 2^64 modulo (less than twice the computation time of LCGs) and much more memory consumption (1279 integers 32-bits coded).

Please notice that the TestU01 article states that the operator should be '*' while George Marsaglia in its original article [4] used the operator '+'. We've implemented in **PyRandLib**  the original operator '+'.



### Melg627 --  2^627 periodicity

**Melg627** implements a fast 64-bits Maximally Equidistributed Long-period Linear Generator (MELG) with a large period (2^627, i.e. 5.31e+182) and low computation time. The internal state of this PRNG is equivalent to 21 integers 32-bits coded.

The base MELG algorithm mixes, xor's and shifts its internal state and offers large to very large periods with the best known results in the evaluation of their randomness. It escapes the zeroland at a fast pace. Its specializations are set with parameters that ensures the maximized equidistribution. It might be valuable to use these rather than the WELL algorithm derivations



### Melg19937 --  2^19937 periodicity

**Melg19937** implements a fast 64-bits Maximally Equidistributed Long-period Linear Generator (MELG) with a large period (2^19,937, i.e. 4.32e+6,001) and low computation time. The internal state of this PRNG is equivalent to 625 integers 32-bits coded.

The base MELG algorithm mixes, xor's and shifts its internal state and offers large to very large periods with the best known results in the evaluation of their randomness. It escapes the zeroland at a fast pace. Its specializations are set with parameters that ensures the maximized equidistribution. It might be valuable to use these rather than the WELL algorithm derivations



### Melg44497 --  2^44497 periodicity

**Melg44497** implements a fast 64-bits Maximally Equidistributed Long-period Linear Generator (MELG) with a very large period (2^44,497,  i.e. 8.55e+13,395) and low computation time. The internal state of this PRNG is equivalent to 1.393 integers 32-bits coded.

The base MELG algorithm mixes, xor's and shifts its internal state and offers large to very large periods with the best known results in the evaluation of their randomness. It escapes the zeroland at a fast pace. Its specializations are set with parameters that ensures the maximized equidistribution. It might be valuable to use these rather than the WELL algorithm derivations



### Mrg287  -  2^287 periodicity

**Mrg287** implements a fast 32-bits Multiple Recursive Generator (MRG) with a long period  (2^287, i.e. 2.49e+86) and low computation time (about twice the computation time of above LCGs) but 256 integers 32-bits coded memory consumption.

Multiple Recursive Generators (MRGs) use recurrence to evaluate pseudo-random numbers suites. For 2 to more different values of *k*, recurrence is of the form:

    x(i) = A * SUM[ x(i-k) ]  mod M

MRGs offer very large periods with the best known results in the evaluation of their randomness, as evaluated by Pierre L'Ecuyer and Richard Simard in [1]. It is therefore strongly recommended to use such pseudo-random numbers generators rather than LCG ones for serious simulation applications.

The implementation of this specific MRG 32-bits model is finally based on a Lagged Fibonacci generator (LFIB), the Marsa-LFIB4 one.

Lagged Fibonacci generators *LFib( m, r, k, op)* use the recurrence

    x(i) = ( x(i-r) op (x(i-k) ) mod m

where op is an operation that can be
    + (addition),
    - (substraction),
    * (multiplication),
    ^(bitwise exclusive-or).
    
With the + or - operation, such generators are true MRGs. They offer very large periods with the best known results in the evaluation of their randomness, as evaluated by Pierre L'Ecuyer and Richard Simard in their paper.

The Marsa-LIBF4 version, i.e. **Mrg287** implementation, uses the recurrence:

    x(i) = ( x(i-55) + x(i-119) + x(i-179) + x(i-256) ) mod 2^32



### Mrg1457  -  2^1,457 periodicity

**Mrg1457** implements a fast 31-bits Multiple Recursive Generator with a longer period than MRGRan287 (2^1457 vs. 2^287, i.e. 4.0e+438 vs. 2.5e+86) and 80 % more computation time but with much less memory space consumption (47 vs. 256 integers 32-bits coded).
   
The implementation of this MRG 31-bits model is based on  DX-47-3 pseudo-random generator proposed by Deng and Lin, see [2]. The DX-47-3 version uses the recurrence:

    x(i) = (2^26+2^19) * ( x(i-1) + x(i-24) + x(i-47) ) mod (2^31-1)

See Mrg287 above description for an explanation of the MRG original algorithm.



### Mrg49507  -  2^49,507 periodicity

**Mrg49507** implements a fast 31-bits Multiple Recursive Generator with the longer period of all of the PRNGs that are implemented in **PyRandLib** (2^49,507, i.e. 1.2e+14,903) with low computation time also (same as for Mrg287) but use of much more memory space (1,597 integers 32-bits coded).
     
The implementation of this MRG 31-bits model is based on the 'DX-1597-2-7' MRG proposed by Deng, see [3]. It uses the recurrence:

    x(i) = (-2^25-2^7) * ( x(i-7) + x(i-1597) ) mod (2^31-1)

See Mrg287 above description for an explanation of the MRG original algorithm.



### Pcg64_32  -  2^64 periodicity

**Pcg64_32** implements a fast 64-bits state and 32-bits output Permutated Congruential Generator with a medium period (2^64, i.e. 1.84e+19) with low computation time and very small memory space consumption (2 integers 32-bits coded).

The underlying algorithm acts as an LCG associated with a bits permutation as its final step before outputing next random value. It is known to succesfully pass all TestU01 tests. It provides multi streams and jump ahead features and is hard to be reverted and predicted.  
**PyRandLib** implements for ths the *PCG XSH RS 64/32 (LCG)* version of the PCG algorithm, as explained in [7] and coded in c++ on www.pcg-random.org.



### Pcg128_64  -  2^128 periodicity

**Pcg128_64** implements a fast 128-bits state and 64-bits output Permutated Congruential Generator with a medium period (2^128, i.e. 3.40e+38) with low computation time and very small memory space consumption (4 integers 32-bits coded).

The underlying algorithm acts as an LCG associated with a bits permutation as its final step before outputing next random value. It is known to succesfully pass all TestU01 tests. It provides multi streams and jump ahead features and is very hard to be reverted and predicted.  
**PyRandLib** implements for this the *PCG XSL RR 128/64 (LCG)* version of the PCG algorithm, as explained in [7] and coded in c++ on www.pcg-random.org.



### Pcg1024_32  -  2^32,830 periodicity

**Pcg1024_32** implements a fast 64-bits based state and 32-bits output Permutated Congruential Generator with a very large period (2^32,830, i.e. 6.53e+9,882) with low computation time and large memory space consumption (1,026 integers 32-bits coded).

The underlying algorithm acts as an LCG associated with a bits permutation as its final step before outputing next random value, and an array of 32-bits independant MCG (multiplied congruential generators) used to create huge chaos. It is known to succesfully pass all TestU01 tests. It provides multi streams and jump ahead features and is very hard to be reverted and predicted.  
**PyRandLib** implements for this the *PCG XSH RS 64/32 (EXT 1024)* version of the PCG algorithm, as explained in [7] and coded in c++ on www.pcg-random.org.



### Squares32  -  2^64 periodicity

**Squares32** implements a fast counter-based pseudo-random numbers generator which outputs 32-bits random values. The core of the algorithm evaluates and squares 64-bits intermadiate values then exchanges their higher and lower bits on a four rounds operations. It uses a 64-bits counter and a 64-bits key. It provides multi-streams feature via different values of key and gets robust randomness characteristics. The counter starts counting at 0. Once returning to 0 modulo 2^64 the whole period of the algorithm will have been exhausted. Values for keys have to be cautiously chosen: the **PyRandLib** implementation of the manner to do it as recommended in [9] is of our own but stricly respects the original recommendation.  
**PyRandLib** Squares32 class implements the *squares32* version of the algorithm as described in [9]. 



### Squares64  -  2^64 periodicity

**Squares64** implements a fast counter-based pseudo-random numbers generator which outputs 64-bits random values. The core of the algorithm evaluates and squares 64-bits intermadiate values then exchanges their higher and lower bits on a five rounds operations. It uses a 64-bits counter and a 64-bits key. It provides multi-streams feature via different values of key and gets robust randomness characteristics. The counter starts counting at 0. Once returning to 0 modulo 2^64 the whole period of the algorithm will have been exhausted. Values for keys have to be cautiously chosen: the **PyRandLib** implementation of the manner to do it as recommended in [9] is of our own but stricly respects the original recommendation.  
Notice: this version of the algorithm should not pass the birthday test, which is a randomness issue, while this is not mentionned in the original paper [9].  
**PyRandLib** Squares64 class implements the *squares64* version of the algorithm as described in [9]. 



### Well512a  -  2^512 periodicity

**Well512a** implements the Well-Equilibrated Long-period Linear generators (WELL) proposed by François Panneton, Pierre L'ECcuyer and Makoto Matsumoto in [6]. This PRNG uses linear recurrence based on primitive characteristic polynomials associated with left- and right- shifts and xor operations to fastly evaluate pseudo-random numbers suites.

It offers a long period of value 2^252 - i.e. 1.34e+154 - with short computation time and 16 integers 32-bits coded memory consumption.  
It escapes the zeroland at a fast pace.  
Meanwhile, it should not be able to pass some of the *crush* and *big-crush* tests of TestU01 - notice: this version of the WELL algorithm has not been tested in original TestU01 paper.



### Well1024a  -  2^1,024 periodicity

**Well1024a** implements the Well-Equilibrated Long-period Linear generators (WELL) proposed by François Panneton, Pierre L'ECcuyer and Makoto Matsumoto in [6]. This PRNG uses linear recurrence based on primitive characteristic polynomials associated with left- and right- shifts and xor operations to fastly evaluate pseudo-random numbers suites.

It offers a long period of value 2^1,024 - i.e. 2.68+308 - with short computation time and 32 integers 32-bits coded memory consumption.  
It escapes the zeroland at a fast pace.  
Meanwhile, it does not pass 4 of the *crush* and 4 of the *big-crush* tests of TestU01.



### Well199937c  -  2^19,937 periodicity

**Well199937c** implements the Well-Equilibrated Long-period Linear generators (WELL) proposed by François Panneton, Pierre L'ECcuyer and Makoto Matsumoto in [6]. This PRNG uses linear recurrence based on primitive characteristic polynomials associated with left- and right- shifts and xor operations to fastly evaluate pseudo-random numbers suites.

It offers a long period of value 2^19,937 - i.e. 4.32e+6,001 - with short computation time and 624 integers 32-bits coded memory consumption - just     s the Mersenne-Twister algorithm).  
It escapes the zeroland at a very fast pace.  
Meanwhile, it does not pass 2 of the *crush* and 2 of the *big-crush* tests of TestU01.



### Well44497b  -  2^44,497 periodicity

**WellWell44497b** implements the Well-Equilibrated Long-period Linear generators (WELL) proposed by François Panneton, Pierre L'ECcuyer and Makoto Matsumoto in [6]. This PRNG uses linear recurrence based on primitive characteristic polynomials associated with left- and right- shifts and xor operations to fastly evaluate pseudo-random numbers suites.

It offers a long period of value 2^44,497 - i.e. 1.51e+13,466 - with short computation time and 1,391 integers 32-bits coded memory consumption.  
It escapes the zeroland at a fast pace.  
Meanwhile, it might not be able to pass a very few of the *crush* and *big-crush* tests of TestU01, while it can be expected to better behave than the Well19937c version - notice: this version of the WELL algorithm has not been tested in original TestU01 paper.



### Xoroshiro256  - 2^256 periodicity

**Xoroshiro256** implements version *xoroshiro256*** of the Scrambled Linear Pseudorandom Number Generators algorithm proposed by David Blackman and Sebastiano Vigna in [10]. This xoroshiro linear transformation updates cyclically two words of a 4 integers state array. The base xoroshiro linear transformation is obtained combining a rotation, a shift, and again a rotation. It also applies a double multiplication as the scrambler model before outputing values. Internal state and output values are coded on 64 bits.

It offers a medium period of value 2^256 - i.e. 1.16e+77 - with short computation time and 4 integers 64-bits coded memory consumption.  
It escapes the zeroland at a very fast pace (about 10 loops) and offers jump-ahead feature. Notice: the 256 version of the algorithm has shown close repeats flaws, with a bad Hamming weight near zero as explained by the authors in [10] and explained in [https://www.pcg-random.org/posts/xoshiro-repeat-flaws.html](https://www.pcg-random.org/posts/xoshiro-repeat-flaws.html).



### Xoroshiro512  - 2^512 periodicity

**Xoroshiro512** implements version *xoroshiro512*** of the Scrambled Linear Pseudorandom Number Generators algorithm proposed by David Blackman and Sebastiano Vigna in[10]. This xoroshiro linear transformation updates cyclically two words of a 8 integers state array. The base xoroshiro linear transformation is obtained combining a rotation, a shift, and again a rotation. It also applies a double multiplication as the scrambler model before outputing values. Internal state and output values are coded on 64 bits.

It offers a medium period of value 2^512 - i.e. 1.34e+154 - with short computation time and 4 integers 64-bits coded memory consumption.  
It escapes the zeroland at a very fast pace (about 30 loops) and offers jump-ahead feature.



### Xoroshiro1024  - 2^1,024 periodicity

**Xoroshiro** implements version *xoroshiro1024*** of the Scrambled Linear Pseudorandom Number Generators algorithm proposed by David Blackman and Sebastiano Vigna in[10]. This xoroshiro linear transformation updates cyclically two words of a 16 integers state array and a 4 bits index. The base xoroshiro linear transformation is obtained combining a rotation, a shift, and again a rotation. It also applies a double multiplication as the scrambler model before outputing values. Internal state and output values are coded on 64 bits.

It offers a medium period of value 2^1,024 - i.e. 1.80e+308 - with short computation time and 4 integers 64-bits coded memory consumption.  
It escapes the zeroland at a fast pace (about 100 loops) and offers jump-ahead feature.



## Inherited Distribution and Generic Methods
(some of next explanation may be either free or exact copy of Python documentation.

Since the base class **BaseRandom** inherits from the built-in class `random.Random`, every PRNG class of **PyRandLib** gets automatic access to the next distribution and generic methods:


**betavariate**(self, alpha, beta)  
Beta distribution.

Conditions on the parameters are `alpha > 0` and `beta > 0`.  
Returned values range between 0 and 1.


**binomialvariate**(self, n=1, p=0.5)  
Binomial distribution. Return the number of successes for `n` independent trials with the probability of success in each trial being `p`:

Mathematically equivalent to:

    sum(random() < p for i in range(n))

The number of trials `n` should be a non-negative integer. The probability of success `p` should be between `0.0 <= p <= 1.0`. The result is an integer in the range `0 <= X <= n`. This built-in method has been added since Python 3.12. **PyRandLIb** implements it also for all former versions of Python: -3.6, -3.9, -3.10, and -3.11.


**choice**(self, seq)  
Chooses a random element from a non-empty sequence. `seq` has to be non empty.


**choices**(self, population, weights=None, *, cum_weights=None, k=1)  
Returns a `k` sized list of elements chosen from the population, with replacement. If the population is empty, raises `IndexError`.

If a `weights` sequence is specified, selections are made according to  the relative weights. Alternatively, if a `cum_weights` sequence is given, the selections are made according to the cumulative weights (perhaps  computed using `itertools.accumulate()`).  
For example, the relative weights `[10, 5, 30, 5]` are equivalent to the cumulative weights `[10, 15, 45, 50]`.  
Internally, the relative weights are converted to cumulative weights before making selections, so supplying the cumulative weights saves work.

If neither `weights` nor `cum_weights` are specified, selections are made with equal probability. If a `weights` sequence is supplied, it must be the same length as the population sequence. It is a `TypeError` to specify both `weights` and `cum_weights`.

The `weights` or `cum_weights` can use any numeric type that interoperates with the float values returned by random() (that includes integers, floats, and fractions but excludes decimals).

Notice: `choices` has been provided since Python 3.6. It should be implemented for older versions.


**expovariate**(self, lambd=1.0)  
Exponential distribution.

`lambd` is 1.0 divided by the desired mean. It should be nonzero. (The parameter should be called "lambda", but this is a reserved word in Python).  
Returned values range from 0 to positive infinity if `lambd` is positive, and from negative infinity to 0 if `lambd` is negative.  
Since Python 3.12, the parameter `lambd` gets a default value in this built-in method. **PyRandLib** defines then this method for all former versions of Python : -3.6, -3.9, -3.10 and -3.11.


**gammavariate**(self, alpha, beta)  
Gamma distribution. Not the gamma function!
    
Conditions on the parameters are `alpha` > 0 and `beta` > 0.


**gauss**(self, mu, sigma)  
Gaussian distribution.

`mu` is the mean, and `sigma` is the standard deviation.  
This is slightly faster than the `normalvariate()` function.

Not thread-safe without a lock around calls.


**getrandbits**(self, k)  
Returns a Python integer with k random bits. Inheriting generators may also provide it as an optional part of their API.  When available, `getrandbits()` enables `randrange()` to handle arbitrarily large ranges.


**getstate**(self)  
Returns internal state; can be passed to `setstate()` later.


**lognormvariate**(self, mu, sigma)  
Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a normal distribution with mean `mu` and standard deviation `sigma`.  
`mu` can have any value, and `sigma` must be greater than zero.


**normalvariate**(self, mu, sigma)  
Normal distribution.

`mu` is the mean, and `sigma` is the standard deviation. See method `gauss()` for a faster but not thread-safe equivalent.


**paretovariate**(self, alpha)  
Pareto distribution. `alpha` is the shape parameter.


**randint**(self, a, b)  
Returns a random integer in range `[a, b]`, including both end points.


**randrange**(self, stop)  
**randrange**(self, start, stop=None, step=1)  
Returns a randomly selected element from range(start, stop, step). This is equivalent to `choice( range(start, stop, step) )` without building a range object.

The positional argument pattern matches that of `range()`. Keyword arguments should not be used because the function may use them in unexpected ways.


**sample**(self, population, k)  
Chooses `k` unique random elements from a population sequence or set.

Returns a new list containing elements from the population while leaving the original population unchanged. The resulting list is in selection order so that all sub-slices will also be valid random samples. This allows raffle winners (the sample) to be partitioned into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique. If the population contains repeats, then each occurrence is a possible selection in the sample.

To choose a sample in a range of integers, use range as an argument. This is especially fast and space efficient for sampling from a large population: `sample(range(10_000_000), 60)`.


**seed**(self, a=None, version=2)  
Initialize internal state from hashable object.

None or no argument seeds from current time, or from an operating system specific randomness source if available.

For version 2 (the default), all of the bits are used if `a` is a str, bytes, or bytearray. For version 1, the hash() of `a` is used instead.

If `a` is an int, all bits are used.


**setstate**(self, state)  
Restores internal state from object returned by `getstate()`.


**shuffle**(self, x, random=None)  
Shuffle the sequence `x` in place. Returns None.

The optional argument `random` is a 0-argument function returning a random float in `[0.0, 1.0)`; by default, this is the function random().

To shuffle an immutable sequence and return a new shuffled list, use `sample(x, k=len(x))` instead.

Note that even for small `len(x)`, the total number of permutations of `x` can quickly grow larger than the period of most random number generators.  This implies that most permutations of a long sequence can never be  generated. For example, a sequence of length 2080 is the largest that can fit within the period of the Mersenne Twister random number generator.


**triangular**(self, low=0.0, high=1.0, mode=None)  
Triangular distribution.

Continuous distribution bounded by given lower and upper limits, and having a given mode value in-between. Returns a random floating point number *N* such that `low` <= *N* <= `high` and with the specified mode  between those bounds. The `low` and `high` bounds default to zero and one. The mode argument defaults to the midpoint between the bounds, giving a symmetric distribution.

see [http://en.wikipedia.org/wiki/Triangular_distribution](http://en.wikipedia.org/wiki/Triangular_distribution)


**uniform**(self, a, b)  
Gets a random number in the range `[a, b)` or `[a, b]` depending on rounding.


**vonmisesvariate**(self, mu, kappa)  
Circular data distribution.

`mu` is the mean angle, expressed in radians between `0` and `2*pi`, and `kappa` is the  concentration parameter, which must be greater than or equal to zero. If `kappa` is equal to zero, this distribution reduces to a uniform random angle over the range `0` to `2*pi`.


**weibullvariate**(self, alpha, beta)  
Weibull distribution.

`alpha` is the scale parameter and `beta` is the shape parameter.



## References

**[1]** Pierre L'Ecuyer and Richard Simard. 2007.  
*TestU01: A C library for empirical testing of random number generators*.  
In ACM Transaction on Mathematical Software, Vol.33 N.4, Article 22 (August 2007), 40 pages.  
DOI: http://dx.doi.org/10.1145/1268776.1268777  
BibTex:
@article{L'Ecuyer:2007:TCL:1268776.1268777,
 author = {L'Ecuyer, Pierre and Simard, Richard},
 title = {TestU01: A C Library for Empirical Testing of Random Number Generators},
 journal = {ACM Trans. Math. Softw.},
 issue_date = {August 2007},
 volume = {33},
 number = {4},
 month = aug,
 year = {2007},
 issn = {0098-3500},
 pages = {22:1--22:40},
 articleno = {22},
 numpages = {40},
 url = {http://doi.acm.org/10.1145/1268776.1268777},
 doi = {10.1145/1268776.1268777},
 acmid = {1268777},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Statistical software, random number generators, random number tests, statistical test},
}  


**[2]** Lih-Yuan Deng & Dennis K. J. Lin. 2000.  
*Random number generation for the new century*.  
The American Statistician Vol.54, N.2, pp. 145–150.
BibTex:
@article{doi:10.1080/00031305.2000.10474528,
author = { Lih-Yuan   Deng  and  Dennis K. J.   Lin },
title = {Random Number Generation for the New Century},
journal = {The American Statistician},
volume = {54},
number = {2},
pages = {145-150},
year = {2000},
doi = {10.1080/00031305.2000.10474528},
URL = {http://amstat.tandfonline.com/doi/abs/10.1080/00031305.2000.10474528},
eprint = {http://amstat.tandfonline.com/doi/pdf/10.1080/00031305.2000.10474528}
}


**[3]** Lih-Yuan Deng. 2005.  
*Efficient and portable multiple recursive generators of large order*.  
In ACM Transactions on Modeling and Computer Simulation, Jan. 2005, Vol. 15 Issue 1, pp. 1-13.  
DOI: https://doi.org/10.1145/1044322.1044323


**[4]** Georges Marsaglia. 1985.  
*A current view of random number generators*.  
In Computer Science and Statistics, Sixteenth Symposium on the Interface.  
Elsevier Science Publishers, North-Holland, Amsterdam, 1985, The Netherlands, pp. 3–10.


**[5]** Makoto Matsumoto and Takuji Nishimura. 1998.  
*Mersenne twister: A 623-dimensionally equidistributed uniform pseudo-random number generator.*  
In ACM Transactions on Modeling and Computer Simulation (TOMACS) - Special issue on uniform random number generation. Vol.8 N.1, Jan. 1998, pp. 3-30.  


**[6]** François Panneton and Pierre L'Ecuyer (Université de Montréal) and Makoto Matsumoto (Hiroshima University). 2006.  
*Improved Long-Period Generators Based on Linear Recurrences Modulo 2*.  
In ACM Transactions on Mathematical Software, Vol. 32, No. 1, March 2006, pp. 1–16.  
see [https://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf](https://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf).


**[7]** Melissa E. O'Neill. 2014.  
*PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation*.  
Submitted to ACM Transactions on Mathematical Software (47 pages)  
Finally: Harvey Mudd College Computer Science Department Technical Report, HMC-CS-2014-0905, Issued: September 5, 2014 (56 pages).  
@techreport{oneill:pcg2014,
    title = "PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation",
    author = "Melissa E. O'Neill",
    institution = "Harvey Mudd College",
    address = "Claremont, CA",
    number = "HMC-CS-2014-0905",
    year = "2014",
    month = Sep,
    xurl = "https://www.cs.hmc.edu/tr/hmc-cs-2014-0905.pdf",
}  
see also [https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf).


**[8]** Tomasz R. Dziala. 2023.  
*Collatz-Weyl Generators: High Quality and High Throughput Parameterized Pseudorandom Number Generators*.  
Published at arXiv, December 2023 (11 pages),  
Last reference: arXiv:2312.17043v4 [cs.CE], 2 Dec 2024, see [https://arxiv.org/abs/2312.17043](https://arxiv.org/abs/2312.17043)  
DOI: https://doi.org/10.48550/arXiv.2312.17043


**[9]** Bernard Widynski. March 2022.  
*Squares: A Fast Counter-Based RNG*.  
Published at arXiv, March 2022 (5 pages)  
Last reference: arXiv:2004.06278v7 [cs.DS] 13 Mar 2022, see [https://arxiv.org/pdf/2004.06278](https://arxiv.org/pdf/2004.06278).  
DOI: https://doi.org/10.48550/arXiv.2004.06278


**[10]** David Blackman, Sebastiano Vigna. 2018.  
*Scrambled Linear Pseudorandom Number Generators*.  
Published in arXiv, March 2022 (32 pages)  
Last reference: arXiv:1805.01407v3 [cs.DS] 28 Mar 2022, see [https://arxiv.org/pdf/1805.01407](https://arxiv.org/pdf/1805.01407).  
DOI: https://doi.org/10.48550/arXiv.1805.01407


**[11]** Shin Harase, Takamitsu Kimoto, 2018.  
*Implementing 64-bit Maximally Equidistributed F2-Linear Generators with Mersenne Prime Period*.  
In ACM Transactions on Mathematical Software, Volume 44, Issue 3, April 2018, Article No. 30 (11 Pages)  
Also published in arXiv, March 2022 (11 pages)  
Last reference: arXiv:1505.06582v6 [cs.DS] 20 Nov 2017, see [https://arxiv.org/pdf/1505.06582](https://arxiv.org/pdf/1505.06582).  
DOI: https://doi.org/10.1145/3159444, https://doi.org/10.48550/arXiv.1505.06582


**[12]** Marsaglia, G. 1972.  
*The structure of linear congruential sequences.*  
In Applications of Number Theory to Numerical Analysis, S. K. Zaremba, Ed. Academic Press, 249–285.


**[13]** Brown, F. B. and Nagaya, Y. 2002.  
*The MCNP5 random number generator.*  
Tech. rep. LA-UR-02-3782, Los Alamos National Laboratory
