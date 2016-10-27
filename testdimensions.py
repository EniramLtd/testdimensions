import inspect
from itertools import dropwhile, takewhile

import re
from textwrap import dedent


def all_same(lines, position, character):
    return all(line[position] == character for line in lines)


def is_blank(s):
    return not s.strip()


def not_blank(s):
    return s.strip()


def split_by_blank_lines(content):
    lines = iter(content.split('\n'))
    while True:
        without_leading_blanks = dropwhile(is_blank, lines)
        non_blank_lines = list(takewhile(not_blank, without_leading_blanks))
        if not non_blank_lines:
            break
        yield non_blank_lines


def is_table(lines, sep='  '):
    if lines:
        return re.match(r' +{}'.format(sep), lines[0])
    else:
        return False


def pick_columns(line, starts, ends):
    return [line[start:end].strip() for start, end in zip(starts, ends)]


def parse_table(lines, sep='  '):
    if not lines:
        return []
    max_length = max((len(line) for line in lines))
    padded_lines = ['{line:<{length}s}'.format(line=line, length=max_length)
                    for line in lines]
    header = padded_lines[0]
    data_lines = padded_lines[1:]
    seps = ''.join(character if all_same(data_lines, position, character)
                   else 'x'
                   for position, character in enumerate(header.rstrip()))
    sep_matches = re.finditer(r' *{} *'.format(sep), seps.rstrip())
    spans = [m.span() for m in sep_matches]
    starts = [0] + [span[1] for span in spans]
    ends = [span[0] for span in spans] + [None]
    return [pick_columns(line, starts, ends) for line in padded_lines]


def iterate_table_cells(table):
    if not table:
        return
    column_titles = table[0][1:]
    rows = table[1:]
    for row in rows:
        row_title = row[0]
        for column_num, cell in enumerate(row[1:]):
            column_title = column_titles[column_num]
            yield row_title, column_title, cell


try:
    import pytest


    def pytest_mark_dimensions(argnames, tables, sep='  ', **namespace):
        # Get globals and locals from the calling scope
        if not isinstance(argnames, (tuple, list)):
            argnames = [x.strip() for x in argnames.split(",") if x.strip()]
        eval_namespace = inspect.currentframe().f_back.f_globals.copy()
        eval_namespace.update(inspect.currentframe().f_back.f_locals)
        eval_namespace.update(namespace)
        argvalues = []
        for lines in split_by_blank_lines(dedent(tables)):
            if is_table(lines, sep):
                uncommented_lines = [line for line in lines
                                     if not line.lstrip().startswith('#')]
                parsed_table = parse_table(uncommented_lines, sep)
                for row, col, cell in iterate_table_cells(parsed_table):
                    argvalues.append(tuple(eval_namespace[argname]
                                           for argname in argnames[:-3]) +
                                     (eval(row, eval_namespace),
                                      eval(col, eval_namespace),
                                      eval(cell, eval_namespace)))
            else:
                exec('\n'.join(lines), eval_namespace)
        return pytest.mark.parametrize(argnames, argvalues)
except ImportError:
    pass
