import socket
import os


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        main_port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, main_port))  # This connects to the server.
            print(s.recv(1024).decode())  # Gets the "Connection made" message.
            print(s.recv(1024).decode())  # Gets the choice menu for PASV, PORT, etc

            # Port selection happens in this while True loop
            while True:
                response = input(">> ")  # I wanted this style since it reminds me of CMD
                response = response.split(" ")  # Splits up command, nice Python trick

                if response[0] == "PASV":
                    s.sendall("PASV".encode())  # Lets server know PASV was chosen
                    port = int(s.recv(1024).decode())  # Grabs the port from the server
                    print(s.recv(1024).decode())  # This gets the "230 OK"
                    break  # Breaks out of the loop

                elif response[0] == "PORT":
                    if len(response) != 2:  # Ensures that a port could be given.
                        print("Invalid format. Try Again.")
                    else:  # This means that at the very least a user did: PORT a
                        try:
                            port = int(response[1])  # Attempts to make the input to an int
                            if 1024 <= port <= 65535:  # If port is int, checks if it's in range
                                s.sendall("PORT".encode())  # Lets server know PORT was chosen
                                s.sendall(str(port).encode())  # Sends the selected PORT to server
                                print(s.recv(1024).decode())  # Gets back the 230 OK message
                                break
                            else:  # This is if given port is out of range
                                print("PORT out of range. Try again.")
                        except ValueError:  # ValueError occurs when typecasting a non-int to an int
                            print("Invalid value in second field. Try again.")  # This means the input wasn't an int

                elif response[0] == "CLOSE":
                    s.sendall("CLOSE".encode())  # Lets the server know the client is quitting
                    exit()  # Quits the client app.

                elif response[0] == "STOP":
                    s.sendall("STOP".encode())  # Sends stop command to server.
                    break  # This break is redundant, as the server would crash

            # FTP Server bit
            client_path = os.getcwd() + "\\Client"  # cwd path of client
            client_items = ["Client"]  # Rudimentary way of showing cwd

            server_items = ["Server"]  # Lets user know cwd of Server

            if not os.path.exists(client_path):  # Checks to see if 'Client' folder exists
                os.mkdir("Client")  # If the 'Client' folder doesn't exist, makes it

            # Initially prints the commands for the user
            print("                       COMMANDS                        \n"
                  "      CLIENT COMMANDS      |      SERVER COMMANDS      \n"
                  "-> CSHW: Like dir on cmd    -> SSHW: Like dir on cmd   \n"
                  "-> CUP: Like cd .. on cmd   -> SUP: Like cd .. on cmd  \n"
                  "-> CDWN: Like cd ## on cmd  -> SDWN: Like cd ## on cmd \n"
                  "-> PUT: File C->S           -> GET: File S->C          \n"
                  "-> HELP: Prints this out    -> QUIT: Quits...")
            while True:
                print("\nLocal CWD: " + '\\'.join(client_items) + "\nRemote CWD: " + '\\'.join(server_items))
                user_input = (input(">> ")).split()  # Cuts user input up.

                if len(user_input) != 1:  # Checks if additional items given
                    bonus_part = user_input[1]  # If additional info given, cuts it out

                command = user_input[0]  # This is the main command given
                s.sendall(command.encode())  # Lets server know the command

                print("")  # Spacer print()

                if command == "CSHW":
                    dirs = []
                    files = []
                    for item in os.listdir(client_path):
                        if os.path.isfile((client_path + f"\\{item}")):
                            files.append(item)
                        else:
                            dirs.append(item)

                    # These next lines prints out all directories present
                    print("Directories:")
                    temp_print = ''
                    i = 0
                    for item in dirs:
                        if i % 5 == 0 and i != 0:
                            temp_print += f"{item}\n"
                        elif i != (len(dirs) - 1):
                            temp_print += f"{item}, "
                        else:
                            temp_print += f"{item}"
                        i += 1
                    print(temp_print)
                    # Ends printing of directories

                    # These next lines prints out all files present
                    print("Files:")
                    temp_print = ''
                    i = 0
                    for item in files:
                        if i % 5 == 0 and i != 0:
                            temp_print += f"{item}\n"
                        elif i != (len(files) - 1):
                            temp_print += f"{item}, "
                        else:
                            temp_print += f"{item}"
                        i += 1
                    print(temp_print)
                    # Ends printing of files

                elif command == "CUP":
                    if len(client_items) == 1:  # This checks the 'cwd' of client
                        print("Can't go up any more!")  # If only 1 item, won't let it rise up
                    else:
                        client_items.pop()  # Removes last item in client items.

                        client_path = client_path.split("\\")  # Splits up the path so it can be edited
                        client_path.pop()  # Removes last item of path
                        client_path = '\\'.join(client_path)  # Rejoins the path

                elif command == "CDWN":
                    if len(user_input) != 2:  # Checks if additional arguments were given
                        print("Invalid Format. Try Again.")  # If no additional arguments, won't work
                    else:
                        if os.path.isdir(client_path + f"\\{bonus_part}"):  # Checks if directory exists
                            client_items.append(bonus_part)  # If so, adds it to 'cwd'
                            client_path += f"\\{bonus_part}"  # Also adds to path
                        else:
                            print("Not a directory. Try Again.")  # This is run, if the directory doesn't exist

                elif command == "SSHW":
                    print(s.recv(1024).decode())  # On client side, simply gets back what server sends and prints

                elif command == "SUP":
                    server_sup = s.recv(1024).decode()  # Server lets client know if it can go up
                    if server_sup == "CNGU":  # CNGU: Can not go up
                        print("ERROR: Can Not Go Up")  # Informs client that server can't go up
                    elif server_sup == "CGU":  # CGU: Can go up
                        server_items = (s.recv(1024).decode()).split("[-]")  # Gets back new server_items
                        s.sendall("OK".encode())  # Lets server know it's message was recieved

                elif command == "SDWN":
                    if len(user_input) != 2:  # Checks if additional arguments were given
                        print("Invalid format. Try again.")  # If no additional arguments, won't work
                    else:
                        s.sendall(bonus_part.encode())  # Sends directory to go down
                        code = s.recv(1024).decode()  # Gets back code from Server
                        if code == "DDE":  # If the DDE: Directory Does Exist
                            server_items = (s.recv(1024).decode()).split("[-]")  # Gets the server_items and updates it
                            s.sendall("OK".encode())  # Sends signal of "OK" to Server
                        elif code == "NAD":  # If it's NAD: Not A Directory
                            print("Not a directory!")  # Lets Client know requested directory isn't one

                elif command == "PUT":
                    if len(user_input) != 2:  # Checks if additional arguments were given.
                        print("Invalid format. Try Again.")  # If not, lets user know
                    else:
                        if os.path.isfile(client_path + f"\\{bonus_part}"):  # If file given is a file...
                            print(s.recv(1024).decode())  # Gets 210 OK message
                            s.sendall(f"{bonus_part}".encode())  # Sends the file to server to check for name duplicates
                            file_ok = s.recv(1024).decode()  # Gets server status
                            if file_ok == "OK" or file_ok == "DUPE":  # file_ok from Server is OK or DUPE
                                if file_ok == "OK":
                                    print("File is OK, continuing")
                                elif file_ok == "DUPE":
                                    dupe_name = s.recv(1024).decode()  # Gets back new name
                                    print("File already exists, new name: " + dupe_name)  # Informs user of new filename
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:  # Opens up data connection
                                    d.connect((host, port))  # Connects with new port
                                    file_path = client_path + f"\\{bonus_part}"  # Makes file path
                                    with open(file_path) as f:  # Opens up the file
                                        contents = f.readlines()  # Reads contents
                                    contents.append('>>FILE ENDED<<')  # Adds end piece
                                    d.sendall(str(len(contents)).encode())  # Sends the length of contents
                                    for line in contents:  # For each line...
                                        d.sendall(line.encode())  # ... sends the info
                                        d.recv(1024).decode()  # ... gets the OK
                                    d.close()  # Closes data communication
                            else:  # Lets user know file_ok isn't OK or DUPE
                                print("Something went wrong.")
                        else:
                            s.sendall("NAVF")  # Lets server know it's not a valid file that was sent
                            print("Not a valid file.")

                elif command == "GET":
                    if len(user_input) != 2:  # Checks if additional arguments were given
                        print("Invalid format. Try Again.")  # If not given, lets user know
                    else:
                        s.sendall(bonus_part.encode())  # Sends file to GET to server
                        exists = s.recv(1024).decode()  # Server lets Client know if file exists
                        print(exists)
                        if exists == "404 Bad Request":  # File doesn't exist
                            print("File doesn't exist on server path. Try Again.")
                        elif exists == "220 OK":  # File does exist
                            if os.path.isfile(client_path + f"\\{bonus_part}"):  # Checks if file with that name exists
                                bonus_part = bonus_part.split('.')  # Splits up file name

                                # Handles coming up with new name for file
                                i = 1
                                while True:
                                    temp_name = '.'.join(bonus_part)
                                    if not os.path.isfile(client_path + f"\\{temp_name}"):
                                        break
                                    bonus_part[-2] += str(i)
                                    i += 1
                                bonus_part = '.'.join(bonus_part)
                                print(f"File exists locally, renaming new file to: {bonus_part}")  # File does exist

                            s.sendall("READY".encode())  # If filename is dupe or not, will be ready now
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:  # Opens data communication
                                d.connect((host, port))  # Connects to server
                                times = int(d.recv(1024).decode())  # Gets number of times from Server
                                text_lines = []  # Creates text_lines list
                                for i in range(times):  # Runs for number of lines
                                    data = d.recv(1024).decode()  # Decodes Server Line
                                    if data != ">>FiLE ENDED<<":  # If info is not end-line...
                                        text_lines.append(data)  # ... Append to text_lines
                                        d.sendall("OK".encode())  # ... Send the OK to server
                                    elif data == ">>FILE ENDED<<":  # If line is end-line
                                        d.sendall("DONE".encode())  # Let server know Client is done
                                        break  # Stops the number of lines
                                    else:
                                        print("???")  # How did you get here
                                with open((client_path + "\\" + bonus_part), 'w') as f:  # Opens up the file
                                    for line in text_lines:  # For each line...
                                        f.write(line)  # Adds it to text file
                                d.close()  # Closes data connection
                                print("CONN CLOSED")

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
