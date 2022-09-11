import socket


class Server:
    def __init__(self):
        pass

    def main(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = int(input("PORT: "))  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
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

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.bind((HOST, PORT))
        #     s.listen()
        #     conn, addr = s.accept()
        #     with conn:
        #         print(f"Connection made | IP: {addr[0]} | Port: {addr[1]}")
        #         while True:
        #             data = conn.recv(1024)
        #             data = data.decode()
        #             if not data:
        #                 break
        #             data = f"Hello {data}".encode()
        #             conn.sendall(data)
        #             # conn.close() # This causes issues



if __name__ == "__main__":
    s = Server()
    s.main()


# import java.net.*;
# import java.io.*;
#
#
# public class TCPServer {
#     public static void main(String args[]) {
#         new TCPServer();
#     }
#
#     public TCPServer() {
#         ServerSocket bigSock;
#         Socket csock;
#         BufferedReader in;
#         PrintWriter out;
#         int port = 4444;
#         int x = 1;
#         try {
#             bigSock = new ServerSocket(port);
#             System.out.println("Ready to accept connections: ");
#             while (x == 1) {
#                 csock = bigSock.accept();
#                 System.out.println("Client Connected");
#                 in = new BufferedReader(new InputStreamReader(csock.getInputStream()));
#                 out = new PrintWriter(csock.getOutputStream(), true);
#                 System.out.println("Streams Established");
#                 // Protocol
#                 String name = in.readLine();
#                 out.println("Hello " + name);
#
#                 // Close streams and client socket
#                 in.close();
#                 out.close();
#                 csock.close();
#             } // End Big Socket
#             bigSock.close();
#         } catch(Exception e) {
#             System.out.println("ERROR");
#         }
#     }
#
# }