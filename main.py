import pygame
from game_page import *
from welcome_page import *

def main():
    pygame.init()
    pygame.display.set_caption('Zombie Wacking')
    isRunning = True
    while isRunning:
        isRunning, level = welcome_page()
        print(isRunning)
        print(level)
        if not isRunning: break
        else: isRunning = game_page(pygame, level)
    pygame.quit()
    print('Thanh you for playing our game!')
    print('Give us 10 point!')

main()