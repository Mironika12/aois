import numpy as np
from binary_math.int_fixed import decimal_to_binary_unsigned
from binary_math.constants import *


def float_to_ieee754(x):
    result = np.zeros(BITS32, dtype=int)

    if x < 0:
        result[0] = 1
        x = -x

    if x == 0:
        return result

    integer = int(x)
    fraction = x - integer

    int_bits = []

    if integer == 0:
        int_bits = [0]
    else:
        while integer > 0:
            int_bits.append(integer % 2)
            integer //= 2
        int_bits = int_bits[::-1]

    frac_bits = []

    for _ in range(BITS31 - 1):
        fraction *= 2
        bit = int(fraction)
        frac_bits.append(bit)
        fraction -= bit

    if int_bits[0] == 1:
        exponent = len(int_bits) - 1
        mantissa = int_bits[1:] + frac_bits
    else:
        shift = 0
        while shift < len(frac_bits) and frac_bits[shift] == 0:
            shift += 1

        if shift == len(frac_bits):
            return result

        exponent = -(shift + 1)
        mantissa = frac_bits[shift + 1:]

    exponent = exponent + EXP_BIAS

    exp_bits = decimal_to_binary_unsigned(exponent, EXP_BITS)
    result[EXP_START:EXP_END] = exp_bits

    for i in range(MANTISSA_BITS):
        if i < len(mantissa):
            result[MANTISSA_START + i] = mantissa[i]

    return result


def ieee754_to_decimal(arr):
    sign = arr[0]

    exponent = 0
    for bit in arr[EXP_START:EXP_END]:
        exponent = (exponent << 1) | bit

    exponent -= EXP_BIAS

    mantissa = 1
    power = 0.5

    for bit in arr[MANTISSA_START:]:
        mantissa += bit * power
        power /= 2

    value = mantissa * (2.0 ** exponent)

    if sign == 1:
        value = -value

    return value


def ieee_add(a_arr, b_arr):
    result = np.zeros(BITS32, dtype=int)

    sign_a = a_arr[0]
    sign_b = b_arr[0]

    exp_a = 0
    exp_b = 0

    for bit in a_arr[EXP_START:EXP_END]:
        exp_a = (exp_a << 1) | bit

    for bit in b_arr[EXP_START:EXP_END]:
        exp_b = (exp_b << 1) | bit

    mant_a = np.zeros(MANTISSA_FULL, dtype=int)
    mant_b = np.zeros(MANTISSA_FULL, dtype=int)

    mant_a[0] = 1
    mant_b[0] = 1

    mant_a[1:] = a_arr[MANTISSA_START:]
    mant_b[1:] = b_arr[MANTISSA_START:]

    while exp_a > exp_b:
        mant_b[1:] = mant_b[:-1]
        mant_b[0] = 0
        exp_b += 1

    while exp_b > exp_a:
        mant_a[1:] = mant_a[:-1]
        mant_a[0] = 0
        exp_a += 1

    exponent = exp_a

    mant_res = np.zeros(MANTISSA_EXTENDED, dtype=int)

    if sign_a == sign_b:
        carry = 0
        for i in range(MANTISSA_BITS, -1, -1):
            s = mant_a[i] + mant_b[i] + carry
            mant_res[i + 1] = s % 2
            carry = s // 2

        mant_res[0] = carry
        sign_res = sign_a

    else:
        if tuple(mant_a) >= tuple(mant_b):
            big = mant_a
            small = mant_b
            sign_res = sign_a
        else:
            big = mant_b
            small = mant_a
            sign_res = sign_b

        borrow = 0
        for i in range(MANTISSA_BITS, -1, -1):
            diff = big[i] - small[i] - borrow
            if diff < 0:
                mant_res[i + 1] = diff + 2
                borrow = 1
            else:
                mant_res[i + 1] = diff
                borrow = 0

    if mant_res[0] == 1:
        mant_res[1:] = mant_res[:-1]
        exponent += 1
    else:
        while mant_res[1] == 0 and exponent > 0:
            mant_res[:-1] = mant_res[1:]
            exponent -= 1

    result[0] = sign_res

    exp_bits = decimal_to_binary_unsigned(exponent, EXP_BITS)
    result[EXP_START:EXP_END] = exp_bits

    result[MANTISSA_START:] = mant_res[2:MANTISSA_EXTENDED]

    return result


def ieee_sub(a_arr, b_arr):
    b_neg = b_arr.copy()
    b_neg[0] = 1 - b_neg[0]
    return ieee_add(a_arr, b_neg)


def ieee_mul(a_arr, b_arr):
    result = np.zeros(BITS32, dtype=int)
    sign = int(a_arr[0]) ^ int(b_arr[0])

    exp_a = 0
    exp_b = 0

    for bit in a_arr[EXP_START:EXP_END]:
        exp_a = (exp_a << 1) | int(bit)

    for bit in b_arr[EXP_START:EXP_END]:
        exp_b = (exp_b << 1) | int(bit)

    is_zero_a = (exp_a == 0) and (not a_arr[MANTISSA_START:].any())
    is_zero_b = (exp_b == 0) and (not b_arr[MANTISSA_START:].any())

    if is_zero_a or is_zero_b:
        result[0] = sign
        return result

    mant_a = 0
    mant_b = 0

    for bit in a_arr[MANTISSA_START:]:
        mant_a = (mant_a << 1) | int(bit)

    for bit in b_arr[MANTISSA_START:]:
        mant_b = (mant_b << 1) | int(bit)

    if exp_a != 0:
        mant_a |= (1 << MANTISSA_BITS)
    else:
        exp_a = 1

    if exp_b != 0:
        mant_b |= (1 << MANTISSA_BITS)
    else:
        exp_b = 1

    exponent = exp_a + exp_b - EXP_BIAS
    product = mant_a * mant_b
    mant_int = product >> MANTISSA_BITS

    if mant_int == 0:
        result[0] = sign
        return result

    if mant_int >= (1 << MANTISSA_FULL):
        mant_int >>= 1
        exponent += 1

    if exponent <= 0:
        result[0] = sign
        return result

    if exponent >= MAX_EXP:
        result[0] = sign
        result[EXP_START:EXP_END] = np.ones(EXP_BITS, dtype=int)
        result[MANTISSA_START:] = np.zeros(MANTISSA_BITS, dtype=int)
        return result

    mantissa_field = mant_int & ((1 << MANTISSA_BITS) - 1)

    result[0] = sign
    result[EXP_START:EXP_END] = decimal_to_binary_unsigned(exponent, EXP_BITS)

    for i in range(MANTISSA_BITS):
        result[MANTISSA_START + i] = (mantissa_field >> (MANTISSA_BITS - 1 - i)) & 1

    return result


def ieee_div(a_arr, b_arr):
    def exp_to_bits(e):
        arr = np.zeros(EXP_BITS, dtype=int)
        for i in range(EXP_BITS):
            arr[EXP_BITS - 1 - i] = (e >> i) & 1
        return arr

    result = np.zeros(BITS32, dtype=int)

    sign = int(a_arr[0]) ^ int(b_arr[0])

    exp_a = 0
    exp_b = 0

    for bit in a_arr[EXP_START:EXP_END]:
        exp_a = (exp_a << 1) | int(bit)

    for bit in b_arr[EXP_START:EXP_END]:
        exp_b = (exp_b << 1) | int(bit)

    is_zero_a = (exp_a == 0) and (not a_arr[MANTISSA_START:].any())
    is_zero_b = (exp_b == 0) and (not b_arr[MANTISSA_START:].any())

    if is_zero_b:
        raise ZeroDivisionError("division by zero")

    if is_zero_a:
        result[0] = sign
        return result

    mant_a = 0
    mant_b = 0

    for bit in a_arr[MANTISSA_START:]:
        mant_a = (mant_a << 1) | int(bit)

    for bit in b_arr[MANTISSA_START:]:
        mant_b = (mant_b << 1) | int(bit)

    if exp_a != 0:
        mant_a |= (1 << MANTISSA_BITS)
    else:
        exp_a = 1

    if exp_b != 0:
        mant_b |= (1 << MANTISSA_BITS)
    else:
        exp_b = 1

    exponent = exp_a - exp_b + EXP_BIAS
    mant_int = (mant_a << MANTISSA_BITS) // mant_b

    if mant_int == 0:
        result[0] = sign
        return result

    if mant_int >= (1 << MANTISSA_FULL):
        mant_int >>= 1
        exponent += 1

    while mant_int < (1 << MANTISSA_BITS):
        mant_int <<= 1
        exponent -= 1
        if exponent <= 0:
            result[0] = sign
            return result

    if exponent >= MAX_EXP:
        result[0] = sign
        result[EXP_START:EXP_END] = np.ones(EXP_BITS, dtype=int)
        result[MANTISSA_START:] = np.zeros(MANTISSA_BITS, dtype=int)
        return result

    mantissa_field = mant_int & ((1 << MANTISSA_BITS) - 1)

    result[0] = sign
    result[EXP_START:EXP_END] = exp_to_bits(exponent)

    for i in range(MANTISSA_BITS):
        result[MANTISSA_START + i] = (mantissa_field >> (MANTISSA_BITS - 1 - i)) & 1

    return result