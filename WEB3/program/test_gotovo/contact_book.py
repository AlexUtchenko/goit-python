from collections import UserDict
import pickle
import re
from datetime import *


class AddressBook(UserDict):
    FOLDER = "contact_data/"

    def add_record(self, name, record):
        self.data[name] = record

    def iterator(self, n=None):
        # returns a view for 'n' records in one iteration
        outer_count = 1
        inner_count = 1
        n_records = []
        records = (i for i in self.data.values())
        for one_record in records:
            n_records.append(one_record)
            if inner_count == n or outer_count == len(self.data):
                yield n_records
                n_records = []
                inner_count = 0
            inner_count += 1
            outer_count += 1

    def save_dumped_data(self):
        with open('contact_list.txt', 'wb') as file:
            pickle.dump(self.data, file)

    def read_dumped_data(self):
        with open('contact_list.txt', 'rb') as file:
            self.data = pickle.load(file)
            return self


class Record:
    def __init__(self, name, email=None, adress=None, birthday=None):
        self.name = name
        self.adress = adress
        self.email = email
        self.phones = []
        self.birthday = birthday

    def __add__(self, phone, email=None):
        self.phones.append(phone)
        return self

    def __delete__(self, phone):
        self.phones.remove(phone)
        return self

    def change_phone(self, phone, new_phone):
        self.phones[self.phones.index(phone)] = new_phone


class Field:

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Adress(Field):
    def __init__(self, adress):
        self.value = adress


class Phone(Field):
    def __init__(self, phone):
        self.value = phone


class Email(Field):
    def __init__(self, email):
        self.value = email


class Birthday(Field):

    def __init__(self, date_birth):
        self.value = date_birth