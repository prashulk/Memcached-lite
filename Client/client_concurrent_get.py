import socket
import random
import sys

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9889))

    try:
        for _ in range(1, 100):
            # Generate a random key for the get command
            key = "c3-" + str(random.randint(1, 20))
            command_message = f"get {key}"
            command = f"get {key}\r\n"

            response = get_response(client_socket, command)
            print(f"input: {command_message}\noutput:\n{response} \n")

    except ConnectionAbortedError as e:
        print("Connection aborted by the server or host.")
    finally:
        client_socket.close()

def get_response(client_socket, command):
    client_socket.send(command.encode("utf-8"))
    return client_socket.recv(1024).decode("utf-8")

if __name__ == "__main__":
    main()
