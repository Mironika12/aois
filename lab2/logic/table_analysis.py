from config import (
    NOT, AND, OR,
    CONSTANT_0, CONSTANT_1
)

def numeric_sdnf(table: list[dict]) -> list[int]:
    return [i+1 for i, row in enumerate(table) if row['f']]


def numeric_sknf(table: list[dict]) -> list[int]:
    return [i+1 for i, row in enumerate(table) if not row['f']]


def index_form(table: list[dict]) -> str:
    return "".join(str(int(row['f'])) for row in table)


def build_sdnf(table: list[dict]) -> list[dict]:
    terms = []

    for row in table:
        if row['f']:
            term = {}

            for var, value in row.items():
                if var == 'f':
                    continue

                term[var] = bool(value)

            terms.append(term)

    return terms


def build_sknf(table: list[dict]) -> list[dict]:
    terms = []

    for row in table:
        if not row['f']:
            term = {}

            for var, value in row.items():
                if var == 'f':
                    continue

                # обратная логика
                term[var] = not bool(value)

            terms.append(term)

    return terms


def term_to_str(term: dict, is_sdnf: bool) -> str:
    parts = []

    for var, value in term.items():
        if value is None:
            continue

        if value:
            parts.append(var)
        else:
            parts.append(f"{NOT}{var}")

    if not parts:
        return str(CONSTANT_1) if is_sdnf else str(CONSTANT_0)

    sep = f" {AND} " if is_sdnf else f" {OR} "
    return sep.join(parts)


def print_terms(terms: list[dict], is_sdnf=True):
    if not terms:
        print(CONSTANT_0 if is_sdnf else CONSTANT_1)
        return

    sep = f" {OR} " if is_sdnf else f" {AND} "

    expr = sep.join(f"({term_to_str(t, is_sdnf)})" for t in terms)
    print(expr)