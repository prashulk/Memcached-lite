import socket
import random
import sys

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9889))

    try:
        for _ in range(1, 100):
            # Generate a random key and value for the set command
            key = "c3-" + str(random.randint(1, 20))
            value = str(random.randint(1, 100))
            value_size = sys.getsizeof(value)
            command_message = f"set {key} {value_size}\r\n{value}\r\n"
            command = f"set {key} {value}\r\n"  # Exclude value size

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
