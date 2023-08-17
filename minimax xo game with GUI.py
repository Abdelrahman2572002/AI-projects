#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import *
from tkinter import messagebox
import platform
import time
from os import system
from random import choice

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0: cells.append([x, y])
    return cells

def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -float('inf')]
    else:
        best = [-1, -1, float('inf')]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def render(state, c_choice, h_choice):
    print('----------------')
    for row in state:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', c_choice, '|', end='')
            elif cell == -1:
                print('|', h_choice, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')

def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print('Computer turn [{}]'.format(c_choice))
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)
    draw_board()

def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print('Human turn [{}]'.format(h_choice))
    render(board, c_choice, h_choice)

    while (move < 1 or move > 9):
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            try_move = set_move(coord[0], coord[1], HUMAN)

            if try_move == False:
                print('Bad move')
                move = -1
        except KeyboardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

def draw_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] == HUMAN:
                buttons[i][j].config(text="O", state=DISABLED)
            elif board[i][j] == COMP:
                buttons[i][j].config(text="X", state=DISABLED)
            else:
                buttons[i][j].config(state=NORMAL)

def button_click(row, col):
    global current_player

    if board[row][col] == 0:
        board[row][col] = HUMAN
        buttons[row][col].config(text="O", state=DISABLED)
        winner = evaluate(board)
        if winner != 0:
            end_game(winner)
        else:
            ai_turn("X", "O")

def end_game(winner):
    message = ""
    if winner == -1:
        message = "It's a draw!"
    else:
        message = f"Player {winner} wins!"
    messagebox.showinfo("Game Over", message)
    root.quit()

# Create the root window
root = Tk()
root.title("Tic-Tac-Toe")

# Create and configure the buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(
            root, text="", font=("Helvetica", 24), width=5, height=2,
            command=lambda row=i, col=j: button_click(row, col)
        )
        buttons[i][j].grid(row=i, column=j)

# Start the event loop
root.mainloop()


# In[ ]:




