from hash_table import HashTable


MENU = """
1. Добавить запись
2. Найти запись
3. Обновить запись
4. Удалить запись
5. Показать таблицу
6. Загрузить из JSON
7. Выход
"""


def main():

    ht = HashTable()

    while True:

        print(MENU)

        choice = input("Выбор: ")

        if choice == '1':
            key = input("Ключ: ")
            value = input("Значение: ")
            ht.insert(key, value)

        elif choice == '2':
            key = input("Ключ: ")
            result = ht.search(key)

            if result:
                print(result)
            else:
                print("Не найдено")

        elif choice == '3':
            key = input("Ключ: ")
            value = input("Новое значение: ")

            if ht.update(key, value):
                print("Обновлено")
            else:
                print("Ключ не найден")

        elif choice == '4':
            key = input("Ключ: ")

            if ht.delete(key):
                print("Удалено")
            else:
                print("Ключ не найден")

        elif choice == '5':
            ht.display()

        elif choice == '6':
            filename = input("Имя JSON файла: ")
            ht.load_from_json(filename)

        elif choice == '7':
            break

if __name__ == "__main__":
    main()

# class HashEntry:
#     def __init__(self, key=None, value=None):
#         self.key = key
#         self.value = value
#         self.C = 0  # коллизия
#         self.U = 0  # занято
#         self.T = 0  # терминальный
#         self.L = 0  # связь
#         self.D = 0  # удалено

# class HashTable:
#     def __init__(self, size=20, B=0):
#         self.size = size
#         self.B = B
#         self.table = [HashEntry() for _ in range(size)]

#     # Преобразование первых двух букв ключа в число V
#     def key_to_number(self, key):
#         alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
#         key = key.upper()
#         first = alphabet.find(key[0]) if key[0] in alphabet else 0
#         second = alphabet.find(key[1]) if len(key) > 1 and key[1] in alphabet else 0
#         V = first * len(alphabet) + second
#         return V

#     # Хеш-функция
#     def hash_func(self, key):
#         V = self.key_to_number(key)
#         h = (V % self.size) + self.B
#         return h

#     # Добавление с квадратичным пробингом
#     def insert(self, key, value):
#         h = self.hash_func(key)
#         i = 0
#         if self.search(key) is not None:
#             print("Ключ уже существует")
#             return
#         while True:
#             idx = (h + i**2) % self.size
#             entry = self.table[idx]
#             if entry.U == 0 or entry.D == 1:
#                 self.table[idx] = HashEntry(key, value)
#                 self.table[idx].U = 1
#                 if i > 0:
#                     self.table[idx].C = 1  # коллизия
#                 break
#             else:
#                 i += 1
#                 if i >= self.size:
#                     raise Exception("Таблица заполнена, нет места для нового ключа")
                
#         V = self.key_to_number(key)
#         print(f"Key={key}, V={V}, h(V)={h}")

#     # Поиск
#     def search(self, key):
#         h = self.hash_func(key)
#         i = 0
#         while i < self.size:
#             idx = (h + i**2) % self.size
#             entry = self.table[idx]
#             if entry.U == 0:
#                 return None
#             if entry.U == 1 and entry.key == key and entry.D == 0:
#                 return entry.value
#             i += 1
#         return None
    
#     def update(self, key, new_value):
#         h = self.hash_func(key)
#         i = 0

#         while i < self.size:
#             idx = (h + i**2) % self.size
#             entry = self.table[idx]

#             if entry.U == 0:
#                 return False

#             if entry.key == key and entry.D == 0:
#                 entry.value = new_value
#                 return True

#             i += 1

#         return False

#     # Удаление
#     def delete(self, key):
#         h = self.hash_func(key)
#         i = 0
#         while i < self.size:
#             idx = (h + i**2) % self.size
#             entry = self.table[idx]
#             if entry.U == 0:
#                 return False
#             if entry.key == key and entry.D == 0:
#                 self.table[idx].D = 1
#                 self.table[idx].U = 0
#                 return True
#             i += 1
#         return False

#     # Вывод таблицы
#     def display(self):
#         print("-" * 80)
#         print(f"{'Index':<6}{'Key':<15}{'Value':<25}{'U':<3}{'C':<3}{'D':<3}")
#         print("-" * 80)

#         for i, entry in enumerate(self.table):
#             print(f"{i:<6}{str(entry.key):<15}{str(entry.value):<25}"
#                 f"{entry.U:<3}{entry.C:<3}{entry.D:<3}")
            
#     def load_factor(self):
#         used = sum(1 for entry in self.table if entry.U == 1)
#         return used / self.size

# # ------------------- Тестирование -------------------
# ht = HashTable()

# # Добавляем несколько ключей
# ht.insert("Азимов", "Термин из биологии")
# ht.insert("Бобков", "Ещё один термин")
# ht.insert("Вяткин", "Тестовая запись")

# # Вывод таблицы
# ht.display()

# # Поиск
# print("Поиск 'Азимов':", ht.search("Азимов"))

# # Удаление
# ht.delete("Бобков")
# ht.display()
# print("Коэффициент заполнения:", ht.load_factor())