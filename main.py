from game_page import Game
from welcome_page import welcome_page
from result_page import result_page

def main():
    isRunning = True
    level = 0
    score = 0
    while isRunning:
        isRunning, level = welcome_page()
        if not isRunning: break
        time = 30
        max_zombie = 5
        game = Game(time, max_zombie)
        isRunning = game.game_page()
        del game
        if not isRunning: break
        isRunning = result_page(score)
    print('Thanh you for playing our game!')
    print('Give us 10 point!')

main()