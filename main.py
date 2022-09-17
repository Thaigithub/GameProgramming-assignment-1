import pygame as pg
from game_page import *
from welcome_page import *

def main():
    pg.init()
    pg.display.set_caption('Zombie Wacking')
    isRunning = True
    while isRunning:
        isRunning, level = welcome_page()
        print(isRunning)
        if not isRunning: break
        else: isRunning = game_page(200)
    pg.quit()
    print('Thanh you for playing our game!')
    print('Give us 10 point!')

main()