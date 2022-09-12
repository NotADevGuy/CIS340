import socket


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = int(input("PORT: "))

        # TTT game initialization
        player = [0, 0]
        board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        moves = 0

        # Method for printing the board
        def getBoard():
            message = ""
            for i in range(0, 9):
                message += f"{board[i]}"
                if i == 2 or i == 5:
                    message += "\n"
                elif i != 8:
                    message += " | "
            return message

        # SOCK_STREAM is for TCP connections, AF_INET being the IPv4 protocol
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # These lines bind the server to the address, and allows a connection...
            s.bind((host, port))
            s.listen()

            # ... And once a connection is found it is accepted
            conn, addr = s.accept()

            # Next two lines lets both players know a connection is made
            print(f"Connection to {addr[0]} on port #{addr[1]}")
            conn.sendall("Connect made to TicTacToe Server!".encode())

            # These next 3 lines handles naming both players
            player[0] = str(input("Player 1 name: "))
            conn.sendall("Player 2 name: ".encode())
            player[1] = conn.recv(1024).decode()

            # 'with conn:' means using the connection made, do what follows
            with conn:
                # Normally this is a while True, but for TTT it can be changed to 'while moves < 9:'
                while moves < 9:
                    # Using list comprehension, the currentPlayer and currentSymbol are established
                    # List comprehension allows you to save space and make some loops and statements more compact
                    currentPlayer = (player[0] if moves % 2 == 0 else player[1])
                    currentSymbol = ("X" if currentPlayer == player[0] else "Y")

                    # This is how I decided to handle input, it figures out what player is going and goes from there
                    if player[0] == currentPlayer:
                        # This is the server player, so not too bad, simple stuff here.
                        print(getBoard())
                        choice = input(f"Enter spot 0-8, {currentPlayer} ({currentSymbol}): ")
                        try:
                            choice = int(choice)
                        except:
                            choice = -1
                        # Simplified the while loop, otherwise it's a fairly large code block. Save space when I can
                        while choice > 8 or choice < 0 or board[choice] != choice:
                            choice = int(input("Bad input, try again: "))

                    elif player[1] == currentPlayer:
                        # This is the client player, the next 3 lines sends the board, requests a move and takes it in
                        conn.sendall(getBoard().encode())
                        conn.sendall(f"Enter spot 0-8, {currentPlayer} ({currentSymbol}): ".encode())
                        choice = conn.recv(1024).decode()
                        # Have to do this to ensure the input can be turned to an int, so it can be compared
                        try:
                            choice = int(choice)
                        except:
                            choice = -1
                        # Same as the input validation as above, but with the socket portions
                        while choice > 8 or choice < 0 or board[choice] != choice:
                            conn.sendall(f"Bad input, try again: ".encode())
                            choice = conn.recv(1024).decode()
                            try:
                                choice = int(choice)
                            except:
                                choice = -1

                    # Updates the board
                    board[choice] = currentSymbol

                    # This searches the board for any possible wins.
                    for wc in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
                        if board[wc[0]] == board[wc[1]] == board[wc[2]]:
                            moves = 10
                            player = currentPlayer
                            # "BREAK" is a nice command to send to let client know to expect a winner
                            conn.sendall("BREAK".encode())
                            break
                    moves += 1

                # These lines generate a win condition (winner or tie) with list comprehension
                # Then it sends it to the client, and prints for the server
                winCon = "Game ended in tie" if moves == 9 else f"Winner is {player}"
                conn.sendall(winCon.encode())
                print(winCon)


if __name__ == '__main__':
    s = Server()
    s.main()
