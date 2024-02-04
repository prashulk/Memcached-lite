import socket
import random
import sys


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9889))

    def get_response(command):
        client_socket.send(command.encode("utf-8"))
        try:
            return client_socket.recv(1024).decode("utf-8")
        except ConnectionResetError as e:
            return "NOT STORED" if "set" in command else "SERVER STOPPED"

    try:
        for _ in range(1, 100):
            if _ % 3 != 0:
                # Generate a random key and value for the set command
                key = "c1-" + str(random.randint(1, 20))
                value = str(random.randint(1, 100))
                value_size = sys.getsizeof(value)
                command_message = f"set {key} {value_size}\r\n{value}\r\n"
                command = f"set {key} {value}\r\n"  # Exclude value size
            else:
                # Generate a random key for the get command
                key = "c1-" + str(random.randint(1, 20))
                command_message = f"get {key}"
                command = f"get {key}\r\n"

            response = get_response(command)
            print(f"input: {command_message}\noutput:\n{response} \n")

    except ConnectionResetError as e:
        print(e)
        client_socket.close()

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
