from testdimensions import pytest_mark_dimensions


def test_pytest_mark_dimensions(mocker):
    parametrize = mocker.patch('pytest.mark.parametrize')
    pytest_mark_dimensions(
        'y,x,expect',
        ('Z = 0\n'
         '\n'
         '   |      1 |  2\n'
         '10 | Z + 11 | 12\n'
         '20 |     21 | 22\n'
         '\n'
         'Z = 100\n'
         '\n'
         '   |      1 | 2\n'
         '10 | Z + 11 | 112\n'
         '20 |    121 | R\n'),
        r'\|',
        R=122)

    parametrize.assert_called_once_with(['y', 'x', 'expect'],
                                        [(10, 1, 11),
                                         (10, 2, 12),
                                         (20, 1, 21),
                                         (20, 2, 22),
                                         (10, 1, 111),
                                         (10, 2, 112),
                                         (20, 1, 121),
                                         (20, 2, 122)])


def test_pytest_mark_dimensions_whitespace_separator(mocker):
    parametrize = mocker.patch('pytest.mark.parametrize')
    pytest_mark_dimensions(
        'y,x,expect',
        ('Z = 0\n'
         '\n'
         '         1   2  \n'
         '10  Z + 11  12\n'
         '20      21  22\n'
         '\n'
         'Z = 100\n'
         '\n'
         '         1  2\n'
         '10  Z + 11  112\n'
         '20     121  R\n'),
        '  ',
        R=122)

    parametrize.assert_called_once_with(['y', 'x', 'expect'],
                                        [(10, 1, 11),
                                         (10, 2, 12),
                                         (20, 1, 21),
                                         (20, 2, 22),
                                         (10, 1, 111),
                                         (10, 2, 112),
                                         (20, 1, 121),
                                         (20, 2, 122)])


def test_pytest_mark_dimensions_indented(mocker):
    parametrize = mocker.patch('pytest.mark.parametrize')
    pytest_mark_dimensions(
        'z,R,y,x,expect',
        '''
        z = 5

                  1  2  3
        'count'   1  1  1
        'sum'     1  1  1
        'mean'    1  1  1
        ''',
        '  ',
        R=122)

    parametrize.assert_called_once_with(['z', 'R', 'y', 'x', 'expect'],
                                        [(5, 122, 'count', 1, 1),
                                         (5, 122, 'count', 2, 1),
                                         (5, 122, 'count', 3, 1),
                                         (5, 122, 'sum', 1, 1),
                                         (5, 122, 'sum', 2, 1),
                                         (5, 122, 'sum', 3, 1),
                                         (5, 122, 'mean', 1, 1),
                                         (5, 122, 'mean', 2, 1),
                                         (5, 122, 'mean', 3, 1)])


@pytest_mark_dimensions(
    'y,x,expect',
    '''
              1  2  3  4  5
    'count'   1  1  1  1  1
    'sum'     1  1  1  1  1
    'mean'    1  1  1  1  1
    'median'  1  1  1  1  1
    'min'     1  1  1  1  1
    'max'     1  1  1  1  1
    ''',
    sep='  ')
def test_something(y, x, expect):
    assert True