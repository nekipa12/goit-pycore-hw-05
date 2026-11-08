import sys
from collections import Counter
from datetime import datetime

# рівні логування, які вважаються коректними
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def parse_log_line(line: str) -> dict:
    """Розбирає рядок логу на дату, час, рівень і повідомлення."""
    # ділимо лише тричі, бо саме повідомлення теж містить пробіли
    parts = line.split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError("очікуються дата, час, рівень і повідомлення")

    date, time, level, message = parts

    # перевіряємо формат дати й часу, наприклад 2024-01-22 08:30:01
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("неправильний формат дати або часу")

    level = level.upper()
    if level not in LOG_LEVELS:
        raise ValueError(f"невідомий рівень логування {level}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    """Завантажує записи логу з файлу у список словників."""
    logs = []
    # utf-8-sig читає і звичайний UTF-8, і файли з BOM
    # (такі іноді зберігає Блокнот у Windows)
    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            # порожні рядки пропускаємо
            if not line:
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                # некоректний рядок не зупиняє аналіз, лише попереджаємо
                print(f"Рядок {line_number} пропущено: {error}.")
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Повертає лише записи вказаного рівня логування."""
    level = level.upper()
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: list) -> dict:
    """Підраховує кількість записів для кожного рівня логування."""
    counter = Counter(log["level"] for log in logs)
    # most_common сортує рівні від найчастішого до найрідшого
    return dict(counter.most_common())


def display_log_counts(counts: dict) -> None:
    """Виводить таблицю з кількістю записів для кожного рівня."""
    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def display_logs(logs: list, level: str) -> None:
    """Виводить дату, час і повідомлення записів обраного рівня."""
    print(f"\nДеталі логів для рівня '{level}':")
    if not logs:
        print("Записів такого рівня у файлі немає.")
        return
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    # очікуємо: python main.py <шлях до файлу> [рівень логування]
    if len(sys.argv) not in (2, 3):
        print("Використання: python main.py <шлях до файлу логів> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]

    # рівень перевіряємо одразу, щоб не читати файл даремно
    level = None
    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        if level not in LOG_LEVELS:
            print(f"Невідомий рівень логування: {sys.argv[2]}")
            print(f"Доступні рівні: {', '.join(LOG_LEVELS)}")
            sys.exit(1)

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)
    except IsADirectoryError:
        print(f"{file_path} є директорією, а не файлом.")
        sys.exit(1)
    except PermissionError:
        print(f"Немає доступу до файлу {file_path}.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Файл {file_path} не є текстовим файлом у кодуванні UTF-8.")
        sys.exit(1)
    except OSError as error:
        print(f"Не вдалося прочитати файл {file_path}: {error}")
        sys.exit(1)

    if not logs:
        print(f"У файлі {file_path} немає жодного коректного запису логу.")
        sys.exit(1)

    display_log_counts(count_logs_by_level(logs))

    if level:
        display_logs(filter_logs_by_level(logs, level), level)


if __name__ == "__main__":
    main()
