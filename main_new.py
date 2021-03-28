import numpy as np
import time
import random

board = np.array([[0 for j in range(9)] for i in range(9)])
guess_array = [[[] for j in range(9)] for i in range(9)]
dict_guess_length = {}
fill_order = []

def validate(guess,r,c):
    if guess in board[r]:
        return False
    else:
        lis = []
        for i in range(9):
            lis.append(board[i][c])
        if guess in lis:
            return False
        new_lis = []
        br = r//3
        bc = c//3
        for i in range(3*br,3*(br+1)):
            for j in range(3*bc,3*(bc+1)):
                new_lis.append(board[i][j])
        if guess in new_lis:
            return False
    return True

def guess_array_fill_and_board_update():
    global guess_array
    guess_array = [[[] for j in range(9)] for i in range(9)]
    filled_all_obv_ones = True
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                for guess in range(1,10):
                    if validate(guess,i,j):
                        guess_array[i][j].append(guess)
                if len(guess_array[i][j])==1:
                    filled_all_obv_ones = False
                    board[i][j] = guess_array[i][j][0]
                    guess_array[i][j] = []
    if filled_all_obv_ones:
        return True
    else:
        return guess_array_fill_and_board_update() or filled_all_obv_ones

def solve(ind):
    global fill_order
    global guess_array
    global board
    solved = False
    if ind>=len(fill_order):
        solved = True
        return solved

    for guess in guess_array[fill_order[ind][0]][fill_order[ind][1]]:
        if validate(guess,fill_order[ind][0],fill_order[ind][1]):
            board[fill_order[ind][0]][fill_order[ind][1]] = guess
            if solve(ind+1):
                solved = True
                return solved
                break
            
    if not solved:
        board[fill_order[ind][0]][fill_order[ind][1]] = 0
    return solved

with open('lazy.txt', 'r') as file:
    file = list(file)
    for i in range(len(file)):
        board[i] = file[i].split(",")





print(board)
print("")
guess_array_fill_and_board_update()
#print(board)


for i in range(9):
    for j in range(9):
        dict_guess_length[(i,j)] = len(guess_array[i][j])
        random.shuffle(guess_array[i][j])

#Sorting can be improved
for i in range(1,10):
    for key in dict_guess_length:
        if dict_guess_length[key] == i:
            fill_order.append(key)



print("")
start_time = time.time()
solve(0)
print(board)
print("")
print(f'Time taken to solve: {time.time()-start_time}')
