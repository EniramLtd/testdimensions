import pytest
from nose_parameterized import parameterized

from testdimensions import (all_same,
                            is_blank,
                            not_blank,
                            split_by_blank_lines,
                            is_table,
                            pick_columns,
                            parse_table,
                            iterate_table_cells)


@parameterized(
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


@parameterized(
    [('', True),
     (' ', True),
     ('\t', True),
     ('  x  ', False),
     ('foobar', False)])
def test_is_blank(s, expect):
    result = is_blank(s)
    assert result == expect


@parameterized(
    [('', False),
     (' ', False),
     ('\t', False),
     ('  x  ', True),
     ('foobar', True)])
def test_not_blank(s, expect):
    result = bool(not_blank(s))
    assert result == expect


@parameterized(
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


@parameterized(
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


@parameterized(
    [('', [], [], []),
     ('abcde', [], [], []),
     ('', [5], [10], ['']),
     ('abcde', [0, 2, 4], [1, 4, 8], ['a', 'cd', 'e']),
     (' a | b | c ', [0, 4, 8], [3, 7, 11], ['a', 'b', 'c'])])
def test_pick_columns(line, starts, ends, expect):
    result = pick_columns(line, starts, ends)
    assert result == expect


@parameterized(
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


@parameterized(
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
