import pytest

from logic.minimization_carno import (
    gray_code,
    build_kmap,
    is_valid_group,
    get_all_groups,
    remove_subgroups,
    group_to_term,
    minimize_kmap
)


# ---------------- helpers ----------------

@pytest.fixture
def simple_table_2vars():
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 0},
    ]


@pytest.fixture
def simple_table_1var():
    return [
        {"a": 0, "f": 0},
        {"a": 1, "f": 1},
    ]


# ---------------- gray_code ----------------

def test_gray_code_0():
    assert gray_code(0) == [[]]


def test_gray_code_1():
    assert gray_code(1) == [[0], [1]]


def test_gray_code_2():
    result = gray_code(2)
    assert result == [
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0],
    ]


# ---------------- build_kmap ----------------

def test_build_kmap_2vars(simple_table_2vars):
    kmap, vars, row_codes, col_codes = build_kmap(simple_table_2vars)

    assert len(kmap) == 2
    assert len(kmap[0]) == 2
    assert vars == ["a", "b"]


def test_build_kmap_1var(simple_table_1var):
    kmap, vars, row_codes, col_codes = build_kmap(simple_table_1var)

    assert len(kmap) == 1
    assert len(kmap[0]) == 2


# ---------------- is_valid_group ----------------

def test_is_valid_group_true():
    kmap = [[1, 1], [1, 1]]
    cells = [(0, 0), (0, 1)]
    assert is_valid_group(kmap, cells, 1) is True


def test_is_valid_group_false():
    kmap = [[1, 0], [1, 1]]
    cells = [(0, 0), (0, 1)]
    assert is_valid_group(kmap, cells, 1) is False


# ---------------- get_all_groups ----------------

def test_get_all_groups_basic(simple_table_2vars):
    kmap, *_ = build_kmap(simple_table_2vars)

    groups = get_all_groups(kmap, 1)
    assert isinstance(groups, list)
    assert all(isinstance(g, list) for g in groups)


def test_get_all_groups_zero_target(simple_table_2vars):
    kmap, *_ = build_kmap(simple_table_2vars)

    groups = get_all_groups(kmap, 0)
    assert groups  # должны быть группы


# ---------------- remove_subgroups ----------------

def test_remove_subgroups():
    groups = [
        [(0, 0)],
        [(0, 0), (0, 1)],
    ]

    result = remove_subgroups(groups)

    assert [(0, 0)] not in result
    assert [(0, 0), (0, 1)] in result


# ---------------- group_to_term ----------------

def test_group_to_term_sdnf(simple_table_2vars):
    kmap, vars, row_codes, col_codes = build_kmap(simple_table_2vars)

    group = [(0, 1)]  # конкретная клетка
    term = group_to_term(group, vars, row_codes, col_codes, True)

    assert isinstance(term, dict)
    assert set(term.keys()) == set(vars)


def test_group_to_term_sknf(simple_table_2vars):
    kmap, vars, row_codes, col_codes = build_kmap(simple_table_2vars)

    group = [(0, 0)]
    term = group_to_term(group, vars, row_codes, col_codes, False)

    assert isinstance(term, dict)


def test_group_to_term_with_none():
    vars = ["a", "b"]
    row_codes = [[0], [1]]
    col_codes = [[0], [1]]

    group = [(0, 0), (0, 1)]  # b меняется → None
    term = group_to_term(group, vars, row_codes, col_codes, True)

    assert term["b"] is None


# ---------------- minimize_kmap ----------------

def test_minimize_kmap_sdnf(simple_table_2vars):
    terms = minimize_kmap(simple_table_2vars, True)

    assert isinstance(terms, list)
    assert all(isinstance(t, dict) for t in terms)


def test_minimize_kmap_sknf(simple_table_2vars):
    terms = minimize_kmap(simple_table_2vars, False)

    assert isinstance(terms, list)


def test_minimize_kmap_constant_1():
    table = [
        {"a": 0, "f": 1},
        {"a": 1, "f": 1},
    ]

    terms = minimize_kmap(table, True)

    # должна быть константа → один терм без переменных
    assert terms
    assert all(v is None for v in terms[0].values())


def test_minimize_kmap_constant_0():
    table = [
        {"a": 0, "f": 0},
        {"a": 1, "f": 0},
    ]

    terms = minimize_kmap(table, False)

    assert terms
    assert all(v is None for v in terms[0].values())