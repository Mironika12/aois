from config import AND, XOR

def is_T0(table: list[dict]) -> bool:
    return not bool(table[0]['f'])

def is_T1(table: list[dict]) -> bool:
    return bool(table[-1]['f'])

def is_self_dual(table: list[dict]) -> bool:
    for i in range(len(table)):
        if table[i]['f'] == table[-(i+1)]['f']:
            return False
    return True

def leq(row1: dict, row2: dict) -> bool:
    for k in row1:
        if k == 'f':
            continue
        if row1[k] > row2[k]:
            return False
    return True

def is_monotonic(table: list[dict]) -> bool:
    n = len(table)

    for i in range(n):
        for j in range(n):
            if leq(table[i], table[j]):
                if table[i]['f'] > table[j]['f']:
                    return False

    return True

def zhegalkin_coeffs(values: list[int]) -> list[int]:
    coeffs = []
    current = values[:]

    while current:
        coeffs.append(current[0])
        current = [
            current[i] ^ current[i + 1]
            for i in range(len(current) - 1)
        ]

    return coeffs

def is_linear(table: list[dict]) -> bool:
    values = [int(row['f']) for row in table]
    coeffs = zhegalkin_coeffs(values)

    for i, c in enumerate(coeffs):
        if c == 0:
            continue

        # если больше одной единицы → это произведение (ab, abc)
        if bin(i).count('1') > 1:
            return False

    return True

def zhegalkin_polynomial(table: list[dict]) -> str:
    values = [int(row['f']) for row in table]
    coeffs = zhegalkin_coeffs(values)

    vars = [k for k in table[0].keys() if k != 'f']
    terms = []

    for i, c in enumerate(coeffs):
        if c == 0:
            continue

        if i == 0:
            terms.append("1")
            continue

        bits = bin(i)[2:].zfill(len(vars))
        term = []

        for bit, var in zip(bits, vars):
            if bit == '1':
                term.append(var)

        terms.append(AND.join(term))

    return f" {XOR} ".join(terms) if terms else "0"