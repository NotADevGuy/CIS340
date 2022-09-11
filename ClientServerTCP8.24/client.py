import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = (str(input("Please enter your name: "))).encode()
            s.sendall(message)
            data = (s.recv(1024)).decode()
            s.close()
        print(f"Received: {data}")


if __name__ == '__main__':
    c = Client()
    c.main()
