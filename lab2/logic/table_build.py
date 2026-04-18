import re
from itertools import product

from config import (
    LOGIC_VAR, VAR_VALUES,
    MAX_VARS, OR, AND, NOT,
    IMPLICATION, EQUIVALENCE,
    EXPR_TEMPLATE, LOGIC_OPERATOR,
    OPEN_BRACKET, CLOSE_BRACKET,
    BINARY_OPERATORS, OPERATORS
)


def read_expr(filepath: str) -> list[str]:
    """Чтение логической функции из файла"""
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def find_vars(expr: str) -> list[str]:
    """Поиск переменных в выражении"""
    vars = set(re.findall(LOGIC_VAR, expr))
    return sorted(list(vars))


def generate_rows(vars: list[str]) -> list[dict]:
    table = []
    for combo in product(VAR_VALUES, repeat=len(vars)):
        row = dict(zip(vars, combo))
        row['f'] = None
        table.append(row)
    return table


def validate_tokens(tokens: list[str]):
    if not tokens:
        raise ValueError("Пустое выражение")

    balance = 0
    expect_operand = True  # ожидаем переменную или !

    for i, token in enumerate(tokens):
        if re.match(LOGIC_VAR, token):
            if not expect_operand:
                raise ValueError("Пропущен оператор")
            expect_operand = False

        elif token == NOT:
            if not expect_operand:
                raise ValueError("Некорректное использование !")
            # expect_operand остаётся True

        elif token in BINARY_OPERATORS:
            if expect_operand:
                raise ValueError("Пропущен операнд")
            expect_operand = True

        elif token == OPEN_BRACKET:
            if not expect_operand:
                raise ValueError("Пропущен оператор перед (")
            balance += 1

        elif token == CLOSE_BRACKET:
            if expect_operand:
                raise ValueError("Пустые или некорректные скобки")
            balance -= 1
            if balance < 0:
                raise ValueError("Несогласованные скобки")

        else:
            raise ValueError("Неизвестный токен")

    if balance != 0:
        raise ValueError("Несогласованные скобки")

    if expect_operand:
        raise ValueError("Выражение заканчивается оператором")


def convert_to_postfix(expr: str) -> list[str]:
    operator_stack = []
    output = []

    inp = re.findall(EXPR_TEMPLATE, expr)

    expr_clean = re.sub(r"\s+", "", expr)
    if "".join(inp) != expr_clean:
        raise ValueError("Неизвестный символ")

    validate_tokens(inp)

    for token in inp:
        if re.match(LOGIC_VAR, token):
            output.append(token)
        elif re.match(LOGIC_OPERATOR, token):
            while (
                operator_stack and
                is_higher_priority(token, operator_stack[-1])
            ):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == OPEN_BRACKET:
            operator_stack.append(token)
        elif token == CLOSE_BRACKET:
            while operator_stack and operator_stack[-1] != OPEN_BRACKET:
                output.append(operator_stack.pop())

            if not operator_stack:
                raise ValueError("Несогласованные скобки")

            operator_stack.pop()
        else:
            raise ValueError("Неизвестный символ")
        
    while operator_stack:
        op = operator_stack.pop()
        if op == OPEN_BRACKET:
            raise ValueError("Несогласованные скобки")
        output.append(op)
        
    return output


def is_higher_priority(operator: str, prev_operator: str) -> bool:
    priority = {
        '!': 4,
        '&': 3,
        '|': 2,
        '->': 1,
        '~': 0
    }

    right_assoc = {NOT, IMPLICATION, EQUIVALENCE}

    if prev_operator == OPEN_BRACKET:
        return False
    
    if operator in right_assoc:
        return priority[prev_operator] > priority[operator]
    
    return priority[prev_operator] >= priority[operator]


def evaluate(expr: list[str], row: dict) -> bool:
    stack = []

    for token in expr:
        if token == NOT:
            a = stack.pop()
            stack.append(not a)

        elif token in BINARY_OPERATORS:
            b = stack.pop()
            a = stack.pop()

            if token == AND:
                stack.append(a and b)
            elif token == OR:
                stack.append(a or b)
            elif token == IMPLICATION:
                stack.append(not a or b)
            elif token == EQUIVALENCE:
                stack.append(a == b)

        elif token in row:  # ← переменная
            stack.append(row[token])

        else:
            raise ValueError("Некорректный токен")

    if len(stack) != 1:
        raise ValueError("Ошибка вычисления")

    return stack.pop()

def build_table(expr: str) -> list[dict]:
    """Построение таблицы истинности"""
    postfix = convert_to_postfix(expr)
    vars = find_vars(expr)

    if len(vars) > MAX_VARS:
        raise ValueError("Слишком много переменных")

    table = generate_rows(vars)

    for row in table:
        row['f'] = evaluate(postfix, row)

    return table

def print_table(table: list[dict]):
    if not table:
        print("Таблица пустая")
        return

    # порядок колонок (переменные + f)
    headers = list(table[0].keys())

    # ширина колонок
    col_width = max(len(h) for h in headers) + 2

    # заголовок
    header_line = "".join(h.center(col_width) for h in headers)
    print(header_line)
    print("-" * len(header_line))

    # строки
    for row in table:
        line = ""
        for h in headers:
            value = int(row[h]) if isinstance(row[h], bool) else row[h]
            line += str(value).center(col_width)
        print(line)