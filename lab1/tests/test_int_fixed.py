import numpy as np
import pytest

from binary_math.int_fixed import (
    decimal_to_binary_unsigned,
    direct_code,
    ones_complement,
    twos_complement,
    add_twos_complement,
    twos_to_decimal,
    subtract_twos_complement,
    multiply_direct,
    compare_binary,
    subtract_binary,
    divide_direct,
    fixed_to_decimal,
)

def test_decimal_to_binary_unsigned_basic():
    res = decimal_to_binary_unsigned(5, bits=4)
    assert np.array_equal(res, np.array([0,1,0,1]))

def test_decimal_to_binary_unsigned_zero():
    res = decimal_to_binary_unsigned(0, bits=4)
    assert np.array_equal(res, np.zeros(4))

def test_direct_code_positive():
    res = direct_code(5)
    assert res[0] == 0
    assert twos_to_decimal(res) == 5

def test_direct_code_negative():
    res = direct_code(-5)
    assert res[0] == 1

def test_ones_complement_positive():
    res = ones_complement(3)
    dc = direct_code(3)
    assert np.array_equal(res, dc)

def test_ones_complement_negative():
    res = ones_complement(-3)
    dc = direct_code(-3)
    assert not np.array_equal(res, dc)

def test_twos_complement_positive():
    res = twos_complement(7)
    assert twos_to_decimal(res) == 7

def test_twos_complement_negative():
    res = twos_complement(-7)
    assert twos_to_decimal(res) == -7

def test_add_twos_complement():
    a = twos_complement(4)
    b = twos_complement(3)
    result = add_twos_complement(a, b)
    assert twos_to_decimal(result) == 7

def test_subtract_twos_complement():
    a = twos_complement(10)
    b = twos_complement(-3)
    result = subtract_twos_complement(a, b)
    assert twos_to_decimal(result) == 7

def test_compare_binary_true():
    a = np.array([1,0,1])
    b = np.array([1,0,0])
    assert compare_binary(a,b)

def test_compare_binary_false():
    a = np.array([1,0,0])
    b = np.array([1,1,0])
    assert not compare_binary(a,b)

def test_subtract_binary():
    a = np.array([1,0,1])
    b = np.array([0,1,1])
    res = subtract_binary(a,b)
    assert np.array_equal(res, np.array([0,1,0]))

def test_multiply_direct():
    a = direct_code(3)
    b = direct_code(2)
    result = multiply_direct(a,b)
    sign = result[0]
    magnitude = result[1:]
    value = 0
    for bit in magnitude:
        value = value * 2 + bit
    if sign:
        value = -value
    assert value == 6

def test_divide_direct_basic():
    a = direct_code(8)
    b = direct_code(2)
    res = divide_direct(a,b)
    val = fixed_to_decimal(res)
    assert round(val) == 4

def test_divide_by_zero():
    a = direct_code(5)
    b = direct_code(0)
    with pytest.raises(ValueError):
        divide_direct(a,b)

def test_fixed_to_decimal_positive():
    arr = direct_code(4)
    val = fixed_to_decimal(arr)
    assert isinstance(val, float)

def test_fixed_to_decimal_negative():
    arr = direct_code(-4)
    val = fixed_to_decimal(arr)
    assert val < 0