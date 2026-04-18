import numpy as np
from binary_math.constants import *


def decimal_to_bcd(number: int, min_digits: int = 0) -> np.ndarray:
    if not isinstance(number, int):
        raise TypeError("number must be int")
    if number < 0:
        raise ValueError("Only non-negative integers are supported")

    number_str = str(number)
    total_digits = max(min_digits, len(number_str))
    number_str = number_str.zfill(total_digits)

    bcd_result = np.zeros(BCD_BITS * total_digits, dtype=int)

    for digit_index, char in enumerate(number_str):
        digit_value = ord(char) - ord('0')

        for bit_index in range(BCD_BITS):
            bit_position = digit_index * BCD_BITS + bit_index
            bcd_result[bit_position] = (digit_value >> (BCD_BITS - 1 - bit_index)) & 1

    return bcd_result


def bcd_to_decimal(bcd_bits) -> int:
    bits_array = np.asarray(bcd_bits, dtype=int).flatten()

    if bits_array.size % BCD_BITS != 0:
        raise ValueError("Length of BCD bit array must be multiple of 4")

    digit_count = bits_array.size // BCD_BITS
    decimal_result = 0

    for digit_index in range(digit_count):
        start = digit_index * BCD_BITS
        end = start + BCD_BITS

        digit_bits = bits_array[start:end]

        digit_value = 0
        for bit in digit_bits:
            digit_value = (digit_value << 1) | bit

        if digit_value >= BCD_BASE:
            raise ValueError(f"Invalid BCD digit {digit_value} in chunk {digit_index}")

        decimal_result = decimal_result * BCD_BASE + digit_value

    return decimal_result


def add_bcd(first_bcd, second_bcd):
    max_length = max(len(first_bcd), len(second_bcd))
    digit_count = max_length // BCD_BITS

    if len(first_bcd) < max_length:
        padding = np.zeros(max_length - len(first_bcd), dtype=int)
        first_bcd = np.concatenate((padding, first_bcd))

    if len(second_bcd) < max_length:
        padding = np.zeros(max_length - len(second_bcd), dtype=int)
        second_bcd = np.concatenate((padding, second_bcd))

    result = np.zeros(max_length, dtype=int)
    carry = 0

    for digit_index in range(digit_count - 1, -1, -1):
        start = digit_index * BCD_BITS

        first_digit = 0
        second_digit = 0

        for bit_index in range(BCD_BITS):
            first_digit = (first_digit << 1) | first_bcd[start + bit_index]
            second_digit = (second_digit << 1) | second_bcd[start + bit_index]

        digit_sum = first_digit + second_digit + carry

        if digit_sum >= BCD_BASE:
            result_digit = digit_sum - BCD_BASE
            carry = 1
        else:
            result_digit = digit_sum
            carry = 0

        for bit_index in range(BCD_BITS):
            result[start + bit_index] = (result_digit >> (BCD_BITS - 1 - bit_index)) & 1

    if carry:
        carry_block = np.array([0, 0, 0, 1])
        result = np.concatenate((carry_block, result))

    return result