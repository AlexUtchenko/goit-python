from . import contact_book
import inspect
import pathlib
import signal
from . import sort_file
from . import Noter
import pathlib
import re
import sys
from pathlib import Path
import pickle
import difflib
from datetime import *
import logging  # Логгирование
from logging import FileHandler, Formatter  # Логгирование

logger = logging.getLogger(__name__)  # Логгирование
logger.setLevel(logging.DEBUG)  # Логгирование
handler = logging.FileHandler("MyLogFile.txt")  # Логгирование
handler.setFormatter(
    Formatter(fmt='[%(asctime)s]: %(message)s'))  # Логгирование
logger.addHandler(handler)  # Логгирование


# in USE add contact
def com_add(name, phone, email=None, adress=None, birthday=None):
    import logging  # Логгирование


from logging import FileHandler, Formatter  # Логгирование

logger = logging.getLogger(__name__)  # Логгирование
logger.setLevel(logging.DEBUG)  # Логгирование
handler = logging.FileHandler("MyLogFile.txt")  # Логгирование
handler.setFormatter(Formatter(fmt='[%(asctime)s]: %(message)s'))  # Логгирование
logger.addHandler(handler)  # Логгирование


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f'Command {e} not found!!!'
        except ValueError as e:
            return e
        except IndexError as e:
            return f'Command not full!!'

    return inner


# in USE add contact
def com_add(name, phone, email=None, adress=None, birthday=None):
    if name.value in [key.value for key in list(contact_list.keys())]:
        raise ValueError(f'The new contact cannot be saved because the name "{name.value}" already exists. '
                         f'Please enter a different name.\n')

    record = contact_book.Record(name, email, adress, birthday) + phone
    contact_list.add_record(name, record)
    return f'New contact is saved: name "{name.value}", phone "{phone.value}",' \
           f'email "{email if email else "-"}",' \
           f'adress "{adress if adress else "-"}",' \
           f' date of birth "{birthday if birthday else "-"}".\n'


# in USE change number
def com_change(name, phone, new_phone):
    print(new_phone)
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact by name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            for ph in rec.phones:
                if ph.value == phone:
                    rec.change_phone(ph, new_phone)
                    return f'Saved a new phone number "{new_phone.value}" for a contact with the name "{name}".\n'
        else:
            raise ValueError(
                f'The contact "{name}" does not have a phone number {phone}.\n')


# in USE add number
def com_join(name, phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            record = rec + phone
            contact_list.add_record(nam, record)
    print(f'A new phone number "{phone.value}" has been added for the contact with the name "{name}".\n')


# in USE delete number
def com_delete(name, phone):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact by name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            for ph in rec.phones:
                if ph.value == phone:
                    rec.phones.remove(ph)
                    print(f'Delete phone number "{ph.value}" for a contact with the name "{name}".\n')

                # in USE show


# in USE show
def com_search(pattern):
    result = ''
    for nam, rec in contact_list.items():
        phone_list = [phone.value for phone in rec.phones]
        for p in phone_list:
            if p.find(pattern) != (-1) or nam.value.find(pattern) != (-1):
                result = f'name: {nam.value}, phone: {" ".join([phone.value for phone in rec.phones])}, ' \
                         f' email {rec.email if rec.email else "-"} ' \
                         f'adress {rec.adress if rec.adress else "-"} ' \
                         f'birthday {rec.birthday if rec.birthday else "-"}\n'
    if not result:
        raise ValueError(f'No matches.\n')
    return result


# in USE com_delete_contact
def com_delete_contact(name):
    result = ''
    for nam, rec in contact_list.items():
        if nam.value == name:
            contact_list.data.pop(nam)
            contact_list.save_dumped_data()
    if not result:
        raise ValueError(f'No matches.\n')
    return result


# in USE days to birthday
def days_to_birthday(days):
    for nam, rec in contact_list.items():
        if rec.birthday:
            st_birthday = str(rec.birthday).split('-')
            birthday = []
            for d in st_birthday:
                birthday.append(int(d))
            now_ywd = datetime.now().timetuple()
            now_date = date(now_ywd[0], now_ywd[1], now_ywd[2])
            (birthday[0]) = now_ywd[0]
            days_to_birthday = date((birthday[0]), (birthday[1]), (birthday[2]))
            delta = (days_to_birthday - now_date).days
            if delta < 0:
                (birthday[0]) = now_ywd[0] + 1
                days_to_birthday = date((birthday[0]), (birthday[1]), (birthday[2]))
                delta = (days_to_birthday - now_date).days
                if delta <= days:
                    print(f'birthday of {nam.value} less {days} days')
            if delta <= days:
                print(f'birthday of {nam.value} less {days} days')
            else:
                print(f'Days left {delta} for {nam.value}')
        continue


# in USE new email/adress/birthday
def com_join_attribute(name, email=None, adress=None, birthday=None):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            if email:
                rec.email = email
                contact_list.add_record(nam, rec)
                print(f'A new email "{email}" has been added for the contact with the name "{name}".\n')
            if adress:
                rec.adress = adress
                contact_list.add_record(nam, rec)
                print(f'A new adress "{adress}" has been added for the contact with the name "{name}".\n')
            if birthday:
                rec.birthday = birthday
                contact_list.add_record(nam, rec)
                print(f'A new birthday "{birthday}" has been added for the contact with the name "{name}".\n')


# in USE delete email/adress/birthday
def com_delete_attribute(name, email=None, adress=None, birthday=None):
    if not name in [key.value for key in list(contact_list.keys())]:
        raise ValueError(
            f'Сontact with name "{name}" does not exist. Enter the correct name.\n')
    for nam, rec in contact_list.items():
        if nam.value == name:
            if email:
                print(f'A email "{rec.email}" has been remove for the contact with the name "{name}".\n')
                rec.email = None
                contact_list.add_record(nam, rec)

            if adress:
                print(f'A adress "{rec.adress}" has been remove for the contact with the name "{name}".\n')
                rec.adress = None
                contact_list.add_record(nam, rec)
            if birthday:
                print(f'A birthday "{rec.birthday}" has been remove for the contact with the name "{name}".\n')
                rec.birthday = None
                contact_list.add_record(nam, rec)


contact_list = contact_book.AddressBook()

def main ():
    global contact_list
    path = pathlib.Path('contact_list.txt')

    logger.debug('enter program')  # Логгирование

    if path.exists() and path.stat().st_size > 0:
        contact_list = contact_list.read_dumped_data()

    noter = Noter.Noter()
    ######### for HELP 1 MAIN MENU

    commands1 = ["contact", "noter", "sort file", "help", "exit"]
    prediction_experience1 = {}
    ####
    try:
        with open("experience.dat", "rb") as f:
            prediction_experience1 = pickle.load(f)
    except FileNotFoundError:
        prediction_experience1 = {}
        ####
    while True:
        text_help_menu = '''
            --------------
            Assistant v1.0
            --------------
            Программа - персональный ассистент. 
            -->Команды главного меню:
                contact - адресная книга
                noter - заметки
                sort file - сортировка файлов
                help - помощь 
                exit - выход из программы
            -->Команды адресной книги:
                add contact - добавить контакт
                delete contact - удалить контакт
                add number - добавить номер телефона существующему контакту 
                change number - изменить номер телефона существующему контакту
                delete number - удалить номер телефона существующему контакту
                new email - добавить email контакту
                delete email - удалить email существующему контакту
                new adress - добавить адрес существующему контакту 
                delete adress - удалить адрес существующему контакту
                new birthday - добавить день рождение существующему контакту
                delete birthday - удалить день рождение существующему контакту
                show - информация по указанному контакту
                show all - информация по всем контактам
                help - помощь
                return - выход в предыдущее меню
            -->Команды меню заметок:
                add note - добавить заметку
                show text - показать текст заметки
                show tag - показать тег заметки
                edit - редактировать заметку
                add tag - добавить тег существующей заметке
                delete - удалить заметку
                show - информация по указанной заметке
                show all - вывод названия всех заметок
                sort tag - сортировка заметок по тегу
                find text - поиск заметки по тексту
                help - помощь
                return - выход в предыдущее меню

            -->Запуск сортировки файлов:    
                В главном меню программы необходимо ввести 
                команду sort file

            '''
        text_main_menu = '''
                --------------
                Assistant v1.0
                --------------
                Программа - персональный ассистент. 
                Помощник имеет 3 функции:
                  1. Работа с адресной книгой;
                  2. Работа с заметками;
                  3. Сортировка файлов.
                --------------
                -->Главное меню
                Для перехода в необходимую подпрограмму введите команду:
                  contact - адресная книга
                  noter - заметки
                  sort file - сортировка файлов
                  help - помощь 
                  exit - выход из программы
                '''
        print(text_main_menu)
        command1 = input('Enter comand (contact, noter, sort file, help, exit): ')

        logger.debug(command1)  # Логгирование
        ####
        if not command1 in commands1:
            answer = ""
            while answer != "y":
                if command1 in commands1:
                    break
                for key, value in prediction_experience1.items():
                    if command1 in key:
                        print(f"(d)Perhaps you mean {prediction_experience1[key]}")
                        answer = str(input("Answer (Y/N): ")).lower()
                        if answer == "n":
                            command1 = str(input("Command input error, try again: ")).lower()
                        elif answer == "y":
                            command1 = prediction_experience1[key]
                            break
                if not command1 in commands1:
                    result = str(difflib.get_close_matches(command1, commands1, cutoff=0.1, n=1))[2:-2]
                    print(f"Perhaps you mean {result}")
                    answer = str(input("Answer (Y/N): ")).lower()
                    if answer == "n":
                        command1 = str(input("Command input error, try again: ")).lower()
                    elif answer == "y":
                        prediction_experience1[command1] = result
                        command1 = result
        ####
        if command1 == 'help':
            print(text_help_menu)
            command1 = input('Для продолжение введите -> next: ')
        if command1 == 'contact':  # CONTACT

            text_contact_menu = '''
                -->Меню Адресной книги
                Доступные команды:
                  add contact - добавить контакт
                  delete contact - удалить контакт
                  add number - добавить номер телефона существующему контакту 
                  change number - изменить номер телефона существующему контакту
                  delete number - удалить номер телефона существующему контакту
                  new email - добавить email контакту
                  delete email - удалить email существующему контакту
                  new adress - добавить адрес существующему контакту 
                  delete adress - удалить адрес существующему контакту
                  new birthday - добавить день рождение существующему контакту
                  delete birthday - удалить день рождение существующему контакту
                  day to birthday - выводить список контактов у которых день рождения в промежутке заданного количества дней от текущей даты 
                  show - информация по указанному контакту
                  show all - информация по всем контактам
                  help - помощь
                  return - выход в предыдущее меню
                '''
            print(text_contact_menu)
            ######## for HELP 2 CONTACT
            commands2 = ["add contact", "delete contact",
                         "show", "show all",
                         "add number", "change number", "delete number",
                         "new email", "delete email",
                         "new adress", "delete adress",
                         "new birthday", "delete birthday", "day to birthday",
                         "return", "help"]

            prediction_experience2 = {}
            ####
            try:
                with open("experience.dat", "rb") as f:
                    prediction_experience2 = pickle.load(f)
            except FileNotFoundError:
                prediction_experience2 = {}
                ####
            while True:  # CONTACT COMAND
                command2 = str(input("Enter command :>> ")).lower()
                logger.debug(command2)  # Логгирование
                ####
                if not command2 in commands2:
                    answer = ""
                    while answer != "y":
                        if command2 in commands2:
                            break
                        for key, value in prediction_experience2.items():
                            if command2 in key:
                                print(f"(d)Perhaps you mean {prediction_experience2[key]}")
                                answer = str(input("Answer (Y/N): ")).lower()
                                if answer == "n":
                                    command2 = str(input("Command input error, try again: ")).lower()
                                elif answer == "y":
                                    command2 = prediction_experience2[key]
                                    break
                        if not command2 in commands2:
                            result = str(difflib.get_close_matches(command2, commands2, cutoff=0.1, n=1))[2:-2]
                            print(f"Perhaps you mean {result}")
                            answer = str(input("Answer (Y/N): ")).lower()
                            if answer == "n":
                                command2 = str(input("Command input error, try again: ")).lower()
                            elif answer == "y":
                                prediction_experience2[command2] = result
                                command2 = result
                ####

                if command2 == "add contact":  # add contact
                    print("Creating a contact...")
                    while True:
                        name = input("Enter name:> \n").strip()
                        result = contact_list.iterator()
                        name_list = []
                        for n in result:
                            for rec in n:
                                name_list.append(rec.name.value)
                        if name in name_list:
                            print(f"'{name}' is used. Choose another name")
                            continue
                        if not name:
                            print("Empty input")
                            continue
                        else:
                            phone = input(
                                "Enter phone '+380XXXXXXXXX or 0XXXXXXXXX':> \n").strip()
                            REG_PHONE = '(^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$))'
                            if not re.search(REG_PHONE, str(phone)):
                                print(
                                    f'This phone number "{phone}" is not correct. Please enter a 10 or 12 digit phone number.\n')
                                continue
                            else:
                                answer = input(
                                    "Do you need add adress (Y/N):> ").lower()
                            if answer == "y":
                                adress = str(
                                    input("Enter adress:> \n")).strip()
                                continue
                            elif answer == "n":
                                adress = None
                            else:
                                print("Incorrect answer.")
                                continue
                            answer = (
                                input("Do you need add email (Y/N):> ")).lower()
                            if answer == "y":
                                email = contact_book.Email(
                                    input("Enter email 'dog@gmail.com':> \n").strip()).value
                                SAN_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                                if not re.search(SAN_EMAIL, str(email)):
                                    print(
                                        f'This email "{email}" is not correct.\n')
                                    continue
                            elif answer == "n":
                                email = None
                            else:
                                print("Incorrect answer.")
                                continue
                            answer = (
                                input("Do you need add day of birthday (Y/N):> \n")).lower()
                            if answer == "y":
                                birthday = contact_book.Birthday(
                                    (input("Enter birthday 'YYYY-MM-DD':> \n").strip())).value
                                REG_DATE = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
                                if not re.search(REG_DATE, str(birthday)):
                                    print(
                                        f'Please enter your birthday in the format: "YYYY-MM-DD".\n')
                                    continue
                            elif answer == "n":
                                birthday = None
                            else:
                                print("Incorrect answer.")
                                continue
                            print(com_add(name=contact_book.Name(name), phone=contact_book.Phone(
                                phone), email=email, adress=contact_book.Adress(adress).value, birthday=birthday))
                            serialized_lpist = contact_list.save_dumped_data()
                        break

                if command2 == "change number":  # CHANGE NUMBER
                    name = input("Enter name:> ").strip()
                    phone = input("Enter old number:> ").strip()
                    new_phone = input("Enter new number:> ").strip()
                    REG_PHONE = '(^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$))'
                    if not re.search(REG_PHONE, str(new_phone)):
                        print(
                            f'This phone number "{new_phone}" is not correct. Please enter a 10 or 12 digit phone number.\n')
                        continue
                    else:
                        com_change(name, phone, contact_book.Phone(new_phone))
                        serialized_lpist = contact_list.save_dumped_data()

                if command2 == "day to birthday":  # day to birthday
                    print("Choosing the days to birthday...")
                    day = input("Enter days:> ").strip()
                    days_to_birthday(int(day))

                if command2 == "show":  # show
                    print("Choosing the contact to show...")
                    name = input("Enter name:> ").strip()
                    print(com_search(name))

                if command2 == "delete contact":  # delete contact
                    print("Choosing the contact to delete...")
                    name = input("Enter name:> ").strip()
                    com_delete_contact(name)
                    print(f'The contact "{name}" has been delete".\n')

                if command2 == "add number":  # ADD NUMBER
                    name = input("Enter name:> ").split()[0]
                    phone = input("Enter number:> ").split()[0]
                    REG_PHONE = '(^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$))'
                    if not re.search(REG_PHONE, str(phone)):
                        print(
                            f'This phone number "{phone}" is not correct. Please enter a 10 or 12 digit phone number.\n')
                        continue
                    else:
                        com_join(name, contact_book.Phone(phone))
                        serialized_lpist = contact_list.save_dumped_data()

                if command2 == "new email":  # new EMAIL

                    name = input("Enter name:> ").strip()
                    email = input("Enter email:> ").strip()
                    SAN_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if not re.search(SAN_EMAIL, str(email)):
                        print(f'This email "{email}" is not correct.\n')
                        continue
                    else:
                        com_join_attribute(
                            name, email=contact_book.Email(email).value)
                        serialized_lpist = contact_list.save_dumped_data()
                if command2 == "new adress":  # new ADRESS

                    name = input("Enter name:> ").strip()
                    adress = input("Enter adress:> ").strip()
                    com_join_attribute(name, adress=contact_book.Adress(adress).value)
                    serialized_lpist = contact_list.save_dumped_data()

                if command2 == "new birthday":  # new BIRTHDAY

                    name = input("Enter name:> ").strip()
                    birthday = input("Enter birthday:> ").strip()
                    REG_DATE = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
                    if not re.search(REG_DATE, str(birthday)):
                        print(
                            f'Please enter your birthday in the format: "YYYY-MM-DD".\n')
                        continue
                    else:
                        com_join_attribute(
                            name, birthday=contact_book.Birthday(birthday).value)
                        serialized_lpist = contact_list.save_dumped_data()
                if command2 == "delete email":  # delete EMAIL

                    name = input("Enter name:> ").strip()
                    email = 'None'
                    com_delete_attribute(name, email=email)
                    serialized_lpist = contact_list.save_dumped_data()

                if command2 == "delete adress":  # delete ADRESS

                    name = input("Enter name:> ").strip()
                    adress = 'None'
                    com_delete_attribute(name, adress=adress)
                    serialized_lpist = contact_list.save_dumped_data()

                if command2 == "delete birthday":  # delete BIRTHDAY

                    name = input("Enter name:> ").strip()
                    birthday = 'None'
                    com_delete_attribute(name, birthday=birthday)
                    serialized_lpist = contact_list.save_dumped_data()

                if command2 == "delete number":  # DELETE PHONE
                    name = input("Enter name:> ").strip()
                    phone = input("Enter number:> ").strip()
                    com_delete(name, phone)

                if command2 == "show all":  # show all
                    result = contact_list.iterator()
                    for n in result:
                        for rec in n:
                            print(f'name: {rec.name.value}; phone: {", ".join([phone.value for phone in rec.phones])};'
                                  f' email {rec.email if rec.email else "-"} '
                                  f'adress {rec.adress if rec.adress else "-"} '
                                  f'birthday {rec.birthday if rec.birthday else "-"} '
                                  )

                if command2 == "return":
                    print("Return to main menu")
                    with open("experience2.dat", "wb") as f:
                        pickle.dump(prediction_experience2, f)
                    break

        if command1 == 'noter':  # NOTER
            text_noter_menu = '''
                -->Меню Заметок
                Доступные кооманды:
                  add note - добавить заметку
                  show text - показать текст заметки
                  show tag - показать тег заметки
                  edit - редактировать заметку
                  add tag - добавить тег существующей заметке
                  delete - удалить заметку
                  show - информация по указанной заметке
                  show all - вывод названия всех заметок
                  sort tag - сортировка заметок по тегу
                  find text - поиск заметки по тексту
                  help - помощь
                  return - выход в предыдущее меню
                            '''
            print(text_noter_menu)
            ######## for HELP 3 NOTER
            commands3 = ["add note", "add tag",
                         "show text", "show tag", "show", "show all",
                         "delete", "return", "edit",
                         "sort tag", "find text", "help"]

            prediction_experience3 = {}
            try:
                with open("experience.dat", "rb") as f:
                    prediction_experience3 = pickle.load(f)
            except FileNotFoundError:
                prediction_experience3 = {}
            while True:  # NOTER COMAND
                command3 = str(input("Enter command:>> ")).lower()
                logger.debug(command3)  # Логгирование
                if not command3 in commands3:
                    answer = ""
                    while answer != "y":
                        if command3 in commands3:
                            break
                        for key, value in prediction_experience3.items():
                            if command3 in key:
                                print(f"(d)Perhaps you mean {prediction_experience3[key]}")
                                answer = str(input("Answer (Y/N): ")).lower()
                                if answer == "n":
                                    command3 = str(input("Command input error, try again: ")).lower()
                                elif answer == "y":
                                    command3 = prediction_experience3[key]
                                    break
                        if not command3 in commands3:
                            result = str(difflib.get_close_matches(command3, commands3, cutoff=0.1, n=1))[2:-2]
                            print(f"Perhaps you mean {result}")
                            answer = str(input("Answer (Y/N): ")).lower()
                            if answer == "n":
                                command3 = str(input("Command input error, try again: ")).lower()
                            elif answer == "y":
                                prediction_experience3[command3] = result
                                command3 = result

                if command3 == "add note":  # ADD NOTE
                    print("Creating a note...")
                    while True:
                        name = str(input("Enter name:> "))
                        if f"{name}.json" in noter.scan():
                            print(f"'{name}' is used. Choose another name")
                            continue
                        else:
                            text = str(input("Enter text:> "))
                            answer = str(input("Do you need tags recording now (Y/N):> ")).lower()
                            if answer == "y":
                                tags = str(input("Enter tags:> "))
                                print(noter.add(name, text, tags))
                            elif answer == "n":
                                print(noter.add(name, text))
                            else:
                                print("Incorrect answer. Default mode is a new note without tag")
                                print(noter.add(name, text))
                        break

                if command3 == "show":  # SHOW
                    print("Choosing the note to show...")
                    name = str(input("Enter name:> "))
                    print(noter.show_note(name))

                if command3 == "add tag":  # add_tag
                    print("Choosing the note...")
                    name = (input("Enter name:> ").strip())
                    tag = (input("Enter tag:> ").strip())
                    print(noter.add_tag(name, tag))

                if command3 == "sort tag":  # sort_by_tag
                    tag = (input("Enter tag:> ").strip())
                    print(noter.sort_by_tag(tag))

                if command3 == "find text":  # find_by_text
                    text = (input("Enter text:> ").strip())
                    print(noter.find_by_text(text))

                if command3 == "edit":  # edit
                    print("Choosing the note to edit...")
                    name = (input("Enter name:> ").strip())
                    text = (input("Enter text:> ").strip())
                    tag = (input("Enter tag:> ").strip())
                    print(noter.edit(name, text, tag))

                if command3 == "show tag":  # SHOW TAG
                    print(noter.show_content_by_tag())

                if command3 == "show text":  # SHOW TEXT
                    print(noter.show_content_by_text())

                if command3 == "delete":  # DELETE
                    print("Choosing the note to delete...")
                    name = str(input("Enter name:> "))
                    print(noter.delete(name))

                if command3 == "show all":  # SHOW ALL
                    print(noter.scan())

                if command3 == "return":  # return
                    print("Return to main menu")
                    with open("experience3.dat", "wb") as f:
                        pickle.dump(prediction_experience3, f)

                    break

        if command1 == 'sort file':  # SORT FILE
            # HELP 4
            input_arg = input(
                'Enter the directory for sorting (disk:/folder/folder/) ')
            sort_folder = Path(input_arg)
            logger.debug(command1)  # Логгирование
            sort_file.main(sort_folder)
            break

        if command1 == 'exit':
            logger.debug('exit program')  # Логгирование
            break

if __name__ == '__main__':
    main()