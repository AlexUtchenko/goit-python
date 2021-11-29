import difflib
import redis
from pymongo import MongoClient


client = MongoClient('mongodb+srv://Alex:goit123@utcluster.zrkwr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')


def add():
    name = input('Enter name: ')
    if db.ContactBook.find_one({'name': name}):
        print(f"The record with name '{name}' is already exist. Try another name or update the one")
    phone = input('Enter phone: ')
    email = input('Enter email: ')
    db.ContactBook.insert_one({'name': name, 'email': email, 'phone': phone})
    print('New record successfully added')


def showall():
    for rec in db.ContactBook.find():
        print(f'name = {rec["name"]}, phone = {rec["phone"]}, email = {rec["email"]}')


def delete():
    name = input('Enter name: ')
    if db.ContactBook.find_one({'name': name}):
        db.ContactBook.delete_one({'name': name})
        print(f'Record with name "{name}" has been successfully deleted')
    else:
        print("There is no such record in DB")


def show():
    name = input('Enter name: ')
    result = db.ContactBook.find_one({'name': name})
    if result:
        print(f'name = {result["name"]}, phone = {result["phone"]}, email = {result["email"]}')
    else:
        print("There is no such record in DB")


def update():
    name = input('Enter name: ')
    if db.ContactBook.find_one({'name': name}):
        print("The record exists in DB. Enter a new data:")
        phone = input('Enter phone: ')
        email = input('Enter email: ')
        db.ContactBook.update_one({'name': name}, {'$set': {'name': name, 'email': email, 'phone': phone}})
        print(f'Record "{name}" has been successfully updated')
    else:
        print("There is no such record in DB. Try another command")


def find():
    data = input('Enter data: ')
    query = {"$or": [{"phone": {"$regex": data}}, {"email": {"$regex": data}}]}
    res = db.ContactBook.find(query, {'_id': 0})
    if res != None:
        for rec in res:
            print(f" Name = {rec['name']}, phone = {rec['phone']}, email = {rec['email']}")
    else:
        print("There is no such record in DB. Try another command")


def command_assistant():
    commands = ['add', 'show', 'delete', 'show_all', 'exit', 'update', 'find']                      # list of commands
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        command = str(input('Enter command:\n>>> ')).lower().strip()
        if not command in commands:                                                                 # prediction logic
            if r.get(command):                                                                      # checking cache
                print(f"(Cache)Perhaps you mean {(r.get(command)).decode('utf-8')}")
                ans = str(input("Answer (Y/N): ")).lower()
                if ans == "n":
                    print("Command input error, try again")
                    continue
                elif ans == "y":
                    variant = r.get(command).decode('utf-8')
                    break
            else:
                variant = str(difflib.get_close_matches(command, commands, cutoff=0.1, n=1))[2:-2]       # prediction realisation
                print(f"Perhaps you mean {variant}")
                answer = str(input("Answer (Y/N): ")).lower()
                if answer == "n":
                    print("Command input error, try again")
                    continue
                elif answer == "y":
                    r.set(command, variant)
                    break
        else:
            variant = command
            break
    return variant

if __name__ == '__main__':
    with client:
        db = client.myfirst_mongoDB
        print(f'{" "*20}*** Welcome to Personal assistant Contact book DB edition!***')
        print("Commands:\n - add;\n - show;\n - show_all;\n - delete;\n - update;\n - find;\n - exit\n")
        while True:
            try:
                answer = command_assistant()
            except (ConnectionRefusedError, redis.exceptions.ConnectionError, ConnectionError) as Error:
                print("Error! Connection problems to Redis. App is working without command prediction")
                answer = str(input('Enter command:\n>>> ')).lower().strip()
            if answer == 'add':
                add()
                continue
            elif answer == 'show_all':
                showall()
                continue
            elif answer == 'delete':
                delete()
                continue
            elif answer == 'show':
                show()
                continue
            elif answer == 'update':
                update()
                continue
            elif answer == 'find':
                find()
                continue
            elif answer == 'exit':
                break
            else:
                print("Command input error. Try correct command again")
                continue
        print("Good bye!")







