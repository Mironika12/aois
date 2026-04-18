from config import (
    CONSTANT_0, CONSTANT_1,
    AND, OR, EMPTY_SET
)

def can_merge(term1: dict, term2: dict) -> bool:
    diff = 0

    for k in term1:
        v1, v2 = term1[k], term2[k]

        if v1 != v2:
            if v1 is None or v2 is None:
                return False
            diff += 1

    return diff == 1


def merge_terms(term1: dict, term2: dict) -> dict:
    merged = {}

    for k in term1:
        if term1[k] == term2[k]:
            merged[k] = term1[k]
        else:
            merged[k] = None

    return merged

def merge_once(terms: list[dict]) -> tuple[list[dict], bool]:
    new_terms = []
    used = [False] * len(terms)

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            if can_merge(terms[i], terms[j]):
                merged = merge_terms(terms[i], terms[j])

                if merged not in new_terms:
                    new_terms.append(merged)

                used[i] = True
                used[j] = True

    for i in range(len(terms)):
        if not used[i]:
            if terms[i] not in new_terms:
                new_terms.append(terms[i])

    changed = len(new_terms) != len(terms)

    return new_terms, changed

def merge_all(terms: list[dict]) -> list[dict]:
    while True:
        new_terms, _ = merge_once(terms)

        if new_terms == terms:
            return terms

        terms = new_terms

def covers(term: dict, row: dict) -> bool:
    for k in term:
        if term[k] is None:
            continue
        if term[k] != row[k]:
            return False
    return True

def term_literal_count(term: dict) -> int:
    return sum(value is not None for value in term.values())


def dedupe_terms(terms: list[dict]) -> list[dict]:
    unique = []
    for term in terms:
        if term not in unique:
            unique.append(term)
    return unique


def remove_redundant(terms: list[dict], original_terms: list[dict]) -> list[dict]:
    terms = dedupe_terms(terms)
    original_terms = dedupe_terms(original_terms)

    if not terms or not original_terms:
        return terms

    # Для каждого терма считаем, какие исходные наборы он покрывает
    cover_masks = []
    for term in terms:
        mask = 0
        for i, row in enumerate(original_terms):
            if covers(term, row):
                mask |= 1 << i
        cover_masks.append(mask)

    full_mask = (1 << len(original_terms)) - 1

    # Если какой-то терм вообще ничего не покрывает, он бесполезен
    candidates = [i for i, mask in enumerate(cover_masks) if mask != 0]
    if not candidates:
        return []

    # Сортировка для более быстрого поиска: сначала термы с большим покрытием
    candidates.sort(key=lambda i: (-cover_masks[i].bit_count(), term_literal_count(terms[i])))

    best_indices = None
    best_key = None

    def dfs(pos: int, chosen: list[int], covered_mask: int, literal_count: int):
        nonlocal best_indices, best_key

        if covered_mask == full_mask:
            key = (len(chosen), literal_count, tuple(chosen))
            if best_key is None or key < best_key:
                best_key = key
                best_indices = chosen.copy()
            return

        if pos >= len(candidates):
            return

        # Если уже не лучше текущего лучшего решения, дальше идти смысла нет
        if best_key is not None and len(chosen) >= best_key[0]:
            return

        idx = candidates[pos]

        # Взять терм
        dfs(
            pos + 1,
            chosen + [idx],
            covered_mask | cover_masks[idx],
            literal_count + term_literal_count(terms[idx])
        )

        # Не брать терм
        dfs(pos + 1, chosen, covered_mask, literal_count)

    dfs(0, [], 0, 0)

    if best_indices is None:
        return terms

    result = [terms[i] for i in best_indices]
    return dedupe_terms(result)


def build_coverage_table(terms: list[dict], original_terms: list[dict]) -> list[list[int]]:
    table = []

    for term in terms:
        row = []
        for orig in original_terms:
            row.append(CONSTANT_1 if covers(term, orig) else CONSTANT_0)
        table.append(row)

    return table

def find_essential_implicants(table: list[list[int]]) -> set[int]:
    essential = set()

    if not table:
        return essential

    cols = len(table[0])

    for j in range(cols):
        covering = []

        for i in range(len(table)):
            if table[i][j] == 1:
                covering.append(i)

        if len(covering) == 1:
            essential.add(covering[0])

    return essential

def remove_covered_columns(table, selected_rows):
    cols = set()

    for r in selected_rows:
        for j, val in enumerate(table[r]):
            if val == 1:
                cols.add(j)

    new_table = []

    for row in table:
        new_row = [val for j, val in enumerate(row) if j not in cols]
        new_table.append(new_row)

    return new_table

def select_remaining(table: list[list[int]], used_rows: set[int]) -> set[int]:
    selected = set()

    while table and any(any(row) for row in table):
        # выбираем строку с максимальным покрытием
        best = -1
        best_count = -1

        for i, row in enumerate(table):
            if i in used_rows or i in selected:
                continue

            count = sum(row)
            if count > best_count:
                best = i
                best_count = count

        if best == -1:
            break

        selected.add(best)

        # удаляем покрытые столбцы
        covered_cols = [j for j, v in enumerate(table[best]) if v == 1]

        new_table = []
        for row in table:
            new_row = [v for j, v in enumerate(row) if j not in covered_cols]
            new_table.append(new_row)

        table = new_table

    return selected


def merge_stages(terms: list[dict]) -> list[list[dict]]:
    stages = [terms]

    while True:
        new_terms, _ = merge_once(terms)

        if new_terms == terms:
            break

        stages.append(new_terms)
        terms = new_terms

    return stages


def minimize(terms):
    return remove_redundant(merge_all(terms), terms)


def minimize_table_method(terms: list[dict]) -> list[dict]:
    original_terms = terms.copy()

    # 1. склеивание
    terms = merge_all(terms)

    # 2. таблица
    table = build_coverage_table(terms, original_terms)

    # 3. существенные
    essential = find_essential_implicants(table)

    # 4. убрать покрытые
    reduced_table = remove_covered_columns(table, essential)

    # 5. добрать
    extra = select_remaining(reduced_table, essential)

    selected = essential.union(extra)

    return [terms[i] for i in selected]
