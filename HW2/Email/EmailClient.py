import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = input("Enter email server IP: ")
        ptfx_port = 25
        dvct_port = 110

        print()

        while True:
            choice = input("Welcome to email service\nCommands: SEND, RECEIVE, IP (change IP), QUIT\n>> ")

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
                print("Get the email")

            elif choice == "IP":
                host = input(">> Enter email server IP: ")
                print(f"IP Changed to {host}")

            elif choice == "QUIT":
                print("Have a good day!")
                break

            else:
                print("Command not recognized.")

            print('')


if __name__ == '__main__':
    c = Client()
    c.main()
