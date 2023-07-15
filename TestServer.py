import socket
import threading
import telnetlib
import time

class TelnetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(f"Telnet server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            tn = telnetlib.Telnet()
            tn.sock = client_socket

            if self.port == 1200:
                tn.write(b"Welcome to the Telnet server!\r\n")
                tn.write(b"Enter 'exit' to quit.\r\n")
                tn.write(b"-> ")
                while True:
                    received_data = tn.read_until(b"\n").decode("utf-8")
                    received_data = received_data.strip()
                    print(f"Received on {self.port}: {received_data}")

                    if received_data.lower() == "exit":
                        tn.write(b"Goodbye!\r\n")
                        break

                    tn.write(f"You said on {self.port}: {received_data}\r\n".encode("utf-8"))
                    tn.write(b"-> ")


            elif self.port == 1201:
                tn.write(b"Welcome to the Linux server simulation!\r\n")
                tn.write(b"Supported commands: cd, pwd, ls, cp\r\n")
                tn.write(b"-> ")
                while True:
                    received_data = tn.read_until(b"\n").decode("utf-8")
                    received_data = received_data.strip()
                    print(f"Received on {self.port}: {received_data}")
                    if received_data.lower() == "exit":
                        tn.write(b"Goodbye!\r\n")
                        break
                    elif received_data.lower() == "cd":
                        tn.write(b"Changed directory\r\n")
                    elif received_data.lower() == "pwd":
                        tn.write(b"/home/user/\r\n")
                    elif received_data.lower() == "ls":
                        tn.write(b"file1.txt\r\nfile2.txt\r\nfile3.txt\r\n")
                    elif received_data.lower().startswith("cp"):
                        file_name = received_data[3:].strip()
                        tn.write(f"Copy file '{file_name}'? (y/n)\r\n".encode("utf-8"))
                        confirmation = tn.read_until(b"\n").decode("utf-8").strip()
                        if confirmation.lower() == "y":
                            tn.write(f"File '{file_name}' copied!\r\n".encode("utf-8"))
                        else:
                            tn.write(f"Copy operation canceled.\r\n".encode("utf-8"))
                    tn.write(b"-> ")

            elif self.port == 1202 or self.port == 1203:
                tn.write(b"Welcome to the SFTP server simulation!\r\n")
                tn.write(b"Supported commands: get, put\r\n")
                tn.write(b"-> ")
                while True:
                    received_data = tn.read_until(b"\n").decode("utf-8")
                    received_data = received_data.strip()
                    print(f"Received on {self.port}: {received_data}")

                    if received_data.lower() == "exit":
                        tn.write(b"Goodbye!\r\n")
                        break
                    elif received_data.lower() == "get":
                        tn.write(b"File sent from SFTP server\r\n")
                    elif received_data.lower() == "put":
                        tn.write(b"File received by SFTP server\r\n")
                    tn.write(b"-> ")

            elif self.port == 1204:
                tn.write(b"Welcome to the Upgrade server simulation!\r\n")
                tn.write(b"Supported command: update\r\n")
                tn.write(b"-> ")

                while True:
                    received_data = tn.read_until(b"\n").decode("utf-8")
                    received_data = received_data.strip()
                    print(f"Received on {self.port}: {received_data}")
                    if received_data.lower() == "update":
                        tn.write(b"Updating...")
                        for i in range(11):
                            time.sleep(1)
                            tn.write(f"Progress: {i * 10}%\r\n".encode("utf-8"))

                        tn.write(b"Update success!\r\n")
                    tn.write(b"-> ")

        except Exception as e:
            print(f"Exception occurred: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    servers = [
        TelnetServer("localhost", 1200),
        TelnetServer("localhost", 1201),
        TelnetServer("localhost", 1202),
        TelnetServer("localhost", 1203),
        TelnetServer("localhost", 1204)
    ]

    threads = []
    for server in servers:
        thread = threading.Thread(target=server.start)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
