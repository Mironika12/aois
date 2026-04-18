import pytest

from logic.minimization_calc_method import (
    can_merge,
    merge_terms,
    merge_once,
    merge_all,
    covers,
    term_literal_count,
    dedupe_terms,
    remove_redundant,
    build_coverage_table,
    find_essential_implicants,
    remove_covered_columns,
    select_remaining,
    merge_stages,
    minimize,
    minimize_table_method
)


# ---------------- helpers ----------------

@pytest.fixture
def simple_terms():
    return [
        {"a": False, "b": False},
        {"a": False, "b": True},
        {"a": True, "b": False},
    ]


# ---------------- can_merge ----------------

def test_can_merge_true():
    t1 = {"a": True, "b": False}
    t2 = {"a": True, "b": True}
    assert can_merge(t1, t2) is True


def test_can_merge_false_multiple_diff():
    t1 = {"a": True, "b": False}
    t2 = {"a": False, "b": True}
    assert can_merge(t1, t2) is False


def test_can_merge_with_none():
    t1 = {"a": None, "b": False}
    t2 = {"a": True, "b": False}
    assert can_merge(t1, t2) is False


# ---------------- merge_terms ----------------

def test_merge_terms_basic():
    t1 = {"a": True, "b": False}
    t2 = {"a": True, "b": True}
    assert merge_terms(t1, t2) == {"a": True, "b": None}


# ---------------- merge_once ----------------

def test_merge_once_changes():
    terms = [
        {"a": True, "b": False},
        {"a": True, "b": True},
    ]
    new_terms, changed = merge_once(terms)

    assert changed is True
    assert {"a": True, "b": None} in new_terms


def test_merge_once_no_change():
    terms = [{"a": True, "b": False}]
    new_terms, changed = merge_once(terms)

    assert changed is False
    assert new_terms == terms


# ---------------- merge_all ----------------

def test_merge_all():
    terms = [
        {"a": False, "b": False},
        {"a": False, "b": True},
    ]
    result = merge_all(terms)

    assert result == [{"a": False, "b": None}]


# ---------------- covers ----------------

def test_covers_true():
    term = {"a": True, "b": None}
    row = {"a": True, "b": False}
    assert covers(term, row) is True


def test_covers_false():
    term = {"a": True, "b": None}
    row = {"a": False, "b": False}
    assert covers(term, row) is False


# ---------------- term_literal_count ----------------

def test_term_literal_count():
    term = {"a": True, "b": None, "c": False}
    assert term_literal_count(term) == 2


# ---------------- dedupe_terms ----------------

def test_dedupe_terms():
    terms = [{"a": True}, {"a": True}]
    assert dedupe_terms(terms) == [{"a": True}]


# ---------------- remove_redundant ----------------

def test_remove_redundant_basic():
    terms = [
        {"a": True, "b": None},
        {"a": True, "b": False},
    ]
    original = [
        {"a": True, "b": False},
    ]

    result = remove_redundant(terms, original)

    assert result == [{"a": True, "b": None}]


def test_remove_redundant_empty():
    assert remove_redundant([], []) == []


def test_remove_redundant_no_cover():
    terms = [{"a": True}]
    original = [{"a": False}]

    result = remove_redundant(terms, original)
    assert result == []


# ---------------- build_coverage_table ----------------

def test_build_coverage_table():
    terms = [{"a": True}]
    original = [{"a": True}, {"a": False}]

    table = build_coverage_table(terms, original)
    assert table == [[1, 0]]


# ---------------- find_essential_implicants ----------------

def test_find_essential_implicants():
    table = [
        [1, 0],
        [0, 1],
    ]
    result = find_essential_implicants(table)
    assert result == {0, 1}


def test_find_essential_implicants_empty():
    assert find_essential_implicants([]) == set()


# ---------------- remove_covered_columns ----------------

def test_remove_covered_columns():
    table = [
        [1, 0],
        [1, 1],
    ]
    result = remove_covered_columns(table, {0})

    assert result == [
        [0],
        [1],
    ]


# ---------------- select_remaining ----------------

def test_select_remaining_basic():
    table = [
        [1, 0],
        [1, 1],
    ]
    result = select_remaining(table, set())

    assert result  # хотя бы что-то выбрано


def test_select_remaining_empty():
    result = select_remaining([], set())
    assert result == set()


# ---------------- merge_stages ----------------

def test_merge_stages():
    terms = [
        {"a": False, "b": False},
        {"a": False, "b": True},
    ]
    stages = merge_stages(terms)

    assert len(stages) >= 1
    assert stages[0] == terms


# ---------------- minimize ----------------

def test_minimize():
    terms = [
        {"a": False, "b": False},
        {"a": False, "b": True},
    ]
    result = minimize(terms)

    assert result == [{"a": False, "b": None}]


# ---------------- minimize_table_method ----------------

def test_minimize_table_method():
    terms = [
        {"a": True, "b": False},
        {"a": True, "b": True},
    ]

    result = minimize_table_method(terms)

    assert result == [{"a": True, "b": None}]


def test_merge_once_partial_usage():
    terms = [
        {"a": True, "b": False},
        {"a": True, "b": True},
        {"a": False, "b": False},
    ]

    new_terms, changed = merge_once(terms)

    assert {"a": True, "b": None} in new_terms
    assert {"a": None, "b": False} in new_terms
    assert {"a": False, "b": False} not in new_terms
    assert changed is True


def test_merge_all_multiple_steps():
    terms = [
        {"a": False, "b": False, "c": False},
        {"a": False, "b": False, "c": True},
        {"a": False, "b": True, "c": False},
        {"a": False, "b": True, "c": True},
    ]

    result = merge_all(terms)

    assert result == [{"a": False, "b": None, "c": None}]


def test_remove_redundant_no_solution():
    terms = [{"a": True}]
    original = [{"a": False}]

    # никто не покрывает → candidates пустые
    result = remove_redundant(terms, original)

    assert result == []


def test_remove_redundant_choice():
    terms = [
        {"a": True, "b": None},   # покрывает оба
        {"a": True, "b": False},  # частично
        {"a": True, "b": True},   # частично
    ]

    original = [
        {"a": True, "b": False},
        {"a": True, "b": True},
    ]

    result = remove_redundant(terms, original)

    # должен выбрать самый общий терм
    assert result == [{"a": True, "b": None}]


def test_remove_covered_columns_all_removed():
    table = [
        [1, 1],
        [1, 1],
    ]

    result = remove_covered_columns(table, {0})

    assert result == [[], []]


def test_select_remaining_no_progress():
    table = [
        [0, 0],
        [0, 0],
    ]

    result = select_remaining(table, set())

    assert result == set()


