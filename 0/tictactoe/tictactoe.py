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
    # return [[X,X,O],
    #         [EMPTY,O,EMPTY],
    #         [EMPTY,EMPTY,EMPTY]]

board11 = [[EMPTY,O,EMPTY],
            [X,O,X],
            [EMPTY,EMPTY,X]]
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cnt = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] is not None):
                cnt = cnt+1
    if(cnt%2 == 0):
        return X
    else:
        return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    l = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                l.add((i,j))

    return l
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board1 = copy.deepcopy(board)
    i,j = action
    if i<0 or j<0 or i>3 or j>3:
        raise IndexError
    playr = player(board1)
    board1[i][j] = playr
    return board1
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if not terminal(board):
        return None
    state = utility(board)
    if state == 0:
        return None
    elif state == 1:
        return X
    else:
        return O
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state = False
    ut = utility(board)
    if ut == 1 or ut == -1:
        return True

    for i in range(3):
        for j in range(3):
            if(board[i][j] is None):
                state = True
    return not(state)
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    state = 0
    for i in range(3):
        if(board[i][0] is not None) & (board[i][1] is not None) & (board[i][2] is not None):
            if(board[i][0] == board[i][1]) & (board[i][1] == board[i][2]):
                if(board[i][0] == X):
                    state = 1
                else:
                    state = -1

    for i in range(3):
        if(board[0][i] is not None) & (board[1][i] is not None) & (board[2][i] is not None):
            if(board[0][i] == board[1][i]) & (board[1][i] == board[2][i]):
                if(board[1][i] == X):
                    state = 1
                else:
                    state = -1

    if(board[0][0] is not None) & (board[1][1] is not None) & (board[2][2] is not None):
        if(board[0][0] == board[1][1]) & (board[1][1] == board[2][2]):
            if(board[0][0] == X):
                state = 1
            else:
                state = -1
    if(board[0][2] is not None) & (board[1][1] is not None) & (board[2][0] is not None):
        if(board[0][2]==board[1][1]) & (board[1][1]==board[2][0]):
            if board[0][2] == X:
                state = 1
            else:
                state = -1
    return state
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    return myminimax(board)[1]

def myminimax(board):
    if terminal(board):
        return (utility(board), None)
    acts = actions(board)
    playr = player(board)
    if playr == X:
        playr = 1
    else:
        playr = -1
    l=[None,None]
    for act in acts:
        res = myminimax(result(board,act))
        if res[0] == playr:
            return (playr,act)
        elif res[0] == 0:
            l[0] = (0,act)
        else:
            l[1] = (res[0],act)
    if l[0] is not None:
        return l[0]
    else:
        return l[1]