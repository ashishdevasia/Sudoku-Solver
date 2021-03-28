import numpy as np
import time

board = np.array([[0 for j in range(9)] for i in range(9)])

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

def solve(r,c):
    solved = False
    if board[r][c]!=0:
        #solved = True
        if c!=8:
            return solve(r,c+1)
        else:
            if r!=8:
                return solve(r+1,0)
            else:
                return True
    else:
        guesses = [i+1 for i in range(9)]
        for guess in guesses:
            if validate(guess,r,c):
                board[r][c] = guess
                if c!=8:
                    if solve(r,c+1):
                        solved = True
                        break
                else:
                    if r!=8:
                        if solve(r+1,0):
                            solved = True
                            break
                    else:
                        solved = True
                        break
            
    if not solved:
        board[r][c] = 0
    return solved

with open('lazy.txt', 'r') as file:
    file = list(file)
    for i in range(len(file)):
        board[i] = file[i].split(",")

print(board)
print("")
start_time = time.time()
solve(0,0)
print(board)
print("")
print(f'Time taken to solve: {time.time()-start_time}')
