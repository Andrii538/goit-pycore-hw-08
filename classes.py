from datetime import datetime, timedelta, date
from collections import UserDict
import logging
import pickle
import os


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)
        if  not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError


class Birthday(Field):
    def __init__(self, value: str):
        if not self.isvalid(value):
            raise ValueError
        super().__init__(value)

    @staticmethod
    def isvalid(value: str) -> bool:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def string_to_date(value: str) -> date:
        return datetime.strptime(value, "%d.%m.%Y").date()

    def date_to_string(date_obj: date) -> str:
        return date_obj.strftime("%d.%m.%Y")

    def find_next_weekday(start_date: date, weekday: int) -> date:
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(birthday: date) -> date:
        if birthday.weekday() >= 5:
            return Birthday.find_next_weekday(birthday, 0)
        return birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, phone, new_phone):
        if self.find_phone(phone):
            self.add_phone(new_phone)
            self.remove_phone(phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {phones}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        self.data.pop(name)

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = date.today()
        days = 7
        for name, record in self.data.items():
            if not record.birthday:
                continue
            real_birthday_date = Birthday.string_to_date(record.birthday.value)
            birthday_this_year = real_birthday_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            days_until = (birthday_this_year - today).days
            if 0 <= days_until <= days:
                congratulation_date = Birthday.adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({"name": name, "birthday": Birthday.date_to_string(congratulation_date)})
        return upcoming_birthdays
    
    def __str__(self):
        return '\n'.join(f'{self.data[item]}' for item in self.data)
    
    @classmethod
    def load_or_create(cls, filename = 'addressbook.pkl'):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                logging.info('Contact list has been restored')
                return pickle.load(f)
        logging.info('Contact list not found. New contact list has been created.')
        return AddressBook()
        
    def save_to_file(self, filename = 'addressbook.pkl'):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        
