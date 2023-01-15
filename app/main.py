# Uncomment this to pass the first stage
import socket
import _thread


def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if data:
            conn.sendall(b"+PONG\r\n")


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
