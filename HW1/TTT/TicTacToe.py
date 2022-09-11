players = [str(input("Player 1 name: ")), str(input("Player 2 name: "))]
board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
moves = 0


def printBoard():
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")


while moves < 9:
    printBoard()

    currentPlayer = (players[0] if moves % 2 == 0 else players[1])
    currentSymbol = ("X" if currentPlayer == players[0] else "Y")

    choice = int(input(f"Please enter spot 0-8, {currentPlayer} ({currentSymbol}): "))

    while True:
        if choice > 8:
            choice = int(input(f"Number too high, try again: "))
        elif choice < 0:
            choice = int(input(f"Number too low, try again: "))
        elif board[choice] != choice:
            choice = int(input("Spot already taken, try again: "))
        else:
            break
    board[choice] = currentSymbol

    for wc in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
        if board[wc[0]] == board[wc[1]] == board[wc[2]]:
            moves = 10
            players = currentPlayer
            break
    moves += 1

printBoard()

print("Game ended in tie") if moves == 9 else print(f"Winner is {players}")
