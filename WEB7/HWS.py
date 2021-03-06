import socket
import threading

host = '127.0.0.1'
port = 1235


def listen_user(user):
    while True:
        try:
            income = user.recv(4096).decode()
        except ConnectionResetError or Exception:
            user.close()
            break
        in_name, in_message = income.split('|||')
        print(f'{in_name:>10}: {in_message}')
        if in_message == 'exit':
            break



def start_server(host, port):
    name = input(' '*20 + 'Welcome to CHAT (host)!\n * print "exit" for quit the chat!\nPlease, enter your name and start communication:\n>>> ')
    with socket.socket() as soc:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((host, port))
        soc.listen(1)
        print("server started and it is waiting for the client connection...")
        user_socket, address = soc.accept()
        print(f'Client  {address[0]} is connected')
        with user_socket:
            while True:
                try:
                    listen_in_tread = threading.Thread(target=listen_user, args=(user_socket,), daemon=True)
                    listen_in_tread.start()
                except ConnectionResetError or Exception:
                    print('Connection is lost or another user has left the chat')
                    # user_socket.close()
                    # soc.close()
                    break
                msg = input("")
                if msg == 'exit':
                    data = str((name + '|||' + msg)).encode()
                    try:
                        user_socket.send(data)
                        break
                    except OSError:
                        print("Connection is lost or another user has left")
                else:
                    data = str((name + '|||' + msg)).encode()
                    try:
                        user_socket.send(data)
                    except OSError:
                        print("Connection is lost or another user has left")
                        break
    print('Good bye!')


if __name__ == '__main__':
    start_server(host, port)
