import pygame
from game_page import *
from welcome_page import *
from result_page import *

def main():
    pygame.init()
    pygame.display.set_caption('Zombie Wacking')
    isRunning = True
    level = 0
    score = 0
    while isRunning:
        isRunning, level = welcome_page(pygame)
        if not isRunning: break
        else: isRunning = game_page(pygame, level)
        if not isRunning: break
        else: isRunning = result_page(pygame, score)
    pygame.quit()
    print('Thanh you for playing our game!')
    print('Give us 10 point!')

main()