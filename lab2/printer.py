from logic.table_analysis import term_to_str
from logic.minimization_calc_method import covers
from config import EMPTY_SET, OR, AND

def print_merge_stages(stages: list[list[dict]], is_sdnf=True):
    for i, stage in enumerate(stages):
        print(f"\nЭтап {i + 1}:")

        if not stage:
            print(EMPTY_SET)
            continue

        sep = f" {OR} " if is_sdnf else f" {AND} "

        expr = sep.join(
            f"({term_to_str(term, is_sdnf)})"
            for term in stage
        )

        print(expr)


def print_coverage_table(prime_terms, original_terms):
    if not original_terms:
        print("Функция константная — таблица покрытия не требуется")
        return

    if not prime_terms:
        print("Нет импликант")
        return

    # заголовки столбцов
    col_headers = [f"m{i+1}" for i in range(len(original_terms))]

    # ширина для выравнивания
    col_width = max(6, max(len(h) for h in col_headers) + 2)

    # печать заголовка
    header = " " * col_width
    for h in col_headers:
        header += h.center(col_width)
    print(header)

    # строки таблицы
    for i, term in enumerate(prime_terms):
        row_name = f"t{i+1}"
        row_str = row_name.ljust(col_width)

        for orig in original_terms:
            val = 1 if covers(term, orig) else 0
            row_str += str(val).center(col_width)

        print(row_str)
