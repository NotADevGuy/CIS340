import socket
from datetime import date
import time

class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        # SOCK_DGRAM is for UDP connections, AF_INET being the IPv4 protocol
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Configures the server to the specified IP and port.
            s.bind((host, port))
            print("Ready for connections...")

            # This while loop handles getting a message, then deciding what needs to be done with it.
            while True:
                # s.recvfrom is for UDP messages
                message, address = s.recvfrom(1024)
                data = message.decode()
                if data != "":
                    # This try/except ensures that choice can become an int, so it can be processed
                    try:
                        choice = int(data)
                    except:
                        choice = 0
                    if choice == 1:
                        msg = f"{time.strftime('%H:%M:%S', time.localtime())}"
                        # s.sendto(message, address) is for sending messages in UDP
                        s.sendto((f"Time: {msg}".encode()), address)
                    elif choice == 2:
                        msg = date.today()
                        msg = f"{msg.strftime('%B %d, %Y')}"
                        s.sendto((f"Date: {msg}".encode()), address)
                    elif choice == 3:
                        s.sendto(("Server shutting down...\nBye!".encode()), address)
                        break


if __name__ == "__main__":
    s = Server()
    s.main()
