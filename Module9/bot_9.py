def parse(request):
    if request[:5].casefold() == 'hello':
        act = "hello"
        return act
    elif request[:4].casefold() == 'exit':
        act = "bye"
        return act
    elif request[:5].casefold() == 'close':
        act = "bye"
        return act
    elif request[:3].casefold() == 'add':
        act = "add"
        return act
    elif request[:6].casefold() == 'change':
        act = "change"
        return act
    elif request[:5].casefold() == 'phone':
        act = "phone"
        return act
    elif request[:8].casefold() == 'show all':
        act = "show"
        return act
    elif request[:8].casefold() == 'good bye':
        act = "bye"
        return act


def input_error(func):
    def inner(act, request):
        global result
        try:
            request_in = request.casefold()
            if request_in.split(' ')[0] in ['hello', 'close', 'exit'] and len(request.strip().split(' ')) != 1:
                print("Name is not nedded")
                result = ""
            elif request_in.split(' ')[0] in ['phone'] and len(request_in.strip().split(' ')) != 2:
                print("Enter user name")
                result = ""
            elif request_in.split(' ')[0] in ['show', 'good'] and request_in.split(' ')[1] in ['all', 'bye'] and len(request_in.strip().split(' ')) != 2:
                print("Enter user name")
                result = ""
            elif request_in.split(' ')[0] in ['add', 'change'] and len(request_in.strip().split(' ')) != 3:
                print("Give me name and phone please")
                result = ""
            elif request_in.split(' ')[0] in ['hello', 'show', 'good', 'close', 'exit', 'phone', 'add',
                                              'change']:
                func(act, request)
            else:
                print("Command error")
                result = ""
        except ValueError:
            print('ValueError')
            result = ""
        except KeyError:
            print('ValueError')
            result = ""
        except IndexError:
            print('IndexError')
            result = ""

    return inner


@input_error
def handle(act, request):
    global result
    if act == "hello":
        result = "hello"
    elif act == "bye":
        result = "stop"
    elif act == "add":
        components = request[4:].split()
        phone_book[components[0]] = components[1]
        result = "add"
    elif act == "change":
        components = request[7:].split()
        if components[0] in phone_book:
            phone_book[components[0]] = components[1]
        else:
            print("There is no such name")
        result = "change"
    elif act == "show":
        result = "show"
    elif act == "phone":
        result = "phone"


if __name__ == "__main__":
    phone_book = {}
    result = ""
    while result != "stop":
        request = input("Enter request: ")
        if request == "":
            print("Enter command")
            continue
        act = parse(request)
        handle(act, request)
        if result == "show":
            for key, value in phone_book.items():
                print(f"{key} {value}")
        elif result == "hello":
            print("How can I help you?")
        elif result == "phone":
            print(phone_book[request[6:]])
    print("Good bye!")
