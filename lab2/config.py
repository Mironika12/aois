import re

LOGIC_VAR = r'[A-Za-z][A-Za-z1-9]*'
LOGIC_OPERATOR = r'^(->|[!&~|])$'
AND = '&'
OR = '|'
NOT = '!'
IMPLICATION = '->'
EQUIVALENCE = '~'
XOR = '^'
OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
BINARY_OPERATORS = [AND, OR, IMPLICATION, EQUIVALENCE]
OPERATORS = [NOT, AND, OR, IMPLICATION, EQUIVALENCE, XOR]


MAX_VARS = 5
VAR_VALUES = [False, True]

EXPR_TEMPLATE = r'[A-Za-z][A-Za-z1-9]*|->|[!&|~()]'

CONSTANT_1 = 1
CONSTANT_0 = 0

EMPTY_SET = "∅"


# и ещё много раз выводит смешанные
# и в целом у меня не все смешанные выводятся, а только до второй, надо исправить