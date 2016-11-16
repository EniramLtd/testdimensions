from mock import patch
from testdimensions import nosedimensions


def test_nosedimensions_indented():
    with patch('nose_parameterized.parameterized.__init__') as parametrize:
        nosedimensions(
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

    parametrize.assert_called_once_with([(5, 122, 'count', 1, 1),
                                         (5, 122, 'count', 2, 1),
                                         (5, 122, 'count', 3, 1),
                                         (5, 122, 'sum', 1, 1),
                                         (5, 122, 'sum', 2, 1),
                                         (5, 122, 'sum', 3, 1),
                                         (5, 122, 'mean', 1, 1),
                                         (5, 122, 'mean', 2, 1),
                                         (5, 122, 'mean', 3, 1)])