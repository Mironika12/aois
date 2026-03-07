import numpy as np
import pytest

from binary_math.float_ieee import (
    float_to_ieee754,
    ieee754_to_decimal,
    ieee_add,
    ieee_sub,
    ieee_mul,
    ieee_div
)


def test_float_to_ieee754_positive():
    arr = float_to_ieee754(2.5)
    assert arr.shape[0] == 32


def test_float_to_ieee754_negative():
    arr = float_to_ieee754(-2.5)
    assert arr[0] == 1


def test_ieee754_to_decimal():
    arr = float_to_ieee754(3.5)
    val = ieee754_to_decimal(arr)
    assert abs(val - 3.5) < 0.01


def test_ieee_add():
    a = float_to_ieee754(2.5)
    b = float_to_ieee754(1.5)

    res = ieee_add(a,b)
    val = ieee754_to_decimal(res)

    assert abs(val - 4.0) < 0.1


def test_ieee_sub():
    a = float_to_ieee754(5.5)
    b = float_to_ieee754(2.0)

    res = ieee_sub(a,b)
    val = ieee754_to_decimal(res)

    assert abs(val - 3.5) < 0.1


def test_ieee_mul():
    a = float_to_ieee754(2.5)
    b = float_to_ieee754(2.0)

    res = ieee_mul(a,b)
    val = ieee754_to_decimal(res)

    assert abs(val - 5.0) < 0.1


def test_ieee_mul_zero():
    a = float_to_ieee754(0.0)
    b = float_to_ieee754(2.0)

    res = ieee_mul(a,b)
    val = ieee754_to_decimal(res)

    assert abs(val) < 0.01


def test_ieee_div():
    a = float_to_ieee754(6.0)
    b = float_to_ieee754(2.0)

    res = ieee_div(a,b)
    val = ieee754_to_decimal(res)

    assert abs(val - 3.0) < 0.1


def test_ieee_div_zero():
    a = float_to_ieee754(5.0)
    b = float_to_ieee754(0.0)

    with pytest.raises(ZeroDivisionError):
        ieee_div(a,b)

def test_float_to_ieee_zero():
    arr = float_to_ieee754(0.0)
    assert np.all(arr == 0)

def test_float_to_ieee_small_number():
    arr = float_to_ieee754(0.125)
    val = ieee754_to_decimal(arr)
    assert abs(val - 0.125) < 0.01

def test_ieee_add_different_signs():
    a = float_to_ieee754(5.0)
    b = float_to_ieee754(-2.0)

    res = ieee_add(a, b)
    val = ieee754_to_decimal(res)

    assert abs(val - 3.0) < 0.1

def test_ieee_mul_zero_operand():
    a = float_to_ieee754(0.0)
    b = float_to_ieee754(5.0)

    res = ieee_mul(a, b)
    assert np.all(res[1:] == 0)

def test_ieee_mul_overflow():
    a = float_to_ieee754(1e30)
    b = float_to_ieee754(1e30)

    res = ieee_mul(a, b)

    assert np.all(res[1:9] == 1)

def test_ieee_div_zero_division():
    a = float_to_ieee754(5.0)
    b = float_to_ieee754(0.0)

    with pytest.raises(ZeroDivisionError):
        ieee_div(a, b)

def test_ieee_div_zero_numerator():
    a = float_to_ieee754(0.0)
    b = float_to_ieee754(5.0)

    res = ieee_div(a, b)

    assert res[0] == 0
    assert np.all(res[1:] == 0)

def test_ieee_div_normal():
    a = float_to_ieee754(9.0)
    b = float_to_ieee754(3.0)

    res = ieee_div(a, b)
    val = ieee754_to_decimal(res)

    assert abs(val - 3.0) < 0.1

