import pickle
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Некоректний номер телефону")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Некоректний формат дня народження")
        self._value = new_value

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, 
                                     datetime.strptime(self.birthday.value, '%Y-%m-%d').month,
                                     datetime.strptime(self.birthday.value, '%Y-%m-%d').day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, 
                                         datetime.strptime(self.birthday.value, '%Y-%m-%d').month,
                                         datetime.strptime(self.birthday.value, '%Y-%m-%d').day)
            days_left = (next_birthday - today).days
            return days_left
        return None

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def save_to_disk(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.records, file)

    def load_from_disk(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.records = pickle.load(file)
        except FileNotFoundError:
            pass

    def search_contacts(self, query):
        results = []
        for record in self.records:
            if (query.lower() in record.name.value.lower() or
                query in record.phone.value or
                (record.birthday and query in record.birthday.value)):
                results.append(record)
        return results

    def iterator(self, N):
        for i in range(0, len(self.records), N):
            yield self.records[i:i + N]

# Приклад використання
address_book = AddressBook()
record1 = Record("John Doe", "1234567890", "1990-01-01")
record2 = Record("Jane Doe", "9876543210", "1995-05-15")
address_book.add_record(record1)
address_book.add_record(record2)

# Збереження на диск
address_book.save_to_disk('address_book.pkl')

# Завантаження з диска
address_book.load_from_disk('address_book.pkl')

# Пошук за ім'ям, номером телефону або днем народження
search_results = address_book.search_contacts('John')
print("Search results:", search_results)

# Виведення записів
for chunk in address_book.iterator(1):
    for record in chunk:
        print(f"Name: {record.name.value}, Phone: {record.phone.value}, Birthday: {record.birthday.value}, "
              f"Days to Birthday: {record.days_to_birthday()}")
