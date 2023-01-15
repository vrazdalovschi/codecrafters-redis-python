# Uncomment this to pass the first stage
import socket
import _thread

from app.resp_decoder import RESPDecoder

memory = dict()


def handle_client(client_connection):
    while True:
        try:
            command, *args = RESPDecoder(client_connection).decode()
            if command == b"ping":
                client_connection.send(b"+PONG\r\n")
            elif command == b"echo":
                client_connection.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
            elif command == b"set":
                memory[args[0]] = args[1]
                client_connection.send(b"+OK\r\n")
            elif command == b"get":
                client_connection.send(b"$%d\r\n%b\r\n" % (len(memory[args[0]]), memory[args[0]]))
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
