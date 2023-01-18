# Uncomment this to pass the first stage
import socket
import _thread
from datetime import datetime

from app.resp_decoder import RESPDecoder

memory = dict()


def handle_client(client_connection):
    while True:
        try:
            command, *args = RESPDecoder(client_connection).decode()
            print(command, args)
            if command == b"ping":
                client_connection.send(b"+PONG\r\n")
            elif command == b"echo":
                client_connection.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
            elif command == b"set":
                store_result = (args[1], None)
                if len(args) == 4 and args[2] == b"px":
                    now = datetime.now().timestamp()
                    exp_at = now + int(args[3].decode()) / 1000
                    store_result = (args[1], exp_at)

                memory[args[0]] = store_result
                client_connection.send(b"+OK\r\n")
            elif command == b"get":
                res, exp = memory[args[0]]
                if not res:
                    client_connection.send(b"$-1\r\n")
                    continue

                now = datetime.now().timestamp()
                if exp and now > exp:
                    memory[args[0]] = None
                    client_connection.send(b"$-1\r\n")
                    continue

                client_connection.send(b"$%d\r\n%b\r\n" % (len(res), res))
            else:
                client_connection.send(b"-ERR unknown command\r\n")
        except ConnectionError:
            break  # Stop serving if the client connection is closed


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_conn, _ = server_socket.accept()
        _thread.start_new_thread(handle_client, (client_conn,))


if __name__ == "__main__":
    main()
