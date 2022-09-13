import pygame as pg

def welcome_page():
    return True

def game_page():
    surface = pg.display.set_mode((1027, 770))
    pg.display.set_caption('Wack a Zombie')
    background = pg.image.load("image/Background.jpg")
    
    while True:
        surface.blit(background,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            pg.display.update()

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