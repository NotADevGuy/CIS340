import socket
import random
import os


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            print(f"Connection to {addr[0]} on port #{addr[1]}")
            conn.sendall("Connection made to FTP Server!".encode())

            conn.sendall("\nWould you like:\n"
                         "\t1. Active (Server Chooses) PASV\n"
                         "\t2. Passive (Client Chooses) PORT ######\n"
                         "\t3. Close Client\n"
                         "\t4. Stop Server".encode())
            connType = int(conn.recv(1024).decode())

            if connType == 1:
                port = random.randint(1024, 65535)
                conn.sendall(str(port).encode())
                conn.sendall("230 OK".encode())
            elif connType == 2:
                conn.sendall("Enter desired port: ".encode())
                port = int(conn.recv(1024).decode())
                conn.sendall("230 OK".encode())
            elif connType == 4:
                exit()

            client = conn.recv(1024).decode()
            clientPrint = ["Client"]

            server = os.getcwd() + "\\Server"
            conn.sendall(server.encode())
            serverPrint = ["Server"]
            conn.sendall('[-]'.join(serverPrint).encode())
            testPiece = "\\"

            while True:
                response = conn.recv(1024).decode()
                print(response)

                if response == "SSHOW":
                    toSend = ""
                    test = os.listdir(server)
                    dirs = []
                    files = []
                    for item in test:
                        itemPath = server + f"\\{item}"
                        if os.path.isfile(itemPath):
                            files.append(item)
                        else:
                            dirs.append(item)
                    toSend += "Directories:\n"
                    toPrint = ''
                    for i in range(len(dirs)):
                        if i % 5 == 0 and i != 0:
                            toPrint += f"{dirs[i]}\n"
                        elif i != (len(dirs) - 1):
                            toPrint += f"{dirs[i]}, "
                        else:
                            toPrint += f"{dirs[i]}"
                        i += 1
                    toSend += toPrint
                    toSend += "\nFiles:\n"
                    toPrint = ''
                    for i in range(len(files)):
                        if i % 5 == 0 and i != 0:
                            toPrint += f"{files[i]}\n"
                        elif i != (len(files) - 1):
                            toPrint += f"{files[i]}, "
                        else:
                            toPrint += f"{files[i]}"
                        i += 1
                    toSend += toPrint
                    conn.sendall(toSend.encode())
                elif response == "SUP":
                    if len(serverPrint) == 1:
                        conn.sendall("123".encode())
                    else:
                        conn.sendall("321".encode())
                        serverPrint.pop()
                        server = server.split("\\")
                        server.pop()
                        server = '\\'.join(server)
                        conn.sendall('[-]'.join(serverPrint).encode())
                        print(conn.recv(1024).decode())
                        conn.sendall(server.encode())
                elif response == "SDOWN":
                    toTravel = conn.recv(1024).decode()
                    if os.path.isdir(server + f"\\{toTravel}"):
                        conn.sendall("123".encode())
                        serverPrint.append(toTravel)
                        server += f"\\{toTravel}"
                        conn.sendall('[-]'.join(serverPrint).encode())
                        print(conn.recv(1024).decode())
                        conn.sendall(server.encode())
                    else:
                        conn.sendall("Not a directory!".encode())
                elif response == "PUT":
                    pass
                elif response == "GET":
                    pass
                elif response == "QUIT":
                    exit()





if __name__ == "__main__":
    s = Server()
    s.main()
