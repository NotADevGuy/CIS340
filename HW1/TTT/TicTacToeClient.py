import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        # SOCK_STREAM is for TCP connections, AF_INET being the IPv4 protocol
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # The s.connect() method binds client to the server
            s.connect((host, port))

            # This is to receive the acknowledgement of connection message
            print(s.recv(1024).decode())

            # These next 3 lines handles receiving name request and returning answer
            data = (s.recv(1024)).decode()
            name = str(input(f"{data}")).encode()
            s.sendall(name)

            # This while loop manages the whole TTT game, it takes in the message
            # If it's BREAK it stops the loop
            # If it ends with ": " it prompts for input
            # Otherwise it prints the data out
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

            # Handles printing who the winner was or if it was a tie
            while True:
                data = (s.recv(1024)).decode()
                if data != "":
                    break
            print(data)
            s.close()


if __name__ == '__main__':
    c = Client()
    c.main()
