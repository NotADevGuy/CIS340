import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 65000  # int(input("PORT: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(s.recv(1024).decode())

            # These next 3 lines handles recieving name request and returning
            data = (s.recv(1024)).decode()
            name = str(input(f"{data}")).encode()
            s.sendall(name)

            while True:
                data = s.recv(1024)
                data = data.decode()
                if data == "BREAK":
                    break
                if data[-2:] == ": ":
                    data = str(input(f"{data}")).encode()
                    s.sendall(data)
                elif data != "":
                    print(data)

            # Handles printing winner or if it was a tie
            while True:
                data = (s.recv(1024)).decode()
                if data != "":
                    break
            print(data)
            s.close()


if __name__ == '__main__':
    c = Client()
    c.main()