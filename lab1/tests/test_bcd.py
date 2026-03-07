import numpy as np
import pytest

from binary_math.bcd import decimal_to_bcd, bcd_to_decimal, add_bcd


def test_decimal_to_bcd_basic():
    res = decimal_to_bcd(25)
    expected = np.array([0,0,1,0, 0,1,0,1])
    assert np.array_equal(res, expected)


def test_decimal_to_bcd_zero():
    res = decimal_to_bcd(0)
    assert np.array_equal(res, np.array([0,0,0,0]))


def test_decimal_to_bcd_min_digits():
    res = decimal_to_bcd(7, min_digits=3)
    expected = np.array([
        0,0,0,0,
        0,0,0,0,
        0,1,1,1
    ])
    assert np.array_equal(res, expected)


def test_decimal_to_bcd_type_error():
    with pytest.raises(TypeError):
        decimal_to_bcd(3.5)


def test_decimal_to_bcd_negative():
    with pytest.raises(ValueError):
        decimal_to_bcd(-5)


def test_bcd_to_decimal_basic():
    arr = np.array([0,0,1,0, 0,1,0,1])
    assert bcd_to_decimal(arr) == 25


def test_bcd_to_decimal_list_input():
    arr = [0,0,0,1, 0,0,1,0]
    assert bcd_to_decimal(arr) == 12


def test_bcd_to_decimal_invalid_length():
    with pytest.raises(ValueError):
        bcd_to_decimal([1,0,1])


def test_bcd_to_decimal_invalid_digit():
    arr = [1,0,1,0]  # 10 — невалидная BCD цифра
    with pytest.raises(ValueError):
        bcd_to_decimal(arr)


def test_add_bcd_simple():
    a = decimal_to_bcd(4)
    b = decimal_to_bcd(5)

    res = add_bcd(a,b)

    assert bcd_to_decimal(res) == 9


def test_add_bcd_with_carry():
    a = decimal_to_bcd(8)
    b = decimal_to_bcd(7)

    res = add_bcd(a,b)

    assert bcd_to_decimal(res) == 15


def test_add_bcd_different_lengths():
    a = decimal_to_bcd(5)
    b = decimal_to_bcd(17)

    res = add_bcd(a,b)

    assert bcd_to_decimal(res) == 22


def test_add_bcd_new_digit_carry():
    a = decimal_to_bcd(9)
    b = decimal_to_bcd(9)

    res = add_bcd(a,b)

    assert bcd_to_decimal(res) == 18