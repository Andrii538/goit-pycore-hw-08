from classes import *


def input_error(error_message):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return error_message
            except KeyError:
                return 'Name is not in contact list'
            except AttributeError:
                return 'Info not found'
            except IndexError:
                return error_message
        return inner
    return decorator


@input_error('Invalid command.')
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error("Enter the contact's name and phone number.")
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error("Enter the contact's name, phone and new phone number.")
def change_contact(args, book: AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(phone, new_phone)
    return "Contact updated."
    

@input_error("Enter the contact's name")
def contact_delete(args, book: AddressBook):
    name, = args
    book.delete(name)
    return f'{name} has been removed from your contact list.'
    

def show_all(book: AddressBook):
    if not book:
        return "Records not found"
    return book


@input_error("Enter the contact's name")
def show_phone(args, book: AddressBook):
    name, = args
    record = book.find(name)
    return ', '.join(f'{phone.value}' for phone in record.phones)


@input_error("Enter the contact's name and birthday date in form DD.MM.YYYY")
def add_birthday(args, book: AddressBook):
    name, date, *_ = args
    record = book.find(name)
    record.add_birthday(date)
    return f'Birthday for {name} was added.'


@input_error("Enter the contact's name")
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    return record.birthday.value


def birthdays(book: AddressBook):
    birthday = book.get_upcoming_birthdays()
    if not birthday:
        return "No birthdays found"
    return '\n'.join(f'{item["name"]} -- {item["birthday"]}' for item in  birthday)
    