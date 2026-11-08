from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Створює функцію fibonacci, яка зберігає обчислені значення в кеші."""
    # кеш живе в замиканні: fibonacci пам'ятає його між викликами
    cache = {}

    def fibonacci(n: int) -> int:
        """Повертає n-е число Фібоначчі, використовуючи кеш."""
        if not isinstance(n, int):
            raise TypeError("Номер числа Фібоначчі має бути цілим числом.")

        # базові випадки рекурсії
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # якщо значення вже обчислене, просто беремо його з кешу
        if n in cache:
            return cache[n]

        # інакше рахуємо рекурсивно і запам'ятовуємо результат
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    # отримуємо функцію fibonacci
    fib = caching_fibonacci()

    # використовуємо її для обчислення чисел Фібоначчі
    print(fib(10))  # виведе 55
    print(fib(15))  # виведе 610
