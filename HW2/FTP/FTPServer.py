import socket


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            conn.sendall("Connection made to FTP Server!".encode())

            conn.sendall("\nWould you like:\n\t1. Active\n\t2. Passive connection\n\t3. Quit (Client)\n\t4. Stop Server".encode())
            connType = int(conn.recv(1024).decode())

            if connType == 1:
                conn.sendall("Enter desired port: ".encode())
                port = int(conn.recv(1024).decode())
                print(port)
            elif connType == 2:
                pass
            elif connType == 4:
                exit()
            pass


if __name__ == "__main__":
    s = Server()
    s.main()
