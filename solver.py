
def validate(board, num, pos):
    """
    Returns validity of inserted number
    :param board: 2D list of ints
    :param num: int
    :param pos: (row, column)
    :return: bool
    """
    # Check row:
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column:
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box:
    box = pos[0] // 3, pos[1] // 3

    for i in range(box[0]*3, box[0]*3 + 3):
        for j in range(box[1]*3, box[1]*3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def backtrack_alg(board):
    """
    Solves the Sudoku via Backtracking
    Alters the Board!
    :param board: 2D list of ints
    :return: bool (True = solved)
    """
    pos = find_empty_spot(board)

    if pos: # if valid empty spot found
        for i in range(1, 10):
            if validate(board, i, pos):
                board[pos[0]][pos[1]] = i

                if backtrack_alg(board):
                    return True

                board[pos[0]][pos[1]] = 0
        return False

    else:   # if no empty spot we're done
        return True


def find_empty_spot(board):
    """
    Checks for the first empty space (denoted by 0 on the Board)
    Left to right, top to bottom
    :param board: 2D list of ints
    :return: tuple (row, column)
    """
    for i in range(len(board[1])):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

def print_board(board):
    """
    Prints Board
    :param board: 2D list of ints
    :return:
    """
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")




