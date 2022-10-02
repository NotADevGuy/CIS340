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
            s.bind((host, main_port))  # Binds the server to the address
            s.listen()  # Allows for searching of a client

            conn, addr = s.accept()

            # Next line lets server know what IP connected and on which PORT.
            print(f"Connection to {addr[0]} on port #{addr[1]}")

            # This lets the client know that there has been a connection made, and provides a menu.
            conn.sendall("Connection made to FTP Server!".encode())
            conn.sendall("PASV, PORT, CLOSE (client), STOP (server)".encode())

            connection_type = conn.recv(1024).decode()  # Once client has valid input, goes to server

            if connection_type == "PASV":
                port = random.randint(1024, 65535)  # Server chooses port
                conn.sendall(str(port).encode())  # Sends back chosen port

            elif connection_type == "PORT":
                port = int(conn.recv(1024).decode())  # This line lets the server save the client's selected port

            elif connection_type == "CLOSE":
                print(f"Connection to {addr[0]} lost.")  # This was for debugging, lets server know client is done

            elif connection_type == "STOP":
                exit()  # Crude way of stopping the server

            # FTP Server bit
            conn.sendall("230 OK".encode())  # This is the sending of the 230 OK message

            server_path = os.getcwd() + "\\Server"  # cwd path of server
            server_items = ["Server"]  # Rudimentary way of showing cwd

            if not os.path.exists(server_path):  # Checks to see if 'Server' folder exists
                os.mkdir("Server")  # If the 'Server' folder doesn't exist, makes it

            while True:
                command = conn.recv(1024).decode()  # This is the command the client ran

                if command == "SSHW":
                    to_send = ""  # One large str to send

                    dirs = []
                    files = []
                    for item in os.listdir(server_path):
                        if os.path.isfile(server_path + f"\\{item}"):  # Checks if item is file or directory
                            files.append(item)  # If file, adds it to files list
                        else:
                            dirs.append(item)  # If not file, adds it to directory list

                    # These next lines adds Directory info to to_send
                    to_send += "Directories:\n"
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
                    to_send += temp_print
                    # Ends adding of directories to to_send

                    # These next lines adds File info to to_send
                    to_send += "\nFiles:\n"
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
                    to_send += temp_print
                    # Ends adding of files to to_send

                    conn.sendall(to_send.encode())  # Sends the client to_send

                elif command == "SUP":
                    if len(server_items) == 1:  # This checks the 'cwd' of server
                        conn.sendall("CNGU".encode())  # If only 1 item, won't rise, sends code to Client informing it
                    else:
                        conn.sendall("CGU".encode())  # If more than 1 item, can rise. Lets client know
                        server_items.pop()  # Removes last item

                        server_path = server_path.split("\\")  # Splits up path so it can be edited
                        server_path.pop()  # Removes last item of path
                        server_path = '\\'.join(server_path)  # Rejoins the path
                        conn.sendall('[-]'.join(server_items).encode())  # Sends the server_items to Client
                        print(conn.recv(1024).decode())  # Gets the OK from Client

                elif command == "SDWN":
                    to_travel = conn.recv(1024).decode()  # Gets the directory from Client

                    if os.path.isdir(server_path + f"\\{to_travel}"):  # Sees if directory exists
                        conn.sendall("DDE".encode())  # Lets Client know DDE: Directory does exist

                        server_items.append(to_travel)  # Items are appended to
                        server_path += f"\\{to_travel}"  # server_path is updated
                        conn.sendall('[-]'.join(server_items).encode())  # server_items is prepped to send, and is sent
                        print(conn.recv(1024).decode())  # Gets back OK signal from Client
                    else:
                        conn.sendall("NAD".encode())  # Lets Client know NAD: Not A Directory

                elif command == "PUT":
                    file_name = conn.recv(1024).decode()  # Gets filename from Client
                    if os.path.isfile(server_path + f"\\{file_name}"):  # Checks if file exists
                        conn.sendall("DUPE".encode())  # If so, lets Client know it's a dupe
                        file_name = file_name.split(".")  # Splits filename
                        i = 1  # Integers used to make unique filenames

                        # This loop handles renaming
                        while True:
                            temp_name = '.'.join(file_name)  # Splits up file_name
                            if not os.path.isfile(server_path + f"\\{temp_name}"):  # Checks if file_name exists
                                break  # Unique filename made
                            file_name[-2] += str(i)  # Appends int to file_name
                            i += 1  # i++ : )
                        file_name = '.'.join(file_name)  # Joins back file_name
                        conn.sendall(file_name.encode())  # Sends dupe filename
                    else:
                        conn.sendall("OK".encode())  # Just Lets Client know no duplicate exists

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:  # Opens data connection
                        print("Connection for data transfer made")
                        d.bind((host, port))  # binds server to new connection
                        d.listen()  # Listens for client
                        dataConn, dataAddr = d.accept()  # Accepts client
                        text_lines = []  # Lines of file list
                        times = int(dataConn.recv(1024).decode())  # Gets number of lines exists

                        for i in range(times):
                            data = dataConn.recv(1024).decode()  # Gets line
                            if data != ">>FILE ENDED<<":  # If not the end-line...
                                text_lines.append(data)  # Appends to text_lines
                                dataConn.sendall("OK".encode())  # Lets Client know to continue
                            elif data == ">>FILE ENDED<<":  # If end-line...
                                dataConn.sendall("DONE".encode())  # Let Client know it's done
                                break  # BE FREE LOOP
                            else:
                                print("???")  # How did the error get here?
                        with open((server_path + "\\" + file_name), 'w') as f:  # Makes the new file
                            for line in text_lines:  # For each file
                                f.write(line)  # Writes it!
                        dataConn.close()  # Closes data connection
                        print("CONN CLOSED")  # DEBUG for Server

                elif command == "GET":
                    file_to_return = conn.recv(1024).decode()  # Gets file from Client
                    if os.path.isfile(server_path + f"\\{file_to_return}"):  # Checks if file exists
                        conn.sendall("OK".encode())  # If it does, send OK
                    else:
                        conn.sendall("NO".encode())  # If not, send NO
                    if conn.recv(1024).decode() == "READY":
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:  # Open data connection
                            d.bind((host, port))  # Binds Server to address and port
                            d.listen()  # Listens for client
                            dataConn, dataAddr = d.accept()  # Accepts client
                            with open((server_path + "\\" + file_to_return)) as f:  # Opens file
                                contents = f.readlines()  # Gets all info
                            contents.append('>>FILE ENDED<<')  # Adds end-line

                            dataConn.sendall(str(len(contents)).encode())  # Sends length of contents

                            for line in contents:  # For every line in the file...
                                dataConn.sendall(line.encode())  # ... Send the line
                                dataConn.recv(1024).decode()  # ... Get the OK
                            dataConn.close()  # End data connection

                elif command == "QUIT":
                    exit()


if __name__ == "__main__":
    s = Server()
    s.main()
