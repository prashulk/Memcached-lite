import socket
import threading
import sys
import time
import random

def read_previous_state(path):
    """
    Read and return the previous state from a file.
    """
    dic = {}
    with open(path, "r") as f:
        for line in f:
            key, value = line.strip().split(" ", 1)
            dic[key] = value
    return dic

def write_current_state(path, key, value):
    """
    Write the current state to a file.
    """
    with open(path, "a") as f:
        f.write(f"{key} {value}\n")

def set_operation(current_dic, file_path, key, value):
    """
    Perform the SET operation.
    """

    with threading.Lock():
        write_current_state(file_path, key, value)
        current_dic[key] = value

def get_operation(current_dic, key):
    """
    Perform the GET operation.
    """
    if key in current_dic:
        return f"VALUE {key} {sys.getsizeof(current_dic[key])}\r\n{current_dic[key]}\r\n"
    else:
        return "NOT FOUND"

def handle_client(client_socket, current_dic, file_path, mutex):
    """
    Handle client requests.
    """
    client_address = client_socket.getpeername()
    print(f"Accepted connection from {client_address}")

    try:
        while True:

            command = client_socket.recv(1024).decode("utf-8").strip()

            if not command:
                break

            response = ""

            if command.startswith("set "):
                _, key, value = command.split(" ", 2)
                sleep_duration = random.uniform(0, 2)
                time.sleep(sleep_duration)  # Sleep before SET operation
                set_operation(current_dic, file_path, key, value)
                response = "STORED"

            elif command.startswith("get "):
                _, key = command.split(" ", 1)
                sleep_duration = random.uniform(0, 1)
                time.sleep(sleep_duration)  # Sleep before GET operation
                response = get_operation(current_dic, key)

            elif command == "quit":
                break

            else:
                response = "ERROR\r\n"

            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"Client {client_address} error: {e}")

    finally:
        client_socket.close()
        print(f"Connection from {client_address} closed")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9889))
    server_socket.listen(5)
    file_path = "data.txt"
    current_dic = read_previous_state(file_path)
    mutex = threading.Lock()

    print("Server listening on localhost:9889")

    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, current_dic, file_path, mutex))
        client_handler.start()

if __name__ == "__main__":
    main()
