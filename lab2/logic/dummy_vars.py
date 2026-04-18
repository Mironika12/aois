def get_neighbor_pairs(table: list[dict], var: str) -> list[tuple[int, int]]:
    vars = [k for k in table[0].keys() if k != 'f']
    n = len(vars)
    size = len(table)

    i = vars.index(var)
    step = 2 ** (n - i - 1)

    pairs = []

    for start in range(0, size, 2 * step):
        for j in range(step):
            idx1 = start + j
            idx2 = idx1 + step
            pairs.append((idx1, idx2))

    return pairs

def find_dummy_vars(table: list[dict]) -> list[str]:
    vars = [k for k in table[0].keys() if k != 'f']
    values = [int(row['f']) for row in table]

    dummy_vars = []

    for var in vars:
        pairs = get_neighbor_pairs(table, var)

        is_dummy = True

        for i, j in pairs:
            if values[i] != values[j]:
                is_dummy = False
                break

        if is_dummy:
            dummy_vars.append(var)

    return dummy_vars


def calculate_derivative(values: list[int], var_index: int, n: int) -> list[int]:
    size = len(values)
    step = 2 ** (n - var_index - 1)

    result = [0] * size

    for start in range(0, size, 2 * step):
        for j in range(step):
            i = start + j
            j2 = i + step

            val = values[i] ^ values[j2]

            result[i] = val
            result[j2] = val

    return result

def boolean_derivative(table: list[dict], var: str) -> list[int]:
    vars = [k for k in table[0].keys() if k != 'f']
    n = len(vars)

    values = [int(row['f']) for row in table]
    idx = vars.index(var)

    return calculate_derivative(values, idx, n)

def mixed_derivative(table: list[dict], vars_order: list[str]) -> list[int]:
    vars = [k for k in table[0].keys() if k != 'f']
    n = len(vars)

    values = [int(row['f']) for row in table]

    for var in vars_order:
        idx = vars.index(var)
        values = calculate_derivative(values, idx, n)

    return values