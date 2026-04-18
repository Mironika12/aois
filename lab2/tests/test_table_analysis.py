import pytest

from logic.table_analysis import (
    numeric_sdnf,
    numeric_sknf,
    index_form,
    build_sdnf,
    build_sknf,
    term_to_str,
    print_terms
)


# ---------------- helpers ----------------

@pytest.fixture
def simple_table():
    return [
        {"a": 0, "b": 0, "f": 0},
        {"a": 0, "b": 1, "f": 1},
        {"a": 1, "b": 0, "f": 1},
        {"a": 1, "b": 1, "f": 0},
    ]


# ---------------- numeric forms ----------------

def test_numeric_sdnf(simple_table):
    assert numeric_sdnf(simple_table) == [2, 3]


def test_numeric_sknf(simple_table):
    assert numeric_sknf(simple_table) == [1, 4]


# ---------------- index form ----------------

def test_index_form(simple_table):
    assert index_form(simple_table) == "0110"


def test_index_form_all_zero():
    table = [{"a": 0, "f": 0}, {"a": 1, "f": 0}]
    assert index_form(table) == "00"


def test_index_form_all_one():
    table = [{"a": 0, "f": 1}, {"a": 1, "f": 1}]
    assert index_form(table) == "11"


# ---------------- build_sdnf / build_sknf ----------------

def test_build_sdnf(simple_table):
    terms = build_sdnf(simple_table)

    assert terms == [
        {"a": False, "b": True},
        {"a": True, "b": False},
    ]


def test_build_sknf(simple_table):
    terms = build_sknf(simple_table)

    assert terms == [
        {"a": True, "b": True},
        {"a": False, "b": False},
    ]


def test_build_sdnf_empty():
    table = [{"a": 0, "f": 0}, {"a": 1, "f": 0}]
    assert build_sdnf(table) == []


def test_build_sknf_empty():
    table = [{"a": 0, "f": 1}, {"a": 1, "f": 1}]
    assert build_sknf(table) == []


# ---------------- term_to_str ----------------

def test_term_to_str_sdnf():
    term = {"a": True, "b": False}
    result = term_to_str(term, is_sdnf=True)
    assert result == "a & !b"


def test_term_to_str_sknf():
    term = {"a": True, "b": False}
    result = term_to_str(term, is_sdnf=False)
    assert result == "a | !b"


def test_term_to_str_with_none():
    term = {"a": True, "b": None}
    result = term_to_str(term, is_sdnf=True)
    assert result == "a"


def test_term_to_str_all_none_sdnf():
    term = {"a": None, "b": None}
    result = term_to_str(term, is_sdnf=True)
    assert result == "1"


def test_term_to_str_all_none_sknf():
    term = {"a": None, "b": None}
    result = term_to_str(term, is_sdnf=False)
    assert result == "0"


# ---------------- print_terms ----------------

def test_print_terms_sdnf(capsys):
    terms = [{"a": True}, {"a": False}]
    print_terms(terms, is_sdnf=True)

    captured = capsys.readouterr()
    assert "(a)" in captured.out
    assert "(!a)" in captured.out


def test_print_terms_sknf(capsys):
    terms = [{"a": True}, {"a": False}]
    print_terms(terms, is_sdnf=False)

    captured = capsys.readouterr()
    assert "(a)" in captured.out
    assert "(!a)" in captured.out


def test_print_terms_empty_sdnf(capsys):
    print_terms([], is_sdnf=True)

    captured = capsys.readouterr()
    assert "0" in captured.out


def test_print_terms_empty_sknf(capsys):
    print_terms([], is_sdnf=False)

    captured = capsys.readouterr()
    assert "1" in captured.out