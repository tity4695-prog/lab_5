"""Лабораторная работа №5: сравнение алгоритмов сортировки.

Запуск: python sravnenie_sortirovok.py
Требуется только Python 3. Никакие сторонние библиотеки не нужны.
Результат: файл rezultaty_sortirovki.csv в той же папке.
"""

import csv
import random
import time
from pathlib import Path


def bubble_sort(items):
    a = list(items)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(items):
    a = list(items)
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        while j >= 0 and a[j] > current:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
    return a


def merge_sort(items):
    a = list(items)
    if len(a) <= 1:
        return a
    middle = len(a) // 2
    left = merge_sort(a[:middle])
    right = merge_sort(a[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def make_data(data_type, size, rng):
    if data_type == "int":
        return [rng.randint(-10000, 10000) for _ in range(size)]
    if data_type == "float":
        return [rng.uniform(-10000, 10000) for _ in range(size)]
    # Строки одинаковой длины, чтобы сравнение было наглядным.
    return [f"word{rng.randint(0, 99999):05d}" for _ in range(size)]


def measure(sort_function, data, repeats):
    durations = []
    expected = sorted(data)
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_function(data)
        durations.append(time.perf_counter() - start)
        if result != expected:
            raise RuntimeError(f"Ошибка: {sort_function.__name__} сортирует неверно")
    return sum(durations) / len(durations)


def main():
    rng = random.Random(42)
    sizes = [100, 250, 500, 1000, 1500]
    repeats = 3
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
    }
    data_types = ["int", "float", "string"]
    rows = []

    print("Сравнение алгоритмов сортировки")
    print("Время указано в секундах; для каждого теста берётся среднее из", repeats, "запусков.\n")

    for data_type in data_types:
        print(f"Тип данных: {data_type}")
        print(f"{'Размер':>8} | {'Bubble Sort':>13} | {'Insertion Sort':>15} | {'Merge Sort':>12}")
        print("-" * 59)
        for size in sizes:
            data = make_data(data_type, size, rng)
            timings = {}
            for name, function in algorithms.items():
                timings[name] = measure(function, data, repeats)
                rows.append({
                    "data_type": data_type,
                    "list_size": size,
                    "algorithm": name,
                    "average_time_seconds": f"{timings[name]:.8f}",
                    "repetitions": repeats,
                })
            print(
                f"{size:8d} | {timings['Bubble Sort']:13.8f} | "
                f"{timings['Insertion Sort']:15.8f} | {timings['Merge Sort']:12.8f}"
            )
        print()

    output_file = Path(__file__).resolve().with_name("rezultaty_sortirovki.csv")
    with output_file.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["data_type", "list_size", "algorithm", "average_time_seconds", "repetitions"],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Готово! Результаты сохранены в файл:\n{output_file}")
    input("\nНажмите Enter, чтобы закрыть программу...")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nПроизошла ошибка: {error}")
        input("Нажмите Enter, чтобы закрыть программу...")
