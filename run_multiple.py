import subprocess
import os
import time

def run_client(client_number):
    try:
        subprocess.run(["python3", "client.py"])
    except Exception as e:
        print(f"Client {client_number} error: {e}")

if __name__ == "__main__":
    num_clients = 100  # Number of clients to run
    processes = []
    start_time = time.time()  # Record the start time

    for i in range(num_clients):
        try:
            process = subprocess.Popen(["python3", "client.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append(process)
            print(f"Started client {i + 1}")
        except Exception as e:
            print(f"Error starting client {i + 1}: {e}")
            break

    for i, process in enumerate(processes):
        process.wait()
        out, err = process.communicate()
        print(f"Client {i + 1} output:")
        print(out)
        print(err)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"All clients have completed. Elapsed time: {elapsed_time} seconds")
