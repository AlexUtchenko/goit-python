class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
             self.data[record.name.value].adds(record.phones)

class Record:
    def __init__(self, name, phones=None):
        self.name = name
        if phones is None:
            self.phones = []
        else:
            self.phones = phones

    def add(self, number):
        self.phones.append(number)

    def adds(self, numbers):
        self.phones.extend(numbers)

    def remove(self, number):
        pos = 0
        for index, value in enumerate(self.phones):
            if str(value) == str(number):
                pos = index
                break
        self.phones.pop(pos)

    def edit(self, old_number, new_number):
        pos = 0
        for index, value in enumerate(self.phones):
            if str(value) == str(old_number):
                pos = index
                break
        self.phones[pos] = new_number

class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
        def __init__(self, value):
            super().__init__(value)

        def __repr__(self):
            return self.value

