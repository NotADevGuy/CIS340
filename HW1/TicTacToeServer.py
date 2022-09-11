import socket


class Server:
    def __init__(self):
        pass

    def main(self):
        host = "127.0.0.1"
        port = 65000  # int(input("PORT: "))

        player = [0, 0]
        board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        moves = 0

        def getBoard():
            message = ""
            for i in range(0, 9):
                message += f"{board[i]}"
                if i == 2 or i == 5:
                    message += "\n"
                elif i != 8:
                    message += " | "
            return message

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()

            # Next two lines let both players know a connection is made
            print(f"Connection to {addr[0]} on port #{addr[1]}")
            conn.sendall("Connect made to TicTacToe Server!".encode())

            # These next 3 lines handles naming both players
            player[0] = str(input("Player 1 name: "))
            conn.sendall("Player 2 name: ".encode())
            player[1] = conn.recv(1024).decode()

            with conn:
                while moves < 9:
                    # TODO Print board for either player.

                    currentPlayer = (player[0] if moves % 2 == 0 else player[1])
                    currentSymbol = ("X" if currentPlayer == player[0] else "Y")

                    if player[0] == currentPlayer:
                        print(getBoard())
                        choice = int(input(f"Enter spot 0-8, {currentPlayer} ({currentSymbol}): "))
                        while choice > 8 or choice < 0 or board[choice] != choice:
                            choice = int(input("Bad input, try again: "))
                    elif player[1] == currentPlayer:
                        conn.sendall(getBoard().encode())
                        conn.sendall(f"Enter spot 0-8, {currentPlayer} ({currentSymbol}): ".encode())
                        choice = conn.recv(1024).decode()
                        try:
                            choice = int(choice)
                        except:
                            print("ERROR")
                            choice = -1
                        while choice > 8 or choice < 0 or board[choice] != choice:
                            conn.sendall(f"Bad input, try again: ".encode())
                            choice = conn.recv(1024).decode()
                            try: choice = int(choice)
                            except: choice = -1

                    board[choice] = currentSymbol

                    for wc in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
                        if board[wc[0]] == board[wc[1]] == board[wc[2]]:
                            moves = 10
                            player = currentPlayer
                            conn.sendall("BREAK".encode())
                            break
                    moves += 1
                winCon = "Game ended in tie" if moves == 9 else f"Winner is {player}"
                conn.sendall(winCon.encode())
                print(winCon)


if __name__ == '__main__':
    s = Server()
    s.main()