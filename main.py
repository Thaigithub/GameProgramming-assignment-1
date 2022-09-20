from game_page import *
from welcome_page import *
from result_page import *

def main():
    isRunning = True
    level = 0
    score = 0
    while isRunning:
        # isRunning, level = welcome_page()
        # if not isRunning: break
        isRunning = game_page(level)
        if not isRunning: break
        isRunning = result_page(score)
    pygame.quit()
    print('Thanh you for playing our game!')
    print('Give us 10 point!')

main()