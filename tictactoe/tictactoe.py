"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0

    if board == initial_state():
        return X  # First player is always X
    elif terminal(board):
        print("The gave is already over")
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_num += 1
            elif board[i][j] == O:
                o_num += 1

    if x_num > o_num:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Check if the cell is empty
    if board[i][j] is not None:
        raise ValueError('Invalid action: Cell already occupied')

    # Make a deep copy of the board to avoid modifying it directly
    new_board = [row[:] for row in board]

    # Determine the current player
    current_player = player(board)

    # Make the move based on the current player
    new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if row.count('X') == len(row):
            return X
        elif row.count('O') == len(row):
            return O

    for col in range(len(board[0])):
        if all(board[row][col] == 'X' for row in range(len(board))):
            return 'X'
        elif all(board[row][col] == 'O' for row in range(len(board))):
            return 'O'

    if all(board[i][i] == 'X' for i in range(len(board))) or all(board[i][len(board) - 1 - i] == 'X' for i in range(len(board))):
        return X
    elif all(board[i][i] == 'O' for i in range(len(board))) or all(board[i][len(board) - 1 - i] == 'O' for i in range(len(board))):
        return O

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    winner_symbol = winner(board)
    if winner_symbol is not None:
        return True

    if all(cell != EMPTY for row in board for cell in row):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_symbol = winner(board)

    if winner_symbol == 'X':
        return 1
    elif winner_symbol == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board):
        if terminal(board):
            return utility(board)

        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))

        return v

    def min_value(board):
        if terminal(board):
            return utility(board)

        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))

        return v

    current_player = player(board)

    if terminal(board):
        return None

    if current_player == 'X':
        optimal_action = max(actions(board), key=lambda action: min_value(result(board, action)))
    else:
        optimal_action = min(actions(board), key=lambda action: max_value(result(board, action)))

    return optimal_action
