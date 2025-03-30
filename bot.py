"""
Expand bot command support and integrate birthday logic. Extends bot commands to 
handle phone and birthday operations.
"""

from functools import wraps
from addressbook import AddressBook, Record, Phone  # Імпортуємо необхідні нам класи з адресної книги


# Декоратор для обробки помилок.
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:                     # Передаємо унікальне повідомлення користувачу в залежності від типу помилки
            return str(e)
        except KeyError:
            return "No such contact in your list."
        except Exception as e:
            return f"Error: {e}"
    return inner


# Основний функціонал бота
def parse_input(user_input):
    if not user_input.strip(): return "", []
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone.")
    name, phone = args[0], args[1]                   # Вказуємо обов'язкові поля для створення контакту
    birthday = args[2] if len(args) >= 3 else None   # День народження можна вказати одразу, але це поле не є обов'язковим для користувача
    validated_phone = Phone(phone)                   # Одразу валідуємо номер, щоб контакт не був створений, якщо при створенні телефон не дорівнював 10 символам
    record = book.find(name)
    message = "Contact updated."
    if not isinstance(record, Record):
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(validated_phone.value)
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Please provide name, old phone and new phone.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return record.edit_phone(old_phone, new_phone)
    return f"No contact with the name {name} found."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide name.")
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"
    return f"No contact with the name {name} found."


@input_error
def show_all(book: AddressBook):
    if not book: 
        return "No contacts in your list."
    return '\n'.join([f"{name}: {record}" for name, record in book.data.items()])


@input_error
def delete_phone(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide name and phone to delete.")
    name, phone = args[0], args[1]
    record = book.find(name)
    if isinstance(record, Record):
        return record.remove_phone(phone)
    return f"No contact with the name {name} found."


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide the name of the contact to delete.")
    name = args[0]
    return book.delete(name)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide name and birthday. Use DD.MM.YYYY")
    name, birthday, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    return f"No contact with the name {name} found."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide name.")
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record) and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"No birthday found for {name}."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming])


@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if not command: continue
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "delete-phone":
            print(delete_phone(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()