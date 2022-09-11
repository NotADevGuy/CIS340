import socket
from datetime import date
import time

class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 65000  # int(input("PORT: "))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            print("Ready for connections...")
            while True:
                message, address = s.recvfrom(1024)
                data = message.decode()
                if data == "BREAK":
                    break
                elif data != "":
                    try:
                        choice = int(data)
                    except:
                        choice = 0
                    if choice == 1:
                        msg = f"{time.strftime('%H:%M:%S', time.localtime())}"
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
