from config import *
from table.hash_entry import HashEntry
from table.utils import compute_v, compute_h
import json


class HashTable:
    def __init__(self, size=TABLE_SIZE):
        self.size = size
        self.table = [HashEntry() for _ in range(size)]

        self.count = 0
        self.collisions = 0


    def is_valid_key(self, key):
        if len(key) < 2:
            return False

        return all('а' <= ch.lower() <= 'я' or ch.lower() == 'ё'
                   for ch in key)
    

    def quadratic_probe(self, h, i):
        return (h + i ** 2) % self.size
    

    def insert(self, key, value, rehashing=False):
        if not self.is_valid_key(key):
            print("Некорректный ключ")
            return False

        if self.search(key) is not None:
            print("Ключ уже существует")
            return False
        
        if not rehashing and ((self.count + 1) / self.size) > MAX_LOAD_FACTOR:
            print("Превышен коэффициент заполнения, выполняется расширение таблицы")
            self.rehash()

        v = compute_v(key)
        h = compute_h(key, self.size)

        print(f"V({key}) = {v}")
        print(f"h({key}) = {h}")

        i = 0

        while i < self.size:
            idx = self.quadratic_probe(h, i)

            entry = self.table[idx]

            if entry.U == 0 or entry.D == 1:
                entry.key = key
                entry.value = value

                entry.U = 1
                entry.D = 0
                entry.T = 1

                if i > 0:
                    entry.C = 1
                    self.collisions += 1

                self.count += 1

                return True
            
            if entry.U == 1:
                self.collisions += 1

            i += 1

        print("Таблица переполнена")
        return False
    

    def search(self, key):
        if not self.is_valid_key(key):
            return None

        h = compute_h(key, self.size)
        i = 0

        while i < self.size:
            idx = self.quadratic_probe(h, i)

            entry = self.table[idx]

            if entry.U == 0 and entry.D == 0:
                return None

            if entry.U == 1 and entry.D == 0 and entry.key == key:
                return entry.value

            i += 1

        return None
    

    def update(self, key, new_value):
        h = compute_h(key, self.size)
        i = 0

        while i < self.size:
            idx = self.quadratic_probe(h, i)

            entry = self.table[idx]

            if entry.U == 0 and entry.D == 0:
                return False

            if entry.U == 1 and entry.D == 0 and entry.key == key:
                entry.value = new_value
                return True

            i += 1

        return False
    

    def delete(self, key):
        h = compute_h(key, self.size)
        i = 0

        while i < self.size:
            idx = self.quadratic_probe(h, i)

            entry = self.table[idx]

            if entry.U == 0 and entry.D == 0:
                return False

            if entry.U == 1 and entry.D == 0 and entry.key == key:
                entry.D = 1
                entry.U = 0

                self.count -= 1

                return True

            i += 1

        return False
    
    def load_factor(self):
        return self.count / self.size


    def display(self):
        print("-" * 120)
        print(f"{'Idx':<5} {'Key':<15} {'V(K)':<6} {'h(V)':<6} "
              f"{'U':<3} {'C':<3} {'D':<3} {'Value'}")
        print("-" * 120)

        for i, entry in enumerate(self.table):

            if entry.key is None:
                print(f"{i:<5} {'FREE':<15}")
                continue

            v = compute_v(entry.key)
            h = compute_h(entry.key, self.size)

            print(f"{i:<5} "
                  f"{entry.key:<15} "
                  f"{v:<6} "
                  f"{h:<6} "
                  f"{entry.U:<3} "
                  f"{entry.C:<3} "
                  f"{entry.D:<3} "
                  f"{entry.value}")

        print("-" * 120)
        print(f"Заполненность: {self.load_factor():.2f}")
        print(f"Количество коллизий: {self.collisions}")

    def load_from_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("Ошибка: JSON должен содержать список объектов")
                return False

            loaded = 0

            for item in data:

                if not isinstance(item, dict):
                    continue

                key = item.get("key")
                value = item.get("value")

                if key is None or value is None:
                    continue

                if self.insert(str(key), str(value)):
                    loaded += 1

            print(f"Загружено записей: {loaded}")
            return True

        except FileNotFoundError:
            print("Файл не найден")
            return False

        except json.JSONDecodeError:
            print("Ошибка JSON")
            return False

        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        
    def rehash(self):
        old_table = self.table

        self.size = self.size * 2 + 1
        self.table = [HashEntry() for _ in range(self.size)]
        self.count = 0
        self.collisions = 0

        for entry in old_table:
            if entry.U == 1 and entry.D == 0:
                self.insert(entry.key, entry.value, rehashing=True)