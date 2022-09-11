import socket


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connection made | IP: {addr[0]} | Port: {addr[1]}")
                while True:
                    data = conn.recv(1024)
                    data = data.decode()
                    if data == "bye":  # This is to allow connections after
                        break
                    data = f"Hello {data}".encode()
                    conn.sendall(data)
                    conn, addr = s.accept()
                    # conn.close() # This causes issues


if __name__ == "__main__":
    s = Server()
    s.main()
