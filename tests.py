import pytest

from testdimensions import (all_same,
                            is_blank,
                            not_blank,
                            split_by_blank_lines,
                            is_table,
                            pick_columns,
                            parse_table,
                            iterate_table_cells,
                            pytest_mark_dimensions,
                            nosedimensions)


@pytest.mark.parametrize(
    'lines,position,character,expect',
    [([], 0, 'x', True),
     (['a|b', 'b|c'], 0, '|', False),
     (['a|b', 'b|c'], 1, '|', True),
     (['a|b', 'b|c'], 10, '|', IndexError),
     (['a|b', 'b|c|d'], 3, '|', IndexError)])
def test_all_same(lines, position, character, expect):
    if isinstance(expect, type) and issubclass(expect, Exception):
        with pytest.raises(expect):
            all_same(lines, position, character)
    else:
        result = all_same(lines, position, character)
        assert result == expect


@pytest.mark.parametrize(
    's,expect',
    [('', True),
     (' ', True),
     ('\t', True),
     ('  x  ', False),
     ('foobar', False)])
def test_is_blank(s, expect):
    result = is_blank(s)
    assert result == expect


@pytest.mark.parametrize(
    's,expect',
    [('', False),
     (' ', False),
     ('\t', False),
     ('  x  ', True),
     ('foobar', True)])
def test_not_blank(s, expect):
    result = bool(not_blank(s))
    assert result == expect


@pytest.mark.parametrize(
    'content,expect',
    [('', []),
     ('foobar', [['foobar']]),
     ('\nfoobar', [['foobar']]),
     ('\n\nfoobar', [['foobar']]),
     ('\nfoo\nbar\n', [['foo', 'bar']]),
     ('\nfoo\nbar\n\nbaz', [['foo', 'bar'], ['baz']]),
     ('\nfoo\nbar\n    \t  \n\nbaz', [['foo', 'bar'], ['baz']]),
     ])
def test_split_by_blank_lines(content, expect):
    result = list(split_by_blank_lines(content))
    assert result == expect


@pytest.mark.parametrize(
    'lines,sep,expect',
    [([''], r'\|', False),
     (['col1 | col2',
       'a | b  '], r'\|', False),
     (['     | col1 | col2',
       'row1 | a '], r'\|', True),
     (['| col1 | col2',
       '| a '], r'\|', False)])
def test_is_table(lines, sep, expect):
    result = bool(is_table(lines, sep))
    assert result == expect


@pytest.mark.parametrize(
    'line,starts,ends,expect',
    [('', [], [], []),
     ('abcde', [], [], []),
     ('', [5], [10], ['']),
     ('abcde', [0, 2, 4], [1, 4, 8], ['a', 'cd', 'e']),
     (' a | b | c ', [0, 4, 8], [3, 7, 11], ['a', 'b', 'c'])])
def test_pick_columns(line, starts, ends, expect):
    result = pick_columns(line, starts, ends)
    assert result == expect


@pytest.mark.parametrize(
    'lines,sep,expect',
    [([], 'x', []),
     ([' | '], r'\|', [['', '']]),
     ([' | col1 | col2'], r'\|', [['', 'col1', 'col2']]),
     (['     | col1   | col2',
       'row1 | cell11 | cell12  ',
       'row2 | cell21 | cell22'],
      r'\|',
      [['', 'col1', 'col2'],
       ['row1', 'cell11', 'cell12'],
       ['row2', 'cell21', 'cell22']]),
     (['      col1    col2',
       'row1  cell11  cell12  ',
       'row2  cell21  cell22'],
      r'  ',
      [['', 'col1', 'col2'],
       ['row1', 'cell11', 'cell12'],
       ['row2', 'cell21', 'cell22']])])
def test_parse_table(lines, sep, expect):
    result = parse_table(lines, sep)
    assert result == expect


@pytest.mark.parametrize(
    'table,expect',
    [([], []),
     ([['', 'col1', 'col2']], []),
     ([['', 'col1', 'col2'],
       ['row1', 'cell11', 'cell12']],
      [('row1', 'col1', 'cell11'),
       ('row1', 'col2', 'cell12')]),
     ([['', 'col1', 'col2'],
       ['row1', 'cell11', 'cell12'],
       ['row2', 'cell21', 'cell22']],
      [('row1', 'col1', 'cell11'),
       ('row1', 'col2', 'cell12'),
       ('row2', 'col1', 'cell21'),
       ('row2', 'col2', 'cell22')
       ])])
def test_iterate_table_cells(table, expect):
    result = list(iterate_table_cells(table))
    assert result == expect


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


def test_nosedimensions_indented(mocker):
    parametrize = mocker.patch('nose_parameterized.parameterized.__init__')
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