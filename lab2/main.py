from logic.table_build import build_table, print_table, read_expr
from logic.table_analysis import (
    build_sdnf,
    build_sknf,
    numeric_sdnf,
    numeric_sknf,
    index_form,
    print_terms
)
from logic.post_zhegalkin import (
    is_T0,
    is_T1,
    is_self_dual,
    is_monotonic,
    is_linear,
    zhegalkin_polynomial
)
from logic.dummy_vars import (
    find_dummy_vars,
    boolean_derivative,
    mixed_derivative
)
from logic.minimization_calc_method import (
    minimize,
    minimize_table_method,
    merge_stages,
    remove_redundant
)
from logic.minimization_carno import (
    minimize_kmap,
    print_kmap
)
from printer import (  
    print_merge_stages,
    print_coverage_table,
)


def analyze(expr: str):
    print("=" * 60)
    print(f"Функция: {expr}")
    print("=" * 60)

    # ---------------- ТАБЛИЦА ----------------
    table = build_table(expr)

    print("\nТаблица истинности:")
    print_table(table)

    # ---------------- ФОРМЫ ----------------
    print("\nСДНФ:")
    sdnf = build_sdnf(table)
    print_terms(sdnf, True)

    print("\nСКНФ:")
    sknf = build_sknf(table)
    print_terms(sknf, False)

    # ---------------- ЧИСЛОВЫЕ ----------------
    print("\nЧисловые формы:")
    print(f"СДНФ: {numeric_sdnf(table)}")
    print(f"СКНФ: {numeric_sknf(table)}")

    print("\nИндексная форма:")
    print(index_form(table))

    print("\nМинимизация (расчетный метод):")

    print("\nСДНФ:")
    stages = merge_stages(sdnf)
    print_merge_stages(stages, True)

    min_sdnf = remove_redundant(stages[-1], sdnf)

    print("\nПосле удаления лишних:")
    print_terms(min_sdnf, True)

    print("\nСКНФ:")
    stages = merge_stages(sknf)
    print_merge_stages(stages, False)

    min_sknf = remove_redundant(stages[-1], sknf)

    print("\nПосле удаления лишних:")
    print_terms(min_sknf, False)

    print("\nМинимизация (расчетно-табличный метод):")

    print("\nСДНФ:")

    stages = merge_stages(sdnf)
    prime_terms = stages[-1]

    print("\nТаблица покрытия:")
    print_coverage_table(prime_terms, sdnf)

    tab_sdnf = minimize_table_method(sdnf)

    print("\nРезультат:")
    print_terms(tab_sdnf, True)

    print("\nСКНФ:")

    stages = merge_stages(sknf)
    prime_terms = stages[-1]

    print("\nТаблица покрытия:")
    print_coverage_table(prime_terms, sknf)

    tab_sknf = minimize_table_method(sknf)

    print("\nРезультат:")
    print_terms(tab_sknf, False)

    print("\nМинимизация (карта Карно):")

    print("\nКарта Карно:")
    print_kmap(table)

    print("\nСДНФ:")
    kmap_sdnf = minimize_kmap(table, True)
    print_terms(kmap_sdnf, True)

    print("\nСКНФ:")
    kmap_sknf = minimize_kmap(table, False)
    print_terms(kmap_sknf, False)

    print("\nКлассы Поста:")
    print(f"T0: {is_T0(table)}")
    print(f"T1: {is_T1(table)}")
    print(f"S: {is_self_dual(table)}")
    print(f"M: {is_monotonic(table)}")
    print(f"L: {is_linear(table)}")

    
    print("\nПолином Жегалкина:")
    print(zhegalkin_polynomial(table))

    
    print("\nФиктивные переменные:")
    dummy = find_dummy_vars(table)
    print(dummy if dummy else "нет")

    
    print("\nБулевы производные:")

    vars = [k for k in table[0].keys() if k != 'f']

    for var in vars:
        derivative = boolean_derivative(table, var)
        print(f"∂f/∂{var}: {derivative}")

    print("\nСмешанные производные:")

    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            v1 = vars[i]
            v2 = vars[j]

            derivative = mixed_derivative(table, [v1, v2])
            print(f"∂²f/∂{v1}∂{v2}: {derivative}")

    print("\n" + "=" * 60 + "\n")





def main():
    filepath = input("Введите имя файла с выражениями: ").strip()

    try:
        expressions = read_expr(filepath)
    except FileNotFoundError:
        print("Файл не найден")
        return
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return

    if not expressions:
        print("Файл пуст")
        return

    for expr in expressions:
        analyze(expr)


if __name__ == "__main__":
    main()