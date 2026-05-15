from config import *


def char_value(ch):
    return RUS_ALPHABET.get(ch.lower(), -1)


# V(K)
def compute_v(key):
    key = key.lower()

    if len(key) < 2:
        raise ValueError("Ключ должен содержать минимум 2 символа")

    v1 = char_value(key[0])
    v2 = char_value(key[1])

    if v1 == -1 or v2 == -1:
        raise ValueError("Недопустимые символы")

    return v1 * ALPHABET_SIZE + v2


# h(V)
def compute_h(key, table_size):
    v = compute_v(key)
    return v % table_size + INITIAL_ADDRESS