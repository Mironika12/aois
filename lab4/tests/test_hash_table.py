import json
import pytest
from table.hash_table import HashTable
from table.utils import compute_v, compute_h, char_value
from table.hash_entry import HashEntry


# -------s---------------------
# utils.py
# ----------------------------

def test_char_value_valid():
    assert char_value('а') == 0
    assert char_value('я') == 32
    assert char_value('Б') == 1


def test_char_value_invalid():
    assert char_value('1') == -1
    assert char_value('@') == -1


def test_compute_v():
    assert compute_v("биология") == 42
    assert compute_v("наява") == 462


def test_compute_v_invalid_short():
    with pytest.raises(ValueError):
        compute_v("а")


def test_compute_v_invalid_symbols():
    with pytest.raises(ValueError):
        compute_v("12")


def test_compute_h():
    assert compute_h("биология", 23) == 19


# ----------------------------
# hash_entry.py
# ----------------------------

def test_hash_entry_clear():
    entry = HashEntry("ключ", "значение")

    entry.U = 1
    entry.C = 1
    entry.D = 1

    entry.clear()

    assert entry.key is None
    assert entry.value is None

    assert entry.U == 0
    assert entry.C == 0
    assert entry.D == 0


# ----------------------------
# hash_table.py
# ----------------------------

@pytest.fixture
def table():
    return HashTable()


def test_valid_key(table):
    assert table.is_valid_key("биология") is True


def test_invalid_key_short(table):
    assert table.is_valid_key("а") is False


def test_invalid_key_symbols(table):
    assert table.is_valid_key("bio123") is False


def test_quadratic_probe(table):
    assert table.quadratic_probe(7, 0) == 7
    assert table.quadratic_probe(7, 1) == 8
    assert table.quadratic_probe(7, 2) == 11


def test_insert(table):
    result = table.insert("биология", "наука")

    assert result is True
    assert table.count == 1


def test_insert_duplicate(table):
    table.insert("биология", "наука")

    result = table.insert("биология", "другое")

    assert result is False
    assert table.count == 1


def test_insert_invalid_key(table):
    result = table.insert("1", "тест")

    assert result is False


def test_search_existing(table):
    table.insert("биология", "наука")

    assert table.search("биология") == "наука"


def test_search_missing(table):
    assert table.search("неизвестно") is None


def test_search_invalid_key(table):
    assert table.search("1") is None


def test_update_existing(table):
    table.insert("биология", "наука")

    result = table.update("биология", "новое значение")

    assert result is True
    assert table.search("биология") == "новое значение"


def test_update_missing(table):
    assert table.update("неизвестно", "данные") is False


def test_delete_existing(table):
    table.insert("биология", "наука")

    result = table.delete("биология")

    assert result is True
    assert table.search("биология") is None
    assert table.count == 0


def test_delete_missing(table):
    assert table.delete("неизвестно") is False


def test_load_factor_empty(table):
    assert table.load_factor() == 0


def test_load_factor_non_empty(table):
    table.insert("биология", "наука")

    assert table.load_factor() == 1 / 23


def test_collision_handling(table):
    table.insert("биология", "1")
    table.insert("биоценоз", "2")

    assert table.collisions > 0
    assert table.search("биология") == "1"
    assert table.search("биоценоз") == "2"


def test_deleted_cell_reuse(table):
    table.insert("биология", "1")

    table.delete("биология")

    result = table.insert("биоценоз", "2")

    assert result is True


def test_display(table, capsys):
    table.insert("биология", "наука")

    table.display()

    captured = capsys.readouterr()

    assert "биология" in captured.out
    assert "наука" in captured.out


# ----------------------------
# load_from_json
# ----------------------------

def test_load_from_json_success(tmp_path):
    data = [
        {
            "key": "биология",
            "value": "наука"
        },
        {
            "key": "биоценоз",
            "value": "организмы"
        }
    ]

    file = tmp_path / "data.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    table = HashTable()

    result = table.load_from_json(file)

    assert result is True
    assert table.count == 2


def test_load_from_json_missing_file():
    table = HashTable()

    result = table.load_from_json("missing.json")

    assert result is False


def test_load_from_json_invalid_json(tmp_path):
    file = tmp_path / "bad.json"

    with open(file, "w", encoding="utf-8") as f:
        f.write("{ invalid json")

    table = HashTable()

    result = table.load_from_json(file)

    assert result is False


def test_load_from_json_not_list(tmp_path):
    file = tmp_path / "bad.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump({"a": 1}, f)

    table = HashTable()

    result = table.load_from_json(file)

    assert result is False


def test_load_from_json_partial_invalid(tmp_path):
    data = [
        {
            "key": "биология",
            "value": "наука"
        },
        {
            "bad": "object"
        }
    ]

    file = tmp_path / "mixed.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    table = HashTable()

    result = table.load_from_json(file)

    assert result is True
    assert table.count == 1