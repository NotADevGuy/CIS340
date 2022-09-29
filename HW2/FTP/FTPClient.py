import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 1040

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(s.recv(1024).decode())
            print(s.recv(1024).decode())
            response = 5
            while response not in [1, 2, 3, 4]:
                response = input("Choice: ")
                try:
                    response = int(response)
                except:
                    response = 5
            response = str(response)
            s.sendall(response.encode())
            response = int(response)
            if response == 1:
                print(s.recv(1024).decode())
                while True:
                    port = input("Port Choice (1024 - 65535): ")
                    try:
                        port = int(port)
                        if 1024 <= port <= 65535:
                            break
                        # else:
                        #     port = ''
                    except:
                        port = ''

                s.sendall(port.encode())

            elif response == 2:
                pass
            elif response == 3:
                exit()

            s.close()


if __name__ == '__main__':
    c = Client()
    c.main()
