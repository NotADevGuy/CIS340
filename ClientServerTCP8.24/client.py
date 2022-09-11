import socket


class Client:
    def __init__(self):
        pass

    def main(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = int(input("PORT: "))  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = (str(input("Please enter your name: "))).encode()
            s.sendall(message)
            data = (s.recv(1024)).decode()
            s.close()
        print(f"Received: {data}")


if __name__ == '__main__':
    c = Client()
    c.main()


# public class TCPClient{
#     public static void main(String args[]){
#         new TCPClient();
#     }
#     public TCPClient(){
#         Socket csock;// client socket
#         BufferedReader in;
#         PrintWriter out;
#         String name,response;
#         int port=4444;
#         Scanner kb= new Scanner(System.in);
#         try{
#
#             csock=new Socket("localhost",port);
#             System.out.println("Connection made ");
#             in=new BufferedReader(new InputStreamReader(csock.getInputStream()));
#             out=new PrintWriter(csock.getOutputStream(),true);
#             System.out.println(" Please enter your name :");
#             name=kb.nextLine();
#             out.println(name);
#             response= in.readLine();
#             System.out.println(response);
#
#         }//end try
#         catch(Exception e) 	{
#             e.printStackTrace();
#         }
#
#     }//Client1
# }//end class