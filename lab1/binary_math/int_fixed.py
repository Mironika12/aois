import numpy as np

BITS32 = 32
BITS31 = 31
FRAC_BITS = 20

def decimal_to_binary_unsigned(n, bits=31):
    arr = np.zeros(bits, dtype=int)
    i = bits - 1
    while n > 0 and i >= 0:
        arr[i] = n % 2
        n //= 2
        i -= 1
    return arr

def direct_code(n):
    result = np.zeros(BITS32, dtype=int)
    if n < 0:
        result[0] = 1
        n = abs(n)
    result[1:] = decimal_to_binary_unsigned(n)
    return result

def ones_complement(n):
    dc = direct_code(n)
    if n < 0:
        inverted = dc.copy()
        inverted[1:] = 1 - inverted[1:]
        return inverted
    return dc

def twos_complement(n):
    if n >= 0:
        result = direct_code(n)
        return result
    oc = ones_complement(n)
    result = oc.copy()
    carry = 1
    for i in range(BITS32 - 1, -1, -1):
        s = result[i] + carry
        result[i] = s % 2
        carry = s // 2
    return result

def add_twos_complement(a, b):
    result = np.zeros(BITS32, dtype=int)
    carry = 0
    for i in range(BITS32 - 1, -1, -1):
        s = a[i] + b[i] + carry
        result[i] = s % 2
        carry = s // 2
    return result

def twos_to_decimal(arr):
    if arr[0] == 0:
        value = 0
        for bit in arr:
            value = value * 2 + bit
        return value
    inverted = 1 - arr
    carry = 1
    for i in range(BITS32 - 1, -1, -1):
        s = inverted[i] + carry
        inverted[i] = s % 2
        carry = s // 2
    value = 0
    for bit in inverted:
        value = value * 2 + bit
    return -value

def subtract_twos_complement(a, b):
    result = add_twos_complement(a, b)
    return result

def multiply_direct(a_arr, b_arr):
    sign = a_arr[0] ^ b_arr[0]
    a = a_arr[1:]
    b = b_arr[1:]
    result = np.zeros(31, dtype=int)
    for i in range(30, -1, -1):
        if b[i] == 1:
            shift = 30 - i
            temp = np.zeros(31, dtype=int)
            if shift == 0:
                temp[:] = a
            else:
                temp[:31-shift] = a[shift:]
            carry = 0
            for j in range(30, -1, -1):
                s = result[j] + temp[j] + carry
                result[j] = s % 2
                carry = s // 2
    final = np.zeros(32, dtype=int)
    final[0] = sign
    final[1:] = result
    return final

def compare_binary(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return True
        if a[i] < b[i]:
            return False
    return True

def subtract_binary(a, b):
    result = a.copy()
    borrow = 0
    for i in range(len(a) - 1, -1, -1):
        diff = result[i] - b[i] - borrow
        if diff < 0:
            result[i] = diff + 2
            borrow = 1
        else:
            result[i] = diff
            borrow = 0
    return result

def divide_direct(a_arr, b_arr):
    if np.all(b_arr[1:] == 0):
        raise ValueError("Division by zero")
    sign = a_arr[0] ^ b_arr[0]
    dividend = a_arr[1:].copy()
    divisor = b_arr[1:].copy()
    remainder = np.zeros(31, dtype=int)
    quotient = np.zeros(31, dtype=int)
    for i in range(31 + FRAC_BITS):
        remainder[:-1] = remainder[1:]
        if i < 31:
            remainder[-1] = dividend[i]
        else:
            remainder[-1] = 0
        if compare_binary(remainder, divisor):
            remainder = subtract_binary(remainder, divisor)
            if i >= FRAC_BITS:
                quotient[i - FRAC_BITS] = 1
    result = np.zeros(32, dtype=int)
    result[0] = sign
    result[1:] = quotient
    return result

def fixed_to_decimal(arr):
    sign = arr[0]
    magnitude = arr[1:]
    value = 0
    for bit in magnitude:
        value = value * 2 + bit
    value = value / (2 ** FRAC_BITS)
    if sign == 1:
        value = -value
    return value