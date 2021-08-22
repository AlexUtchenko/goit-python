import datetime, re

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
             self.data[record.name.value].adds(record.phones)

    def edit_record(self, old_record, new_record):
        if old_record.name.value not in self.data:
            return
        self.data[old_record.name.value].edit(old_record.phones[0], new_record.phones[0])

    def delete(self, record):
        if record.name.value in self.data:
            self.data.pop(record.name.value)

    def __str__(self):
        return "\n".join([str(record) for record in self.data.values()])

    def iterator(self, item_number):
        counter = 0
        result = ""
        for name, record in self.data.items():
            result += str(record) + "\n"
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ""
            yield result

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = name
        self.birthday = birthday
        if phones is None:
            self.phones = []
        else:
            self.phones = phones

    def __repr__(self):
        result = f"{str(self.name)}\n{20 *'-'}"
        for index, phone in enumerate(self.phones, start=1):
            result += f"\n{index} {phone}"
        return result

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

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.date.today()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year + 1) - now).days


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
    PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")

        def __init__(self, value):
            super().__init__(value)
            self.country_code = ""
            self.operator_code = ""
            self.phone_number = ""

        def __repr__(self):
            return self.value

        @Field.value.setter
        def value(self, value: str):
            value = value.replace(" ", "")
            search = re.search(self.PHONE_REGEX, value)
            try:
                country, operator, phone = search.group(1, 2, 3)
            except AttributeError:
                raise IncorrectInput(f"No phone number found in {value}")

            if operator is None:
                raise IncorrectInput(f"Operator code not found in {value}")

            self.country_code = country if country is not None else "38"
            self.operator_code = operator
            self.phone_number = phone
            self.__value = f"+{self.country_code}({self.operator_code}){self.phone_number}"


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self.__value = datetime.datetime.strptime(value, '%d%m%Y').date()





