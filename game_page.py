import pygame as pg

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