import numpy as np
import time
import pygame

board = np.array([[0 for j in range(9)] for i in range(9)])
old_board = np.array([[False for j in range(9)] for i in range(9)])

pygame.init()
pygame.display.set_caption(u'Sudoku Solver')
screen = pygame.display.set_mode((540,540))

done = False
completed = False

font = pygame.font.SysFont("Times new Roman", 24) 

yellow = (255,255,0)
blue = (0,0,100)
green = (0,100,0)
grey = (220,220,220)
cyan = (224,255,255)
black = (0,0,0)
red = (255,0,0)

text_objects = []

for i in range(9):
    text_objects.append([])
    for j in range(9):
        text_objects[i].append(font.render("", True, blue))

def draw():
    global done
    global completed
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
                    if not old_board[i][j]:
                        if not completed:
                            text_objects[i][j] = font.render(str(board[i][j]), True, red)
                        else:
                            text_objects[i][j] = font.render(str(board[i][j]), True, green)
                    else:
                        text_objects[i][j] = font.render(str(board[i][j]), True, blue)
                else:
                    text_objects[i][j] = font.render("", True, red)
                screen.blit(text_objects[i][j],(30+60*j - text_objects[i][j].get_width()//2,30+60*i - text_objects[i][j].get_height()//2))
        pygame.display.flip()
        return
    pygame.quit()



def validate(guess,r,c):
    if guess in board[r]:
        return False
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
    global completed
    solved = False
    draw()
    if board[r][c]!=0:
        if c!=8:
            return solve(r,c+1)
        if r!=8:
            return solve(r+1,0)
        completed = True
        return True

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
                    completed = True
                    solved = True
                    break
            
    if not solved:
        board[r][c] = 0
    return solved

with open('lazy.txt', 'r') as file:
    file = list(file)
    for i in range(len(file)):
        board[i] = file[i].split(",")

for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            old_board[i][j] = True
        



def main():
    draw()
    solve(0,0)
    while not done:
        draw()
    pygame.quit()
    
    
                

    
if __name__ == '__main__':
    main()


    ##print(board)
    ##print("")
    ##start_time = time.time()
    ##solve(0,0)
    ##print(board)
    ##print("")
    ##print(f'Time taken to solve: {time.time()-start_time} seconds.')
