Multi-dimensional parameterized testing with Pytest
===================================================

.. image:: https://travis-ci.org/akaihola/testdimensions.svg?branch=master
    :target: https://travis-ci.org/akaihola/testdimensions

There are multiple ways to write parameterized tests in Python. Unittest has
some support these days, Nose allows yielding test cases, Pytest has built-in
parameterization support, and the excellent nose_parameterized_ package enhances
these capabilities in most test frameworks.

``testdimensions`` provides a convenient way to write multi-dimensional test
matrices in some simple scenarios. If your function accepts multiple arguments
and you want to test a cross product set of parameter combinations,
``testdimensions`` is for you.

Specify your tests as a table whose:

- Y axis labels are values for the third-last parameter
- X axis labels are values for the second-last paremeter
- cell values are the expected values (last parameter)
- columns are separated by two spaces
  (make sure this is true on all rows)

.. code:: python

   # test_math.py
   @pytest_mark_dimensions('base,exponent,expected', '''
       # y: base
       # x: exponent
       # cell: expected

             2    3    9
        0    0    0    0
        1    1    1    1
        2    4    8  512
   ''')
   def test_pow(base, exponent, expected):
       assert math.pow(base, exponent) == expected


   @pytest_mark_dimensions('input,function,expected', '''
                   round  math.floor  math.ceil
       -1.5         -2.0        -2.0       -1.0
        1.0          1.0         1.0        1.0
        1.6          2.0         1.0        2.0
   ''')
   def test_round_floor_ceil(input, function, expected):
       assert function(input) == expected

Output::

    $ pytest -v
    =========================== test session starts ===============================
    platform linux -- Python 3.5.2, pytest-3.0.3, py-1.4.31, pluggy-0.4.0
    collected 18 items

    test_math.py::test_pow[0-2-0] PASSED
    test_math.py::test_pow[0-3-0] PASSED
    test_math.py::test_pow[0-9-0] PASSED
    test_math.py::test_pow[1-2-1] PASSED
    test_math.py::test_pow[1-3-1] PASSED
    test_math.py::test_pow[1-9-1] PASSED
    test_math.py::test_pow[2-2-4] PASSED
    test_math.py::test_pow[2-3-8] PASSED
    test_math.py::test_pow[2-9-512] PASSED
    test_math.py::test_round_floor_ceil[-1.5-function0--2.0] PASSED
    test_math.py::test_round_floor_ceil[-1.5-function1--2.0] PASSED
    test_math.py::test_round_floor_ceil[-1.5-function2--1.0] PASSED
    test_math.py::test_round_floor_ceil[1.0-function3-1.0] PASSED
    test_math.py::test_round_floor_ceil[1.0-function4-1.0] PASSED
    test_math.py::test_round_floor_ceil[1.0-function5-1.0] PASSED
    test_math.py::test_round_floor_ceil[1.6-function6-2.0] PASSED
    test_math.py::test_round_floor_ceil[1.6-function7-1.0] PASSED
    test_math.py::test_round_floor_ceil[1.6-function8-2.0] PASSED

    ============================ 18 passed in 0.03 seconds ========================

Installation
------------

::

    $ pip install testdimensions


Compatibility
-------------

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - Py2.6
     - Py2.7
     - Py3.3
     - Py3.4
     - Py3.5
     - PyPy
   * - nose
     - no
     - yes
     - no
     - no
     - yes
     - no
   * - nose2
     - no
     - no
     - no
     - no
     - no
     - no
   * - py.test
     - not tested
     - yes
     - not tested
     - not tested
     - yes
     - not tested
   * - unittest
     - no
     - no
     - no
     - no
     - no
     - no
   * - unittest2
     - no
     - no
     - no
     - no
     - no
     - no

Dependencies
------------

- nose_parameterized_ for Nose support


Exhaustive Usage Examples
--------------------------

The ``@pytest_mark_dimensions`` decorator is an extension of
``@pytest.mark.parametrize`` and requires a comma-separated list of test
parameters as its first argument. The second argument is a multi-line string
which defines the actual tests. You can also inject values into the test
globals namespace using keyword arguments.

To create higher than two-dimensional tests, just define multiple tables
interspersed with values for the additional parameters.

.. code:: python

   @pytest_mark_dimensions('a,b,expected', '''
               -10   0   9  million
       -9      -19  -9   0   999991
        0      -10   0   9  million
       10        0  10  19  1000010
       ''',
       million=1000000)
   def test_add(a, b, expected):
       assert a + b == expected


   @pytest_mark_dimensions('operation,a,b,expected', '''
       operation = operator.sub

               -10   0    9   million
       -9        1  -9  -18  -1000009
        0       10   0   -9  -million
       10       20  10    1   -999990

       operation = operator.add

               -10   0   9  million
       -9      -19  -9   0   999991
        0      -10   0   9  million
       10        0  10  19  1000010

       operation = operator.mul

               -10   0    9   million
       -9       90   0  -81  -9000000
        0        0   0    0         0
       10     -100   0   90  10000000

       ''',
       million=1000000)
   def test_arithmetic_operations(operation, a, b, expected):
       assert operation(a, b) == expected

For Nose support, you need to install nose_parameterized_ and use the
``@nosedimensions`` decorator:

.. code:: python

   @nosedimensions('a,b,expected', '''
               -10   0   9  million
       -9      -19  -9   0   999991
        0      -10   0   9  million
       10        0  10  19  1000010
       ''',
       million=1000000)
   def test_add(a, b, expected):
       assert a + b == expected


   @nosedimensions('operation,a,b,expected', '''
       operation = operator.sub

               -10   0    9   million
       -9        1  -9  -18  -1000009
        0       10   0   -9  -million
       10       20  10    1   -999990

       operation = operator.add

               -10   0   9  million
       -9      -19  -9   0   999991
        0      -10   0   9  million
       10        0  10  19  1000010

       operation = operator.mul

               -10   0    9   million
       -9       90   0  -81  -9000000
        0        0   0    0         0
       10     -100   0   90  10000000

       ''',
       million=1000000)
   def test_arithmetic_operations(operation, a, b, expected):
       assert operation(a, b) == expected

Note that you still need to enumerate the test parameters just like with Pytest.

.. _nose_parameterized: https://pypi.org/project/nose-parameterized/
