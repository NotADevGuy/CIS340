import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = input("Enter email server IP: ")
        ptfx_port = 25
        dvct_port = 110

        while True:
            choice = input("\nWelcome to email service\nCommands: SEND, RECEIVE, IP (change IP), QUIT\n>> ")

            if choice == "SEND":
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, ptfx_port))
                        s.recv(1024).decode()

                        domain = input(">> Domain: ")
                        s.sendall(f"EHLO {domain}\n".encode())
                        s.recv(1024).decode()

                        name = input(">> Your email: ")
                        s.sendall(f"MAIL FROM:{name}\n".encode())
                        s.recv(1024).decode()

                        receiver = input(">> Email recipient: ")
                        s.sendall(f"RCPT TO:{receiver}\n".encode())
                        code = s.recv(1024).decode()
                        if code[:3] == "454":
                            print("# Invalid recipient domain. Try Again.")
                        elif code[:3] == "550":
                            print("# Invalid recipient. Try Again.")
                        elif code[:3] == "250":
                            message = input(">> Message: ")
                            s.sendall("DATA\n".encode())
                            s.sendall(f"{message}\n".encode())
                            s.sendall(".\n".encode())
                            s.sendall("\n".encode())
                            s.recv(1024).decode()
                            print(">> ...\n>> EMAIL SENT")
                        else:
                            print(code)
                            print("Not exactly sure what went wrong... Try again.")
                except:
                    print("Something happened... is the IP right?")

            elif choice == "RECEIVE":
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, dvct_port))
                        s.recv(1024).decode()

                        user = input(">> Username: ")
                        s.sendall(f"user {user}\n".encode())
                        s.recv(1024).decode()

                        pswd = input(">> Password (very secure, you can trust us): ")
                        s.sendall(f"pass {pswd}\n".encode())

                        code = s.recv(1024).decode()
                        if code[:4] == "-ERR":
                            print("Incorrect password or username! Try Again.")
                        else:
                            s.sendall("LIST\n".encode())
                            count = ((s.recv(1024).decode()).split(" "))[1]
                            print()
                            print(f"Login successful, {count} messages!")
                            print(f"Commands: LIST, READ, or QUIT")
                            while True:
                                choice = input(">> ")
                                choice = choice.split(" ")
                                if choice[0] == "LIST" and len(choice) == 1:
                                    s.sendall("LIST\n".encode())
                                    print(s.recv(1024).decode())
                                elif choice[0] == "READ":
                                    if len(choice) == 1:
                                        num = input(">> Email #: ")
                                        s.sendall(f"RETR {num}\n".encode())
                                        print(s.recv(1024).decode())
                                    elif len(choice) == 2:
                                        print(f"RETR {choice[1]}")
                                        s.sendall(f"RETR {choice[1]}\n".encode())
                                        print(s.recv(1024).decode())
                                    else:
                                        print("Incorrect format. Try Again.\n")
                                elif choice[0] == "QUIT":
                                    choice = ''
                                    break
                                else:
                                    print("Unrecognized command or command format. Try Again.\n")
                except:
                    print("Something happened... is the IP right?")

            elif choice == "IP":
                host = input(">> Enter email server IP: ")
                print(f"IP Changed to {host}")

            elif choice == "QUIT":
                print("Have a good day! Thanks for using my email service!")
                break

            else:
                print("Command not recognized.")


if __name__ == '__main__':
    c = Client()
    c.main()
