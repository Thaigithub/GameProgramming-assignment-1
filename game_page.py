import pygame as pg

framerate = 60

def time_to_string(time):
    minute, second = "",""
    minute = str(time//60) if (time//60)>=10 else "0"+str(time//60)
    second = str(time%60) if (time%60)>=10 else "0"+str(time%60)
    return minute+":"+second

def game_page(time):
    #Load image
    background = pg.image.load("image/Background.jpg")
    zombie = pg.image.load("image/Zombie.png")
    zombie = pg.transform.scale(zombie,(60,60))
    mallet1 = pg.image.load("image/Mallet1.png")
    mallet1 = pg.transform.scale(mallet1,(100,100))
    mallet2 = pg.image.load("image/Mallet2.png")
    mallet2 = pg.transform.scale(mallet2,(100,100))
    #Set up system
    surface = pg.display.set_mode((background.get_width(), background.get_height()))
    clock = pg.time.Clock()
    display_object = {}
    timer_event = {}
    #Game logic
    zombie_matrix = []
    zombie_rect_list = [[]]
    for i in range(5):
        zombie_matrix.append([])
        for j in range(9):
            zombie_matrix[i].append(False)
            zombie.get_rect(center = (93+105*j,83+140*i))
    #Set up display utility object
    display_object["countdown"] = [pg.font.SysFont(None, 50)]
    display_object["countdown"].append(display_object["countdown"][0].render(time_to_string(time), True, (255, 255, 255)))
    timer_event["countdown"] = pg.USEREVENT+len(timer_event)+1
    pg.time.set_timer(timer_event["countdown"], 1000)
    #Start game
    while True:
        surface.blit(background,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == timer_event["countdown"]:
                time -= 1
                display_object["countdown"][1] = display_object["countdown"][0].render(time_to_string(time), True, (255, 255, 255))
                if time == 0:
                    pg.time.set_timer(timer_event["countdown"],0)
                    return True
        for i in range(5):
            for j in range(9):
                if zombie_matrix[i][j]:
                    surface.blit(zombie,zombie_rect_list[i][j])
        if event.type == pg.MOUSEBUTTONDOWN:
            surface.blit(mallet2,mallet2.get_rect(center = (pg.mouse.get_pos()[0]+40,pg.mouse.get_pos()[1]-20)))
            check = False
            for i in range(5):
                for j in range(9):
                    if zombie_rect_list[i][j].collidepoint(pg.mouse.get_pos()) and zombie_matrix[i][j]:
                        check = True
                        break
            if check: print("Hit")
            else: print("Miss")
        else: surface.blit(mallet1,mallet1.get_rect(center = (pg.mouse.get_pos()[0]+40,pg.mouse.get_pos()[1]-20)))
        surface.blit(display_object["countdown"][1], display_object["countdown"][1].get_rect(center = (900, 750)))
        pg.display.flip()