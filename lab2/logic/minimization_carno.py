from config import CONSTANT_0, CONSTANT_1


def gray_code(n: int) -> list[list[int]]:
    if n == 0:
        return [[]]

    prev = gray_code(n - 1)

    return (
        [[0] + code for code in prev] +
        [[1] + code for code in reversed(prev)]
    )

def build_kmap(table: list[dict]):
    vars = [k for k in table[0] if k != 'f']
    n = len(vars)

    row_vars = vars[: n // 2]
    col_vars = vars[n // 2 :]

    row_codes = gray_code(len(row_vars))
    col_codes = gray_code(len(col_vars))

    kmap = [[0 for _ in col_codes] for _ in row_codes]

    for row in table:
        r = [int(row[v]) for v in row_vars]
        c = [int(row[v]) for v in col_vars]

        i = row_codes.index(r)
        j = col_codes.index(c)

        kmap[i][j] = int(row['f'])

    return kmap, vars, row_codes, col_codes

def is_valid_group(kmap, cells, target):
    return all(kmap[i][j] == target for i, j in cells)

def get_all_groups(kmap, target):
    rows = len(kmap)
    cols = len(kmap[0])

    groups = []

    for h in [1, 2, rows]:
        for w in [1, 2, cols]:
            if h * w == 0:
                continue

            for i in range(rows):
                for j in range(cols):

                    cells = []
                    for di in range(h):
                        for dj in range(w):
                            ni = (i + di) % rows
                            nj = (j + dj) % cols
                            cells.append((ni, nj))

                    if is_valid_group(kmap, cells, target):
                        groups.append(cells)

    return groups

def remove_subgroups(groups):
    result = []

    for g in groups:
        if not any(set(g) < set(other) for other in groups if g != other):
            result.append(g)

    return result

def group_to_term(group, vars, row_codes, col_codes, is_sdnf):
    values = {v: set() for v in vars}

    for i, j in group:
        bits = row_codes[i] + col_codes[j]

        for v, b in zip(vars, bits):
            values[v].add(b)

    term = {}

    for v in vars:
        if len(values[v]) == 1:
            val = next(iter(values[v]))

            if is_sdnf:
                term[v] = bool(val)
            else:
                term[v] = not bool(val)
        else:
            term[v] = None

    return term

def minimize_kmap(table: list[dict], is_sdnf=True):
    kmap, vars, row_codes, col_codes = build_kmap(table)

    target = CONSTANT_1 if is_sdnf else CONSTANT_0

    groups = get_all_groups(kmap, target)
    groups = remove_subgroups(groups)

    terms = []

    for g in groups:
        term = group_to_term(g, vars, row_codes, col_codes, is_sdnf)
        if term not in terms:
            terms.append(term)

    return terms


def print_kmap(table: list[dict]):
    kmap, vars, row_codes, col_codes = build_kmap(table)

    row_vars = vars[: len(row_codes[0])]

    # заголовок колонок
    col_labels = ["".join(map(str, code)) for code in col_codes]

    # ширина
    cell_w = max(3, max(len(lbl) for lbl in col_labels) + 1)

    # верхняя строка
    print(" " * (len(row_vars) + 2) + "".join(lbl.center(cell_w) for lbl in col_labels))

    # строки
    for i, row in enumerate(kmap):
        row_label = "".join(map(str, row_codes[i]))
        line = row_label.ljust(len(row_vars) + 2)

        for val in row:
            line += str(val).center(cell_w)

        print(line)