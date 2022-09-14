import pygame as pg
from game_page import *
from welcome_page import *

def main():
    pg.init()
    isRunning = True
    while isRunning:
        isRunning = welcome_page()
        if not isRunning: break
        else: isRunning = game_page()
    print('Thanh you for playing our game!')
    print('Give us 10 point!')
main()