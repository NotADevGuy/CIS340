import socket
import os


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(s.recv(1024).decode())
            print(s.recv(1024).decode())
            response = 1  # Todo change this back
            while response not in [1, 2, 3, 4]:
                response = input("Choice: ")
                try:
                    response = int(response)
                except:
                    response = 5
            response = str(response)
            s.sendall(response.encode())
            response = int(response)

            # This is if Active Connection is chosen. (Server Chooses)
            if response == 1:
                # This next line gets the data port number the server chose
                port = int(s.recv(1024).decode())

                # This next line gets the "230 OK" message
                print(s.recv(1024).decode())

            # This is if Passive Connection is chosen. (Client Chooses)
            # TODO Check if user chooses port or client program
            elif response == 2:
                # This next line gets the "Enter desired port: " text
                print(s.recv(1024).decode())

                # True loop to ensure a valid port is chosen.
                while True:
                    port = input("Port Choice (1024 - 65535): ")
                    try:
                        port = int(port)  # Checks if input is int
                        if 1024 <= port <= 65535:  # Checks if input is in valid range
                            break  # Gets out of the while loop, since qualifications are met
                    except ValueError:  # ValueError be caused from trying to typecast to int a str.
                        pass  # Nothing needs to go here. Could tell user what was wrong, but not needed.

                # This sends the port choice to the server
                s.sendall(str(port).encode())

                # This next line gets the "230 OK" message
                print(s.recv(1024).decode())

            # This is in the case the client wants to close FTP Client
            elif response == 3:
                exit()

            print("\n\n\n")
            response = ''
            client = os.getcwd() + "\\Client"
            s.sendall(client.encode())
            clientPrint = ["Client"]

            server = s.recv(1024).decode()
            serverPrint = (s.recv(1024).decode()).split("[-]")


            testPiece = "\\"
            while True:
                print("\nCOMMANDS:\n"
                      "--> CSHOW: Contents of client cwd  --> SSHOW: Contents of server cwd\n"
                      "--> CUP: like cd .. on client      --> SUP: like cd .. on server    \n"
                      "--> CDOWN: like cd ### on client   --> SDOWN: like cd ### on server \n"
                      "--> PUT: File (client -> server)   --> GET: File (server -> client) \n"
                      "--> QUIT: Quit")
                print(f"Local CWD: {testPiece.join(clientPrint)}\nRemote CWD: {testPiece.join(serverPrint)}")
                response = input("> ")
                s.sendall(response.encode())
                print("\n")
                if response == "CSHOW":
                    test = os.listdir(client)
                    dirs = []
                    files = []
                    for item in test:
                        itemPath = client + f"\\{item}"
                        if os.path.isfile(itemPath):
                            files.append(item)
                        else:
                            dirs.append(item)
                    print("Directories:")
                    toPrint = ''
                    for i in range(len(dirs)):
                        if i % 5 == 0 and i != 0:
                            toPrint += f"{dirs[i]}\n"
                        elif i != (len(dirs) - 1):
                            toPrint += f"{dirs[i]}, "
                        else:
                            toPrint += f"{dirs[i]}"
                        i += 1
                    print(toPrint)
                    print("Files:")
                    toPrint = ''
                    for i in range(len(files)):
                        if i % 5 == 0 and i != 0:
                            toPrint += f"{files[i]}\n"
                        elif i != (len(files) - 1):
                            toPrint += f"{files[i]}, "
                        else:
                            toPrint += f"{files[i]}"
                        i += 1
                    print(toPrint)
                elif response == "CUP":
                    if len(clientPrint) == 1:
                        print("Can't go up any more!")
                    else:
                        clientPrint.pop()
                        client = client.split("\\")
                        client.pop()
                        client = '\\'.join(client)
                        print(clientPrint)
                        print(client)
                elif response == "CDOWN":
                    response = input("What directory to travel down to?")
                    if os.path.isdir(client + f"\\{response}"):
                        clientPrint.append(response)
                        client += f"\\{response}"
                    else:
                        print("Not a directory!")
                elif response == "SSHOW":
                    print(s.recv(1024).decode())
                elif response == "SUP":
                    fromServer = s.recv(1024).decode()
                    if fromServer == "123":
                        print("Can't go up any more!")
                    elif fromServer == "321":
                        serverPrint = (s.recv(1024).decode()).split("[-]")
                        s.sendall("OK".encode())
                        server = s.recv(1024).decode()
                elif response == "SDOWN":
                    toSend = input("What directory to travel down to?")
                    s.sendall(toSend.encode())
                    code = s.recv(1024).decode()
                    if code == "123":
                        serverPrint = (s.recv(1024).decode()).split("[-]")
                        s.sendall("OK".encode())
                        server = s.recv(1024).decode()
                    else:
                        print(code)
                elif response == "PUT":
                    pass
                elif response == "GET":
                    pass
                elif response == "QUIT":
                    exit()
            s.close()


if __name__ == '__main__':
    c = Client()
    c.main()
