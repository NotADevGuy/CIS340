import socket
import os
# TODO CREATE CLIENT FOLDER IF NOT PRESENT
# TODO WHAT IF FILE ALREADY EXISTS IN PUT/GET

class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        main_port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, main_port))
            print(s.recv(1024).decode())
            print(s.recv(1024).decode())
            while True:
                response = input(">> ")
                response = response.split(" ")

                if response[0] == "PASV":
                    s.sendall("PASV".encode())  # Lets server know PASV was chosen
                    port = int(s.recv(1024).decode())  # Grabs the port from the server
                    print(s.recv(1024).decode())  # This gets the "230 OK"
                    break
                elif response[0] == "PORT":
                    if len(response) != 2:
                        print("Too many or too little values given. Try again.")
                    else:
                        try:
                            port = int(response[1])
                            if 1024 <= port <= 65535:
                                s.sendall("PORT".encode())
                                s.sendall(str(port).encode())
                                print(s.recv(1024).decode())
                                break
                            else:
                                print("PORT out of range. Try again.")
                        except ValueError:
                            print("Invalid value in second field. Try again.")
                elif response[0] == "CLOSE":
                    s.sendall("CLOSE".encode())
                    exit()
                elif response[0] == "STOP":
                    s.sendall("STOP".encode())
                    break

            # --------------------------------------------------------- #
            #  Done with port selection, now for fun stuff.             #
            # --------------------------------------------------------- #

            client_path = os.getcwd() + "\\Client"
            # s.sendall(client_path.encode())
            client_items = ["Client"]

            # server_path = s.recv(1024).decode()
            server_items = ["Server"]

            forward_slash = "\\"

            print("                       COMMANDS                        \n"
                  "      CLIENT COMMANDS      |      SERVER COMMANDS      \n"
                  "-> CSHW: Like dir on cmd    -> SSHW: Like dir on cmd   \n"
                  "-> CUP: Like cd .. on cmd   -> SUP: Like cd .. on cmd  \n"
                  "-> CDWN: Like cd ## on cmd  -> SDWN: Like cd ## on cmd \n"
                  "-> PUT: File C->S           -> GET: File S->C          \n"
                  "-> HELP: Prints this out    -> QUIT: Quits...")
            while True:
                print(f"\nLocal CWD: {forward_slash.join(client_items)}\nRemote CWD: {forward_slash.join(server_items)}")
                user_input = (input(">> ")).split()
                if len(user_input) == 1:
                    pass
                else:
                    bonus_part = user_input[1]
                command = user_input[0]
                s.sendall(command.encode())
                print("")

                if command == "CSHW":
                    dirs = []
                    files = []
                    for item in os.listdir(client_path):
                        if os.path.isfile((client_path + f"\\{item}")):
                            files.append(item)
                        else:
                            dirs.append(item)

                    print("Directories:")
                    temp_print = ''
                    for i in range(len(dirs)):
                        if i % 5 == 0 and i != 0:
                            temp_print += f"{dirs[i]}\n"
                        elif i != (len(dirs) - 1):
                            temp_print += f"{dirs[i]}, "
                        else:
                            temp_print += f"{dirs[i]}"
                        i += 1
                    print(temp_print)

                    print("Files:")
                    temp_print = ''
                    for i in range(len(files)):
                        if i % 5 == 0 and i != 0:
                            temp_print += f"{files[i]}\n"
                        elif i != (len(files) - 1):
                            temp_print += f"{files[i]}, "
                        else:
                            temp_print += f"{files[i]}"
                        i += 1
                    print(temp_print)

                elif command == "CUP":
                    if len(client_items) == 1:
                        print("Can't go up any more!")
                    else:
                        client_items.pop()
                        client_path = client_path.split("\\")
                        client_path.pop()
                        client_path = '\\'.join(client_path)

                elif command == "CDWN":
                    if len(user_input) != 2:
                        print("Invalid Format. Try Again.")
                    else:
                        if os.path.isdir(client_path + f"\\{bonus_part}"):
                            client_items.append(bonus_part)
                            client_path += f"\\{bonus_part}"
                        else:
                            print("Not a directory. Try Again.")

                elif command == "SSHW":
                    print(s.recv(1024).decode())

                elif command == "SUP":
                    fromServer = s.recv(1024).decode()
                    if fromServer == "CGUAM":
                        print("ERROR: Can't go up any more.")
                    elif fromServer == "CGU":
                        server_items = (s.recv(1024).decode()).split("[-]")
                        s.sendall("OK".encode())
                        server_path = s.recv(1024).decode()

                elif command == "SDWN":
                    if len(user_input) != 2:
                        print("Invalid format. Try again.")
                    else:
                        s.sendall(bonus_part.encode())
                        code = s.recv(1024).decode()
                    if code == "CTD":
                        server_items = (s.recv(1024).decode()).split("[-]")
                        s.sendall("OK".encode())
                        server_path = s.recv(1024).decode()
                    elif code == "NAD":
                        print("Not a directory1")

                elif command == "PUT":
                    if len(user_input) != 2:
                        print("Invalid format. Try Again.")
                    else:
                        if os.path.isfile(client_path + f"\\{bonus_part}"):
                            s.sendall(f"{bonus_part}".encode())
                            file_ok = s.recv(1024).decode()
                            if file_ok == "OK" or file_ok == "DUPE":
                                if file_ok == "OK":
                                    print("YAY")
                                elif file_ok == "DUPE":
                                    dupe_name = s.recv(1024).decode()
                                    print("File already exists, new name: " + dupe_name)
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
                                    d.connect((host, port))
                                    file_path = client_path + f"\\{bonus_part}"
                                    with open(file_path) as f:
                                        contents = f.readlines()
                                    contents.append('>>FILE ENDED<<')
                                    d.sendall(str(len(contents)).encode())
                                    for line in contents:
                                        d.sendall(line.encode())
                                        # print("transferred some.")
                                        d.recv(1024).decode()
                                    d.close()
                            else:
                                print("Something went wrong.")
                        else:
                            s.sendall("NAVF")
                            print("Not a valid file.")

                elif command == "GET":
                    if len(user_input) != 2:
                        print("Invalid format. Try Again.")
                    else:
                        s.sendall(bonus_part.encode())
                        exists = s.recv(1024).decode()
                        if exists == "NO":
                            print("File doesn't exist on server path. Try Again.")
                        elif exists == "OK":
                            if os.path.isfile(client_path + f"\\{bonus_part}"):
                                print("File exists locally, renaming new file to: ")
                                bonus_part = bonus_part.split('.')
                                i = 1
                                while True:
                                    temp_name = '.'.join(bonus_part)
                                    if not os.path.isfile(client_path + f"\\{temp_name}"):
                                        break
                                    bonus_part[-2] += str(i)
                                    i += 1
                                bonus_part = '.'.join(bonus_part)
                            s.sendall("READY".encode())
                            # s.sendall(bonus_part.encode())

                elif command == "QUIT":
                    s.close()
                    exit()

                elif command == "HELP":
                    print("                       COMMANDS                        \n"
                          "      CLIENT COMMANDS      |      SERVER COMMANDS      \n"
                          "-> CSHW: Like dir on cmd    -> SSHW: Like dir on cmd   \n"
                          "-> CUP: Like cd .. on cmd   -> SUP: Like cd .. on cmd  \n"
                          "-> CDWN: Like cd ## on cmd  -> SDWN: Like cd ## on cmd \n"
                          "-> PUT: File C->S           -> GET: File S->C          \n"
                          "-> HELP: Prints this out    -> QUIT: Quits...")

                else:
                    print("Unrecognized Command...")


if __name__ == '__main__':
    c = Client()
    c.main()
