import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 65000  # int(input("PORT: "))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
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
                    s.sendto((str(choice).encode()), (host, port))
                    print(f"\n{s.recv(1024).decode()}\n\n")
                elif choice == 3:
                    s.sendto((str(choice).encode()), (host, port))
                    print(f"\n{s.recv(1024).decode()}")
                    break


if __name__ == '__main__':
    c = Client()
    c.main()
