from functools import wraps


def input_error(func):
    """Декоратор: перетворює помилки введення на зрозумілі відповіді."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            # ValueError: для name, phone = args потрібно рівно 2 аргументи
            # IndexError: ім'я не передали, тому args[0] не існує
            return "Enter the argument for the command"
        except KeyError:
            # контакту з таким ім'ям немає у словнику
            return "Contact not found."

    return inner


def parse_input(user_input: str) -> tuple:
    """Розбиває введений рядок на команду та список аргументів."""
    parts = user_input.split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args: list, contacts: dict) -> str:
    """Додає новий контакт: add [ім'я] [телефон]."""
    name, phone = args
    # щоб 'john' і 'John' були одним контактом
    name = name.capitalize()
    if name in contacts:
        return "Contact already exists. Use 'change' to update it."
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict) -> str:
    """Змінює номер телефону існуючого контакту: change [ім'я] [телефон]."""
    name, phone = args
    name = name.capitalize()
    if name not in contacts:
        # змінити можна лише контакт, який уже є
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list, contacts: dict) -> str:
    """Показує номер телефону за ім'ям: phone [ім'я]."""
    name = args[0].capitalize()
    return contacts[name]


@input_error
def show_all(contacts: dict) -> str:
    """Повертає всі збережені контакти."""
    if not contacts:
        return "No contacts saved yet."
    lines = []
    for name, phone in contacts.items():
        lines.append(f"{name}: {phone}")
    return "\n".join(lines)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C або Ctrl+D: завершуємо роботу без traceback
        print("\nGood bye!")
