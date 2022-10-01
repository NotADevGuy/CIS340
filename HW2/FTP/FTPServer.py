import socket
import random
import os
# TODO CREATE SERVER FOLDER IF NOT PRESENT


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        main_port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # These lines bind the server to the address, and allows a connection...
            s.bind((host, main_port))
            s.listen()

            # ... And once a connection is found it is accepted
            conn, addr = s.accept()

            # Next line lets server know what IP connected and on which PORT.
            print(f"Connection to {addr[0]} on port #{addr[1]}")

            # This lets the client know that there has been a connection made, and provides a menu.
            conn.sendall("Connection made to FTP Server!".encode())
            conn.sendall("PASV, PORT, CLOSE (client), STOP (server)".encode())

            connType = conn.recv(1024).decode()

            if connType == "PASV":
                port = random.randint(1024, 65535)
                conn.sendall(str(port).encode())
                conn.sendall("230 OK".encode())
            elif connType == "PORT":
                port = int(conn.recv(1024).decode())
                print(port)
                conn.sendall("230 OK".encode())
            elif connType == "CLOSE":
                print(f"Connection to {addr[0]} lost.")
            elif connType == "STOP":
                exit()

            # client = conn.recv(1024).decode()
            # clientPrint = ["Client"]

            server_path = os.getcwd() + "\\Server"
            # conn.sendall(server_path.encode())
            server_items = ["Server"]

            while True:
                command = conn.recv(1024).decode()
                print(command)

                if command == "SSHW":
                    to_send = ""
                    dirs = []
                    files = []
                    for item in os.listdir(server_path):
                        if os.path.isfile(server_path + f"\\{item}"):
                            files.append(item)
                        else:
                            dirs.append(item)

                    to_send += "Directories:\n"
                    to_add = ''
                    for i in range(len(dirs)):
                        if i % 5 == 0 and i != 0:
                            to_add += f"{dirs[i]}\n"
                        elif i != (len(dirs) - 1):
                            to_add += f"{dirs[i]}, "
                        else:
                            to_add += f"{dirs[i]}"
                        i += 1
                    to_send += to_add
                    to_send += "\nFiles:\n"
                    to_add = ''
                    for i in range(len(files)):
                        if i % 5 == 0 and i != 0:
                            to_add += f"{files[i]}\n"
                        elif i != (len(files) - 1):
                            to_add += f"{files[i]}, "
                        else:
                            to_add += f"{files[i]}"
                        i += 1
                    to_send += to_add
                    conn.sendall(to_send.encode())

                elif command == "SUP":
                    if len(server_items) == 1:
                        conn.sendall("CGUAM".encode())
                    else:
                        conn.sendall("CGU".encode())
                        server_items.pop()
                        server_path = server_path.split("\\")
                        server_path.pop()
                        server_path = '\\'.join(server_path)
                        conn.sendall('[-]'.join(server_items).encode())
                        print(conn.recv(1024).decode())
                        conn.sendall(server_path.encode())

                elif command == "SDWN":
                    to_travel = conn.recv(1024).decode()
                    if os.path.isdir(server_path + f"\\{to_travel}"):
                        conn.sendall("CTD".encode())
                        server_items.append(to_travel)
                        server_path += f"\\{to_travel}"
                        conn.sendall('[-]'.join(server_items).encode())
                        print(conn.recv(1024).decode())
                        conn.sendall(server_path.encode())
                    else:
                        conn.sendall("NAD".encode())

                elif command == "PUT":
                    file_name = conn.recv(1024).decode()
                    if os.path.isfile(server_path + f"\\{file_name}"):
                        conn.sendall("DUPE".encode())
                        file_name = file_name.split(".")
                        i = 1
                        temp_name = ''
                        while True:
                            temp_name = '.'.join(file_name)
                            if not os.path.isfile(server_path + f"\\{temp_name}"):
                                break
                            file_name[-2] += str(i)
                            i += 1
                        file_name = '.'.join(file_name)
                        conn.sendall(file_name.encode())
                    else:
                        conn.sendall("OK".encode())

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
                        d.bind((host, port))
                        d.listen()
                        conn, addr = d.accept()
                        text_lines = []
                        while True:
                            data = conn.recv(1024).decode()
                            if data != ">>FILE ENDED<<":
                                text_lines.append(data)
                                conn.sendall("OK".encode())
                            elif data == ">>FILE ENDED<<":
                                conn.sendall("DONE".encode())
                                break
                            else:
                                print("???")
                        print(text_lines)
                        # Can use file_name and the server_path
                        # with write file thing


                    # This is where the file will be prepared to send.
                    # Also check if a file by that name exists already

                elif command == "GET":
                    pass

                elif command == "QUIT":
                    exit()





if __name__ == "__main__":
    s = Server()
    s.main()
