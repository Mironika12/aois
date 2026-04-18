import pytest

from logic.post_zhegalkin import (
    is_T0,
    is_T1,
    is_self_dual,
    leq,
    is_monotonic,
    zhegalkin_coeffs,
    is_linear,
    zhegalkin_polynomial
)


# ---------------- helpers ----------------

@pytest.fixture
def table_and():
    # a & b
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 0},
        {"a": 1, "b": 0, "f": 0},
        {"a": 1, "b": 1, "f": 1},
    ]


@pytest.fixture
def table_or():
    # a | b
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 1},
    ]


@pytest.fixture
def table_xor():
    # a ^ b
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 0},
    ]


@pytest.fixture
def table_const1():
    return [
        {"a": 0, "f": 1},
        {"a": 1, "f": 1},
    ]


# ---------------- T0 / T1 ----------------

def test_is_T0(table_and):
    assert is_T0(table_and) is True


def test_is_not_T0(table_const1):
    assert is_T0(table_const1) is False


def test_is_T1(table_and):
    assert is_T1(table_and) is True


def test_is_not_T1():
    table = [
        {"a": 0, "f": 0},
        {"a": 1, "f": 0},
    ]
    assert is_T1(table) is False


# ---------------- self-dual ----------------

def test_is_self_dual_false(table_and):
    assert is_self_dual(table_and) is False


def test_is_self_dual_true():
    table = [
        {"a": 0, "f": 0},
        {"a": 1, "f": 1},
    ]
    # для 1 переменной это самодвойственная функция
    assert is_self_dual(table) is True


# ---------------- leq ----------------

def test_leq_true():
    r1 = {"a": 0, "b": 0, "f": 0}
    r2 = {"a": 1, "b": 1, "f": 1}
    assert leq(r1, r2) is True


def test_leq_false():
    r1 = {"a": 1, "b": 0, "f": 0}
    r2 = {"a": 0, "b": 1, "f": 1}
    assert leq(r1, r2) is False


# ---------------- monotonic ----------------

def test_is_monotonic_true(table_and):
    assert is_monotonic(table_and) is True


def test_is_monotonic_false(table_xor):
    assert is_monotonic(table_xor) is False


# ---------------- zhegalkin_coeffs ----------------

def test_zhegalkin_coeffs_basic():
    values = [0, 1, 1, 0]  # XOR
    coeffs = zhegalkin_coeffs(values)

    assert isinstance(coeffs, list)
    assert coeffs[0] == 0


def test_zhegalkin_coeffs_constant():
    values = [1, 1]
    coeffs = zhegalkin_coeffs(values)

    assert coeffs == [1, 0]


# ---------------- is_linear ----------------

def test_is_linear_true(table_xor):
    assert is_linear(table_xor) is True


def test_is_linear_false(table_and):
    assert is_linear(table_and) is False


# ---------------- zhegalkin_polynomial ----------------

def test_zhegalkin_polynomial_xor(table_xor):
    poly = zhegalkin_polynomial(table_xor)

    # ожидаем что-то вроде "a ⊕ b"
    assert "a" in poly
    assert "b" in poly


def test_zhegalkin_polynomial_and(table_and):
    poly = zhegalkin_polynomial(table_and)

    # AND даёт произведение
    assert "a&b" in poly or "a & b" in poly


def test_zhegalkin_polynomial_constant1(table_const1):
    poly = zhegalkin_polynomial(table_const1)
    assert poly == "1"


def test_zhegalkin_polynomial_constant0():
    table = [
        {"a": 0, "f": 0},
        {"a": 1, "f": 0},
    ]
    poly = zhegalkin_polynomial(table)
    assert poly == "0"