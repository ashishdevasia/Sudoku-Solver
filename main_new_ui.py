import numpy as np
import time
import pygame
import random

fps = 16
time_delay = 1/fps

old_time = time.time()
start_time = time.time()

board = np.array([[0 for j in range(9)] for i in range(9)])
old_board = np.array([[False for j in range(9)] for i in range(9)])

guess_array = [[[] for j in range(9)] for i in range(9)]
dict_guess_length = {}
fill_order = []

pygame.init()
pygame.display.set_caption(u'Sudoku Solver')
screen = pygame.display.set_mode((540,540))

done = False
completed = False

font = pygame.font.SysFont("Times new Roman", 24) 

yellow = (255,255,0)
blue = (0,0,255)
green = (0,100,0)
grey = (220,220,220)
cyan = (224,255,255)
black = (0,0,0)
red = (255,0,0)

colour_array = np.array([[red for j in range(9)] for i in range(9)])

text_objects = []

for i in range(9):
    text_objects.append([])
    for j in range(9):
        text_objects[i].append(font.render("", True, blue))

def draw():
    '''
    This is the function that needs to be called in order to draw the state of the board at any given time.
    Limited by FPS in order to not compromise with the solving speed.
    '''
    global old_time
    if (time.time() - old_time) < time_delay:
        return
    old_time = time.time()
    global done
    global completed
    global colour_array
    if not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
        screen.fill(cyan)
        for i in range(3):
            pygame.draw.line(screen, (0, 0, 0), [0, (i+1)*180], [540, (i+1)*180], 3)
            pygame.draw.line(screen, (0, 0, 0), [(i+1)*180, 0], [(i+1)*180, 540], 3)
        for i in range(9):
            pygame.draw.line(screen, (105, 105, 105), [0, (i+1)*60], [540, (i+1)*60], 1)
            pygame.draw.line(screen, (105, 105, 105), [(i+1)*60, 0], [(i+1)*60, 540], 1)
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                        text_objects[i][j] = font.render(str(board[i][j]), True, colour_array[i][j])
                else:
                    text_objects[i][j] = font.render("", True, red)
                screen.blit(text_objects[i][j],(30+60*j - text_objects[i][j].get_width()//2,30+60*i - text_objects[i][j].get_height()//2))
        pygame.display.flip()
        return
    pygame.quit()

def validate(guess,r,c):
    '''
    Checks if the number 'guess' is a valid number in the cell represented by r,c.
    '''
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
    global colour_array
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
                    colour_array[i][j] = green
                    guess_array[i][j] = []
    if filled_all_obv_ones:
        return True
    else:
        return guess_array_fill_and_board_update() or filled_all_obv_ones

def solve(ind, last_element=True):
    global fill_order
    global guess_array
    global board
    global colour_array
    global completed
    solved = False
    draw()
    if ind>=len(fill_order):
        solved = True
        return solved

    for guess in guess_array[fill_order[ind][0]][fill_order[ind][1]]:
        if validate(guess,fill_order[ind][0],fill_order[ind][1]):
            board[fill_order[ind][0]][fill_order[ind][1]] = guess
            if (guess == guess_array[fill_order[ind][0]][fill_order[ind][1]][-1]) and (last_element):
                colour_array[fill_order[ind][0]][fill_order[ind][1]] = green
                if solve(ind+1,True):
                    solved = True
                    completed = True
                    return solved
            else:
                if solve(ind+1,False):
                    solved = True
                    completed = True
                    return solved
            
    if not solved:
        board[fill_order[ind][0]][fill_order[ind][1]] = 0
    return solved

with open('lazy.txt', 'r') as file:
    file = list(file)
    for i in range(len(file)):
        board[i] = file[i].split(",")

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                old_board[i][j] = True
                colour_array[i][j] = blue


def main():
    guess_array_fill_and_board_update()
    for i in range(9):
        for j in range(9):
            dict_guess_length[(i,j)] = len(guess_array[i][j])
            random.shuffle(guess_array[i][j])

    #Sorting can be improved
    for i in range(1,10):
        for key in dict_guess_length:
            if dict_guess_length[key] == i:
                fill_order.append(key)

    solve(0)
    print(completed)
    print(f'Time taken: {(((- start_time + time.time())*10000)//1)/10000} s')
    
    for i in range(9):
        for j in range(9):
            if not old_board[i][j]:
                if completed:
                    colour_array[i][j] = green
                else:
                    colour_array[i][j] = red
                
    while not done:
        draw()
    pygame.quit()
    
if __name__ == '__main__':
    main()    

##print(board)
##print("")
##guess_array_fill_and_board_update()
###print(board)
##
##
##for i in range(9):
##    for j in range(9):
##        dict_guess_length[(i,j)] = len(guess_array[i][j])
##
###Sorting can be improved
##for i in range(1,10):
##    for key in dict_guess_length:
##        if dict_guess_length[key] == i:
##            fill_order.append(key)
##
##
##
##print("")
##start_time = time.time()
##solve(0)
##print(board)
##print("")
##print(f'Time taken to solve: {time.time()-start_time}')
