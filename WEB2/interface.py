from abc import ABC, abstractmethod
import difflib
from pathlib import Path
import json
import pickle


class Command(ABC):

    def __init__(self):
        self.commands = []

    @abstractmethod
    def execute(self, command):
        pass

    @abstractmethod
    def validate(self):
        pass

class PartChoosingInterface(Command):

    def __init__(self):
        self.commands = ['contact', 'noter', 'sort file', 'help', 'exit']

    def validate(self):
        print("Welcome to noter advanced iterface!\nChoose a part or command (noter for test) you need: 'contact', 'noter', 'sort file', 'help', 'exit'")
        command = str(input("Please enter a command.\n>>> ")).lower()
        if not command in self.commands:
            answer = "n"
            while answer == 'n':
                result = str(difflib.get_close_matches(command, self.commands, cutoff=0.1, n=1))[2:-2]
                print(f"Perhaps you mean {result}")
                answer = str(input("Answer (Y/N): ")).lower()
                if answer == "n":
                    command = str(input("Command prediction fail. Try another variant.\n>>> ")).lower()
                    continue
                elif answer == "y":
                    return result
                else:
                    print("{answer} is not correct answer. Choose Y/N for answering")
                    continue
        else:
            return command

    def execute(self, command):
        print(f"Going to the {command} part...")
        if command == 'noter':
            print('''
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
                ''')
            noter_int = NoterInterface()
            noter_int.execute(noter_int.validate())
        if command == 'exit':
            return "final"


class NoterInterface(PartChoosingInterface):

    def __init__(self):
        self.commands = ["add note", "add_tag",
                         "show text", "show_tag", "show", "show_all",
                         "delete", "return", "edit",
                         "sort tag", "find text", "help"]


    def execute(self, item):
        noter = Noter()
        if item == "add note":
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
        elif item == "show":
            print("Choosing the note to show...")
            name = str(input("Enter name:> "))
            print(noter.show_note(name))
        elif item == "delete":  # DELETE
            print("Choosing the note to delete...")
            name = str(input("Enter name:> "))
            print(noter.delete(name))
        elif item == 'exit':
            exInterface = PartChoosingInterface()
            exInterface.execute(exInterface.validate())


class Noter:

    FOLDER = "noter_data/"

    def scan(self):     #сканирует папку для записей на актуальное наличие файлов *.json
        try:
            self.folder = Path(Noter.FOLDER)
            self.content = []
            for item in self.folder.iterdir():
                self.extension = Path(item.name).suffix[1:].upper()
                if self.extension == "JSON":
                    self.content.append(item.name)
            return self.content
        except FileNotFoundError:
            self.folder.mkdir(exist_ok=True)
            return []

    def add(self, name, text: str, tag=None):     #создает заметку. Аргументы: 1 = имя, 2 = заметка, 3 = тэг(None по умолчанию)
        self.note = {text: tag}
        self.new_file_name = f"{str(Noter.FOLDER)}{name}.json"
        with open(self.new_file_name, "w") as f:
            json.dump(self.note, f)
        return f"Record '{name}' was successfully added"

    def show_content_by_text(self):     #сканирует папку и выводит актуальный словарь типа имя:заметка
        res_str = ""
        for item in Path(Noter.FOLDER).iterdir():
            extension = Path(item.name).suffix[1:].upper()
            if extension == "JSON":
                with open(item, "r") as f:
                    note = json.load(f)
                for key, value in note.items():
                    res_str += f"Name: {item.name[:-5]}\nText: {key}\n{'='*20}\n"
        if res_str:
            return res_str
        return f"There is nothing yet"

    def show_content_by_tag(self):      #сканирует папку и выводит актуальный словарь типа имя:тэг
        res_str = ""
        for item in Path(Noter.FOLDER).iterdir():
            extension = Path(item.name).suffix[1:].upper()
            if extension == "JSON":
                with open(item, "r") as f:
                    note = json.load(f)
                for key, value in note.items():
                    res_str += f"Name: {item.name[:-5]}\nText: {value}\n{'-'*20}\n"
        if res_str:
            return res_str
        return f"There is nothing yet"

    def delete(self, name):       #удаляет запись по имени
        file = Path(f"{Noter.FOLDER}{name}.json")
        try:
            file.unlink(missing_ok=False)
            return f"Record number '{name}' was successfully deleted"
        except FileNotFoundError:
            return f"Record number '{name}' doesn`t exist. Check content and try again"

    def show_note(self, name): # выводит заметку с тэгом по имени
        res_dic = {}
        file = Path(f"{Noter.FOLDER}{name}.json")
        try:
            with open(file, "r") as f:
                note = json.load(f)
            for key, value in note.items():
                text = key
                tag = value
                if tag == None:
                    return f"Name: {name}\nText: {text}"
                else:
                    return f"Name: {name}\nText: {text}\nTag: {tag}"
        except FileNotFoundError:
            return f"Record '{name}' doesn`t exist. Check content and try again"

    def edit(self, name, text, tag):  # редактирует / перезаписывает заметку. Логика дозаписи: show_note() -> edit()
        res_dic = {}
        file = Path(f"{Noter.FOLDER}{name}.json")
        try:
            with open(file, "w") as f:
                res_dic[text] = tag
                json.dump(res_dic, f)
            return f"Record '{name}' was successfully edited"
        except FileNotFoundError:
            return f"Record '{name}' doesn`t exist. Check content and try again"

    def add_tag(self, name, tag):  # дописывает тэг
        res_dic = {}
        file = Path(f"{Noter.FOLDER}{name}.json")
        try:
            with open(file, "r") as f:
                res_dic = json.load(f)
                for key in res_dic.keys():
                    k = key
                res_dic[k] = tag
            with open(file, "w") as f:
                json.dump(res_dic, f)
            return f"Tag '{tag}' was added to '{name}'"
        except FileNotFoundError:
            return f"Record '{name}' doesn`t exist. Check content and try again"


    def find_by_text(self, req):  # сканирует текст заметок на совпадение, выдает словарь типа имя:заметка
        res_str = ""
        for item in Path(Noter.FOLDER).iterdir():
            extension = Path(item.name).suffix[1:].upper()
            if extension == "JSON":
                with open(item, "r") as f:
                    note = json.load(f)
                for key, value in note.items():
                    if str(req) in key:
                        res_str += f"Name: {item.name[:-5]}\nText: {key}\n{'='*20}\n"
        if res_str:
            return res_str
        return f"There is no this text in notes"

    def sort_by_tag(self, req):  # сканирует имена и теги, выдает список фалов с совпадениями в алфавитном порядке
        res_list = []
        res_str = ""
        for file_name in self.scan():
            if req in file_name:
                res_list.append(file_name[:-5])
        for item in Path(Noter.FOLDER).iterdir():
            extension = Path(item.name).suffix[1:].upper()
            if extension == "JSON":
                with open(item, "r") as f:
                    note = json.load(f)
                for key, value in note.items():
                    if str(req) in str(value):
                        res_list.append(item.name[:-5])
        if res_list:
            res_list.sort()
            res_str = "The next files containe the request in their names or tags:\n"
            for rec in res_list:
                res_str += f" - '{rec}'\n"
            return res_str
        return f"There is no this text in tags and names"



if __name__ == '__main__':
    start = None
    while start is None:
        exInterface = PartChoosingInterface()
        start = exInterface.execute(exInterface.validate())
        if start is None:
            end = str(input("Закончить или продолжить? (Y/N)\n>>> ")).lower()
            if end == 'y':
                break
            elif end == 'n':
                start = None
                continue
            else:
                print("Uncorrect answer.")
                start = "final"
                continue
    print('The program is finished')
