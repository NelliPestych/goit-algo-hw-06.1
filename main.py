from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        # Перевіряємо, що номер містить рівно 10 цифр
        if len(value) != 10 or not value.isascii() or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Додаємо новий телефон до списку
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Знаходимо та видаляємо телефон
        found_phone = self.find_phone(phone)

        if found_phone:
            self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        # Перевіряємо, чи існує старий номер
        found_phone = self.find_phone(old_phone)

        if found_phone is None:
            raise ValueError("Phone number not found.")

        # Перевіряємо новий номер і замінюємо старий
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(found_phone)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone):
        # Шукаємо телефон за його значенням
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Зберігаємо запис, використовуючи ім'я як ключ
        self.data[record.name.value] = record

    def find(self, name):
        # Повертаємо запис або None, якщо його немає
        return self.data.get(name)

    def delete(self, name):
        # Видаляємо запис, якщо він існує
        self.data.pop(name, None)

    def __str__(self):
        # Формуємо рядок з усіх контактів
        return "\n".join(str(record) for record in self.data.values())


# Перевірка роботи програми
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    # Видалення телефону John
    john.remove_phone("5555555555")
    print(john)

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення оновленої адресної книги
    print(book)
