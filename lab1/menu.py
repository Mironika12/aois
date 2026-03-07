from my_math.int_fixed import *
from my_math.float_ieee import *
from my_math.bcd import decimal_to_bcd, bcd_to_decimal, add_bcd

def print_codes(n):
    print(f"Число: {n}")

    if isinstance(n, float) and not n.is_integer():
        ieee = float_to_ieee754(n)
        print("IEEE              :", "".join(ieee.astype(str)))
        return

    n_int = int(n)

    dc = direct_code(n_int)
    oc = ones_complement(n_int)
    tc = twos_complement(n_int)

    print("Прямой код        :", "".join(dc.astype(str)))
    print("Обратный код      :", "".join(oc.astype(str)))
    print("Дополнительный код:", "".join(tc.astype(str)))

    ieee = float_to_ieee754(float(n_int))
    print("IEEE              :", "".join(ieee.astype(str)))


def add_numbers():
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))

    a_tc = twos_complement(a)
    b_tc = twos_complement(b)

    result = add_twos_complement(a_tc, b_tc)

    print("A (two's complement):", "".join(a_tc.astype(str)))
    print("B (two's complement):", "".join(b_tc.astype(str)))

    print("Результат (binary):", "".join(result.astype(str)))
    print("Результат (decimal):", twos_to_decimal(result))


def subtract_numbers():
    a = int(input("Введите уменьшаемое: "))
    b = int(input("Введите вычитаемое: "))

    a_tc = twos_complement(a)
    b_tc = twos_complement(-b)

    result = subtract_twos_complement(a_tc, b_tc)

    print("A (two's complement):", "".join(a_tc.astype(str)))
    print("B (two's complement):", "".join(b_tc.astype(str)))

    print("Результат (binary):", "".join(result.astype(str)))
    print("Результат (decimal):", twos_to_decimal(result))


def multiply_numbers():
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))

    a_bin = direct_code(a)
    b_bin = direct_code(b)

    result = multiply_direct(a_bin, b_bin)

    print("Результат (binary):", "".join(result.astype(str)))
    print("Результат (decimal):", a * b)


def divide_numbers():
    a = int(input("Введите делимое: "))
    b = int(input("Введите делитель: "))

    a_bin = direct_code(a)
    b_bin = direct_code(b)

    result = divide_direct(a_bin, b_bin)

    print("Результат (binary):", "".join(result.astype(str)))

    decimal_result = fixed_to_decimal(result)

    print("Результат (decimal):", round(decimal_result, 5))


def add_ieee_numbers():
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    a_ieee = float_to_ieee754(a)
    b_ieee = float_to_ieee754(b)

    result_ieee = ieee_add(a_ieee, b_ieee)

    print("IEEE:", "".join(result_ieee.astype(str)))

    result_decimal = ieee754_to_decimal(result_ieee)

    print("Decimal:", result_decimal)


def subtract_ieee_numbers():
    a = float(input("Введите уменьшаемое: "))
    b = float(input("Введите вычитаемое: "))

    a_ieee = float_to_ieee754(a)
    b_ieee = float_to_ieee754(b)

    result_ieee = ieee_sub(a_ieee, b_ieee)

    print("IEEE:", "".join(result_ieee.astype(str)))

    result_decimal = ieee754_to_decimal(result_ieee)

    print("Decimal:", result_decimal)


def multiply_ieee_numbers():
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    a_ieee = float_to_ieee754(a)
    b_ieee = float_to_ieee754(b)

    result_ieee = ieee_mul(a_ieee, b_ieee)

    print("IEEE:", "".join(result_ieee.astype(str)))

    result_decimal = ieee754_to_decimal(result_ieee)

    print("Decimal:", result_decimal)


def divide_ieee_numbers():
    a = float(input("Введите делимое: "))
    b = float(input("Введите делитель: "))

    a_ieee = float_to_ieee754(a)
    b_ieee = float_to_ieee754(b)

    result_ieee = ieee_div(a_ieee, b_ieee)

    print("IEEE:", "".join(result_ieee.astype(str)))

    result_decimal = ieee754_to_decimal(result_ieee)

    print("Decimal:", result_decimal)


def add_bcd_numbers():
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))

    a_bcd = decimal_to_bcd(a)
    b_bcd = decimal_to_bcd(b)

    res = add_bcd(a_bcd, b_bcd)

    print("BCD:", "".join(res.astype(str)))
    print("Decimal:", bcd_to_decimal(res))


def main_menu():
    while True:
        print("\nВыберите операцию:")
        print(" 1) Перевод числа в коды (IEEE)")
        print(" 2) Сложение в дополнительном коде (two's complement)")
        print(" 3) Вычитание в дополнительном коде")
        print(" 4) Умножение в прямом коде")
        print(" 5) Деление в прямом коде (fixed-point)")
        print(" 6) Сложение с плавающей точкой (IEEE-754)")
        print(" 7) Вычитание с плавающей точкой (IEEE-754)")
        print(" 8) Умножение с плавающей точкой (IEEE-754)")
        print(" 9) Деление с плавающей точкой (IEEE-754)")
        print("10) Сложение в BCD (8421)")
        print(" 0) Выход")
        choice = input("Выбор: ").strip()

        try:
            if choice == "0":
                print("Выход.")
                break

            if choice == "1":
                n = float(input("Введите число для перевода в коды: "))
                print_codes(n)

            elif choice == "2":
                add_numbers()

            elif choice == "3":
                subtract_numbers()

            elif choice == "4":
                multiply_numbers()

            elif choice == "5":
                divide_numbers()

            elif choice == "6":
                add_ieee_numbers()

            elif choice == "7":
                subtract_ieee_numbers()

            elif choice == "8":
                multiply_ieee_numbers()

            elif choice == "9":
                divide_ieee_numbers()

            elif choice == "10":
                add_bcd_numbers()

            else:
                print("Неверный выбор. Введите номер операции.")

        except ZeroDivisionError as e:
            print("Ошибка: деление на ноль.")
        except ValueError as e:
            print("Ошибка значения:", e)
        except Exception as e:
            print("Ошибка:", e)
