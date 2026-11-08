# goit-pycore-hw-05

Домашнє завдання до теми 8: елементи функціонального програмування та вбудовані модулі Python.

## Структура

- `task1/fibonacci.py` — `caching_fibonacci()`: числа Фібоначчі з кешем у замиканні
- `task2/profit.py` — `generator_numbers(text)` і `sum_profit(text, func)`: генератор дійсних чисел з тексту та загальний дохід
- `task3/main.py` — аналіз лог-файлу: кількість записів за рівнями та деталі обраного рівня, приклад логу в `task3/logfile.log`
- `task4/bot.py` — консольний бот-помічник з обробкою помилок через декоратор `input_error`

## Запуск

Сторонні бібліотеки не потрібні, достатньо Python 3.

```
python task1/fibonacci.py
python task2/profit.py
python task3/main.py task3/logfile.log
python task3/main.py task3/logfile.log error
python task4/bot.py
```
