import pytest

from logic.table_build import (
    find_vars,
    generate_rows,
    convert_to_postfix,
    evaluate,
    build_table,
    is_higher_priority,
    read_expr,
    validate_tokens
)


# ---------------- find_vars ----------------

def test_find_vars_basic():
    expr = "a & b | c"
    assert find_vars(expr) == ["a", "b", "c"]


def test_find_vars_duplicates():
    expr = "a & a | b"
    assert find_vars(expr) == ["a", "b"]


def test_find_vars_with_digits():
    expr = "x1 & y2"
    assert find_vars(expr) == ["x1", "y2"]


# ---------------- generate_rows ----------------

def test_generate_rows_2_vars():
    vars = ["a", "b"]
    rows = generate_rows(vars)

    assert len(rows) == 4
    for row in rows:
        assert "a" in row and "b" in row and "f" in row
        assert row["f"] is None


def test_generate_rows_0_vars():
    rows = generate_rows([])
    assert rows == [{"f": None}]


# ---------------- convert_to_postfix ----------------

def test_convert_simple_and():
    expr = "a & b"
    assert convert_to_postfix(expr) == ["a", "b", "&"]


def test_convert_with_not():
    expr = "!a"
    assert convert_to_postfix(expr) == ["a", "!"]


def test_convert_priority():
    expr = "a | b & c"
    # & выше |
    assert convert_to_postfix(expr) == ["a", "b", "c", "&", "|"]


def test_convert_brackets():
    expr = "(a | b) & c"
    assert convert_to_postfix(expr) == ["a", "b", "|", "c", "&"]


def test_convert_implication():
    expr = "a -> b"
    assert convert_to_postfix(expr) == ["a", "b", "->"]


def test_convert_equivalence():
    expr = "a ~ b"
    assert convert_to_postfix(expr) == ["a", "b", "~"]


def test_convert_unmatched_brackets():
    with pytest.raises(ValueError):
        convert_to_postfix("(a & b")


def test_convert_invalid_token():
    with pytest.raises(ValueError):
        convert_to_postfix("a $ b")


# ---------------- is_higher_priority ----------------

def test_priority_and_vs_or():
    assert is_higher_priority("|", "&") is True


def test_priority_not_right_assoc():
    assert is_higher_priority("!", "!") is False


def test_priority_with_bracket():
    assert is_higher_priority("&", "(") is False


# ---------------- evaluate ----------------

def test_evaluate_and():
    expr = ["a", "b", "&"]
    row = {"a": True, "b": False}
    assert evaluate(expr, row) is False


def test_evaluate_or():
    expr = ["a", "b", "|"]
    row = {"a": False, "b": True}
    assert evaluate(expr, row) is True


def test_evaluate_not():
    expr = ["a", "!"]
    row = {"a": False}
    assert evaluate(expr, row) is True


def test_evaluate_implication():
    expr = ["a", "b", "->"]
    row = {"a": True, "b": False}
    assert evaluate(expr, row) is False


def test_evaluate_equivalence():
    expr = ["a", "b", "~"]
    row = {"a": True, "b": True}
    assert evaluate(expr, row) is True


def test_evaluate_complex():
    expr = convert_to_postfix("(a & b) | !c")
    row = {"a": True, "b": True, "c": False}
    assert evaluate(expr, row) is True


def test_evaluate_invalid_stack():
    with pytest.raises(IndexError):
        evaluate(["&"], {})


def test_evaluate_invalid_operation():
    with pytest.raises(ValueError):
        evaluate(["a", "b", "^"], {"a": True, "b": False})


def test_evaluate_wrong_stack_size():
    with pytest.raises(ValueError):
        evaluate(["a", "b"], {"a": True, "b": False})


# ---------------- build_table ----------------

def test_build_table_simple():
    table = build_table("a & b")

    assert len(table) == 4
    results = [row["f"] for row in table]

    assert results == [False, False, False, True]


def test_build_table_not():
    table = build_table("!a")
    results = [row["f"] for row in table]

    assert results == [True, False]


def test_build_table_multiple_ops():
    table = build_table("(a | b) & !c")
    assert len(table) == 8


def test_build_table_too_many_vars():
    expr = "a & b & c & d & e & f"
    with pytest.raises(ValueError):
        build_table(expr)

def test_read_expr(tmp_path):
    file = tmp_path / "expr.txt"
    file.write_text("a & b\n\nc | d\n")

    result = read_expr(file)

    assert result == ["a & b", "c | d"]

# def test_convert_no_operator():
#     with pytest.raises(ValueError):
#         convert_to_postfix("ab")

def test_convert_nested_brackets():
    expr = "((a & b) | c)"
    result = convert_to_postfix(expr)

    assert result == ["a", "b", "&", "c", "|"]

def test_convert_complex_expression():
    expr = "!(a & b) | c"
    result = convert_to_postfix(expr)

    assert "!" in result
    assert "|" in result

def test_priority_implication_right_assoc():
    # для -> должна быть правоассоциативность
    assert is_higher_priority("->", "->") is False

def test_evaluate_chain():
    expr = convert_to_postfix("a & b | c")
    row = {"a": True, "b": False, "c": True}

    assert evaluate(expr, row) is True

def test_evaluate_multiple_operations():
    expr = convert_to_postfix("(a & b) | (c & !d)")
    row = {"a": True, "b": True, "c": False, "d": False}

    assert evaluate(expr, row) is True

def test_build_table_one_var():
    table = build_table("a")

    assert len(table) == 2
    assert [row["f"] for row in table] == [False, True]

def test_build_table_complex():
    table = build_table("(a -> b) & !c")

    assert len(table) == 8
    assert all("f" in row for row in table)

def test_validate_simple_var():
    validate_tokens(["a"])


def test_validate_not():
    validate_tokens(["!", "a"])


def test_validate_binary():
    validate_tokens(["a", "&", "b"])


def test_validate_complex():
    validate_tokens(["(", "a", "&", "b", ")", "|", "c"])


def test_validate_missing_operator():
    with pytest.raises(ValueError):
        validate_tokens(["a", "b"])


def test_validate_missing_operand():
    with pytest.raises(ValueError):
        validate_tokens(["a", "&"])


def test_validate_starts_with_binary():
    with pytest.raises(ValueError):
        validate_tokens(["&", "a", "b"])


def test_validate_double_operator():
    with pytest.raises(ValueError):
        validate_tokens(["a", "&", "|", "b"])

def test_validate_invalid_not_usage():
    with pytest.raises(ValueError):
        validate_tokens(["a", "!", "b"])

def test_validate_unmatched_open_bracket():
    with pytest.raises(ValueError):
        validate_tokens(["(", "a", "&", "b"])


def test_validate_unmatched_close_bracket():
    with pytest.raises(ValueError):
        validate_tokens(["a", "&", "b", ")"])


def test_validate_empty_brackets():
    with pytest.raises(ValueError):
        validate_tokens(["(", ")"])

def test_validate_ends_with_operator():
    with pytest.raises(ValueError):
        validate_tokens(["a", "&"])


def test_validate_empty():
    with pytest.raises(ValueError):
        validate_tokens([])


def test_validate_unknown_token():
    with pytest.raises(ValueError):
        validate_tokens(["a", "^", "b"])