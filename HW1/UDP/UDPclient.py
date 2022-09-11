import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        # This while loop handles getting a message, then deciding what needs to be done with it.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # "Connect" in this case really means send, it just uses same syntax
            s.connect((host, port))
            while True:
                choice = input("0: Quit | 1: Time | 2: Date | 3: Shut down server\nYour choice: ")
                try:
                    choice = int(choice)
                except:
                    choice = 4
                if choice == 0:
                    break
                elif choice == 1 or choice == 2:
                    # s.sendto(message, address) is for sending messages in UDP
                    s.sendto((str(choice).encode()), (host, port))
                    print(f"\n{s.recv(1024).decode()}\n\n")
                elif choice == 3:
                    s.sendto((str(choice).encode()), (host, port))
                    print(f"\n{s.recv(1024).decode()}")
                    break


if __name__ == '__main__':
    c = Client()
    c.main()
