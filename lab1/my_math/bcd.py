import numpy as np

def decimal_to_bcd(n: int, min_digits: int = 0) -> np.ndarray:
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 0:
        raise ValueError("only non-negative integers supported")
    s = str(n)
    digits = max(min_digits, len(s))
    s = s.zfill(digits)
    out = np.zeros(4 * digits, dtype=int)
    for i, ch in enumerate(s):
        d = ord(ch) - 48
        for j in range(4):
            out[i*4 + j] = (d >> (3 - j)) & 1
    return out

def bcd_to_decimal(bcd_bits) -> int:
    arr = np.asarray(bcd_bits, dtype=int).flatten()
    if arr.size % 4 != 0:
        raise ValueError("length of BCD bit array must be multiple of 4")
    nd = arr.size // 4
    val = 0
    for i in range(nd):
        chunk = arr[i*4:(i+1)*4]
        digit = 0
        for bit in chunk:
            digit = (digit << 1) | int(bit)
        if digit > 9:
            raise ValueError(f"invalid BCD digit {digit} in chunk {i}")
        val = val * 10 + digit
    return val

def add_bcd(a, b):
    n = max(len(a), len(b))
    nibbles = n // 4
    if len(a) < n:
        a = np.concatenate((np.zeros(n - len(a), dtype=int), a))
    if len(b) < n:
        b = np.concatenate((np.zeros(n - len(b), dtype=int), b))
    result = np.zeros(n, dtype=int)
    carry = 0
    for i in range(nibbles - 1, -1, -1):
        start = i * 4
        da = a[start]*8 + a[start+1]*4 + a[start+2]*2 + a[start+3]
        db = b[start]*8 + b[start+1]*4 + b[start+2]*2 + b[start+3]
        s = da + db + carry
        if s > 9:
            s += 6
            carry = 1
        else:
            carry = 0
        digit = s % 16
        result[start]   = (digit >> 3) & 1
        result[start+1] = (digit >> 2) & 1
        result[start+2] = (digit >> 1) & 1
        result[start+3] = digit & 1
    if carry:
        result = np.concatenate((np.array([0,0,0,1]), result))
    return result