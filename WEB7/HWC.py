import socket
import threading
import time

port = '127.0.0.1'
host = 1235


def listening(soc):
    try:
        while True:
            income = (soc.recv(4096)).decode()
            in_name, in_message = income.split('|||')
            print(f'{in_name:>10}: {in_message}')
            if in_message == 'exit':
                break
    except ConnectionResetError or Exception:
        soc.close()


def start_client(port, host):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name = input('\nWelcome to CHAT (client)!\n Please, enter your name and start communication:\n>>> ')
    while True:
        try:
            soc.connect((port, host))
            break
        except ConnectionRefusedError:
            print('Waiting for the host...')
            time.sleep(3)
    print("Connected")
    try:
        while True:
            try:
                t_lis = threading.Thread(target=listening, args=(soc,), daemon=True)
                t_lis.start()
            except ConnectionRefusedError or Exception:
                print("Connection is lost or another user has left")
                break
            msg = input("")
            if msg == 'exit':
                try:
                    data = str((name + '|||' + msg)).encode()
                    soc.send(data)
                except OSError:
                    print("Connection is lost or another user has left")
                break
            else:
                try:
                    data = str((name + '|||' + msg)).encode()
                    soc.send(data)
                except OSError:
                    print("Connection is lost or another user has left")
                    break
        print('Good bye!')
    except ConnectionResetError:
        print('Connection is lost or another user has left the chat')


if __name__ == '__main__':
    start_client(port, host)
