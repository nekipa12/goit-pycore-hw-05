import re
from typing import Callable


def generator_numbers(text: str):
    """Генератор, який по черзі повертає всі дійсні числа з тексту."""
    if not isinstance(text, str):
        raise TypeError("Текст має бути рядком.")

    # числа відокремлені пробілами з обох боків,
    # тому розбиваємо текст на слова і перевіряємо кожне
    for word in text.split():
        # дійсне число: цифри, крапка, цифри (наприклад, 1000.01)
        if re.fullmatch(r"\d+\.\d+", word):
            yield float(word)


def sum_profit(text: str, func: Callable) -> float:
    """Рахує загальний дохід: суму чисел, які func знаходить у тексті."""
    total = sum(func(text))
    # округлюємо до копійок, щоб прибрати похибку float
    # (наприклад, 0.1 + 0.2 дає 0.30000000000000004)
    return round(total, 2)


if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими "
        "надходженнями 27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
