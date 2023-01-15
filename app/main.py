# Uncomment this to pass the first stage
import socket
import _thread


class UnsupportedCommandError(Exception):
    pass


def handle_client(conn):
    while True:
        data = conn.recv(2048)
        command, args = parse_command(data)
        if command == 'ping':
            conn.sendall(b"+PONG\r\n")
        elif command == 'echo':
            conn.sendall(b"+%b\r\n" % args[0])
        else:
            raise UnsupportedCommandError()


def parse_command(data: bytes) -> (str, list):
    print("parse_command", data)
    if data[0:1] != b"*":
        raise UnsupportedCommandError()

    up_to = data.find(b'\r\n')
    array_size = int(data[1:up_to])
    command_size_pos = data.find(b'$') + 1
    command_size_post2 = data.find(b'\r\n', command_size_pos)
    command_size = int(data[command_size_pos:command_size_post2])
    command = data[command_size_post2 + 2: command_size_post2 + 2 + command_size]

    if array_size == 1:
        return command.decode('utf-8'), []
    elif array_size == 2:
        args_size_from_pos = data.find(b'$', command_size_post2 + 2 + command_size) + 1
        args_size_upto_pos = data.find(b'\r\n', args_size_from_pos)
        args_size = int(data[args_size_from_pos:args_size_upto_pos])
        argg = data[args_size_upto_pos + 2: args_size_upto_pos + 2 + args_size]

        return command.decode('utf-8'), [argg]

    raise UnsupportedCommandError()


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
