# Memcached-lite
This Python server is designed to provide a simple key-value store over a network using the TCP protocol. It allows clients to perform two main operations: SET and GET. The server can handle multiple concurrent client connections and persists data to a file for durability.

## Architecture -

### Components:

**- Socket Server (server_socket):** Responsible for establishing and managing network connections with clients. This function creates a socket with the AF_INET (IPv4) address and SOCK_STREAM socket type binding the socket to ‘localhost’ and port 9889. Moreover, we have maximum number of incoming client connections = 5 using ```server_socket.listen(5)```. The ```server_socket.accept()``` accepts the incoming clients and spawns a new thread to handle client requests.

**- Client Handler Threads:** These handle individual client connections concurrently. Each client connection triggers creation of new thread using threading.Thread() which runs the handle_client() function and manages the interaction.

**- Data Dictionary (current_dic):** The data dictionary serves as in-memory key-value store that holds the server’s current data. The purpose of its creation is discussed below.

**- File Persistence (data.txt):** This serves as persistent storage mechanism to ensure data durability. This lets data persistence and access even after the server dies through accessing this file.


### Design:

- Initially a dictionary is created which stores the keys and values in memory when the server runs. The purpose of creating this dictionary is to quickly access and manipulate data for SET and GET operations. When a SET operation is performed, the dictionary is updated with the new key-value pair. The dictionary is also used for responding to GET requests by looking up values based on keys. By having a dictionary to do these operations we can improve the GET and SET operations efficiency by directly looing up values in O(1) rather than reading the file every time to search for the key and get their corresponding values which would take O(n). Thus, this is the first step with respect to the design process which helps us to improve the efficiency.

- The ```read_previous_state()``` function populates the dictionary every time the server stars with the previously populated values in the data.txt (if any). This is done so that during that specific runtime, the dictionary is updated/populated with the latest values which exist in the file (maybe from previous run sessions).

- Now ```write_current_state()``` function opens the file_path and writes/appends the key values as they are generated from client to the data file.

- The ```set_operation()``` function is responsible for performing SET operations to set/update the key-value pairs in the server’s data dictionary (current_dic) as well as persist this change to the file
(data.txt). It helps achieve and maintain data consistency by ensuring that both in-memory and persistent data are updated synchronously, and this function also handles the data durability aspect as the data is written to the file ensuring that there is no information loss in the event of server crash.

- The get_operation() function handles the GET operations for retrieving data from server’s in-memory data store. The response generation as requested in the assignment is followed, i.e., when the requested key is found, the function constructs in the form ```VALUE {key} {size}\r\n{data}\r\n``` which includes the key, size of the data and the actual data content in the next line.

- Finally the handle_client() function is implemented which serves as the core for manging client-server interactions. Upon accepting a client connection, it obtains the address and logs the connection, receives the client commands, and parses them accordingly for the SET or GET command. Moreover, we also add a simulated delay between each SET and GET operation by randomizing between (0,2) for SET and (0,1) for GET operations. Accordingly, basic exceptions are handled here.


### Some run examples -

<img width="840" alt="image" src="https://github.com/prashulk/Memcached-lite/assets/67316162/076b8f6a-c074-408a-9c51-eb7489d04713">


<img width="805" alt="image" src="https://github.com/prashulk/Memcached-lite/assets/67316162/ab7a4ed1-4042-4611-8116-2931a8d57ab3">


- Below image showing thread limit -
<img width="835" alt="image" src="https://github.com/prashulk/Memcached-lite/assets/67316162/76ecdef4-0ce9-4576-a391-24ee6c83a6ed">


### Limitations of server-

**- Limited Concurrency Handling –** Server would be limited in the number of concurrent clients it can handle. Each new client connection is handled by creating a new thread, which consumes system resources. Hence due to system’s limitations, the server’s ability to handle large number of concurrent clients will be impacted.

**- Resource Contentions –** When many threads compete for CPU time and other resources simultaneously, there is no controlling mechanism implemented as of now for the number of active threads.

**- Data Storage –** The server stores data in memory, which has limitations on the maximum amount of data it can hold.

**- Threadlock -** Although its necessary to implement Mutex to prevent race conditions and provide consistent results, but this is a trade-off that we have to take into account as the server may be impacted when handling high volume of SET requests.

**- Error handling –** I have implemented a basic set of error handling for some of the most common issues/test-cases which I could think of, but it does not cover all possible error scenarios, such as disk space issues, network failures, etc.


### Future Improvements –

**- Error Handling:** Define the cases to handle exits more gracefully for different types of errors.

**- Implement threadpool:** Implementing a threadpool can enhance the server’s scalability by efficiently managing threads and backlog, thereby ensuring a smoother experience for clients.
