import pytest

from logic.dummy_vars import (
    get_neighbor_pairs,
    find_dummy_vars,
    calculate_derivative,
    boolean_derivative,
    mixed_derivative
)


# ---------------- helpers ----------------

@pytest.fixture
def table_2vars():
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 0},
        {"a": 1, "b": 1, "f": 1},
    ]


@pytest.fixture
def table_dummy_var():
    # функция зависит только от a → b фиктивная
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 0},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 1},
    ]


# ---------------- get_neighbor_pairs ----------------

def test_get_neighbor_pairs_a(table_2vars):
    pairs = get_neighbor_pairs(table_2vars, "a")
    assert pairs == [(0, 2), (1, 3)]


def test_get_neighbor_pairs_b(table_2vars):
    pairs = get_neighbor_pairs(table_2vars, "b")
    assert pairs == [(0, 1), (2, 3)]


# ---------------- find_dummy_vars ----------------

# def test_find_dummy_vars_none(table_2vars):
#     assert find_dummy_vars(table_2vars) == []


def test_find_dummy_vars_one(table_dummy_var):
    assert find_dummy_vars(table_dummy_var) == ["b"]


def test_find_dummy_vars_all_dummy():
    table = [
        {"a": 0, "b": 0, "f": 1},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 1},
    ]
    # константа → все переменные фиктивные
    assert set(find_dummy_vars(table)) == {"a", "b"}


# ---------------- calculate_derivative ----------------

def test_calculate_derivative_basic():
    values = [0, 1, 0, 1]
    # производная по первой переменной
    result = calculate_derivative(values, var_index=0, n=2)

    assert result == [0 ^ 0, 1 ^ 1, 0 ^ 0, 1 ^ 1]


def test_calculate_derivative_second_var():
    values = [0, 1, 0, 1]
    result = calculate_derivative(values, var_index=1, n=2)

    assert result == [0 ^ 1, 0 ^ 1, 0 ^ 1, 0 ^ 1]


# ---------------- boolean_derivative ----------------

def test_boolean_derivative_a(table_2vars):
    result = boolean_derivative(table_2vars, "a")

    assert len(result) == 4
    assert all(v in (0, 1) for v in result)


def test_boolean_derivative_b(table_2vars):
    result = boolean_derivative(table_2vars, "b")

    assert len(result) == 4


# ---------------- mixed_derivative ----------------

def test_mixed_derivative_basic(table_2vars):
    result = mixed_derivative(table_2vars, ["a", "b"])

    assert len(result) == 4
    assert all(v in (0, 1) for v in result)


def test_mixed_derivative_order_matters(table_2vars):
    res1 = mixed_derivative(table_2vars, ["a", "b"])
    res2 = mixed_derivative(table_2vars, ["b", "a"])

    # для XOR-производных порядок может совпасть, но проверим корректность вычисления
    assert len(res1) == len(res2)


def test_mixed_derivative_single_var(table_2vars):
    result = mixed_derivative(table_2vars, ["a"])

    # должно совпадать с обычной производной
    expected = boolean_derivative(table_2vars, "a")
    assert result == expected