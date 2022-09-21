import pygame
framerate = 60

def time_to_string(time):
    minute, second = "",""
    minute = str(time//60) if (time//60)>=10 else "0"+str(time//60)
    second = str(time%60) if (time%60)>=10 else "0"+str(time%60)
    return minute+":"+second

def loop_event():
    pass

def loop_display():
    pass

def game_page(time):
    #Load image
    pygame.init()
    pygame.display.set_caption("Zombie Wacking")
    background = pygame.image.load("image/Background.jpg")
    zombie = pygame.image.load("image/Zombie.png")
    zombie = pygame.transform.scale(zombie,(60,60))
    mallet1 = pygame.image.load("image/Mallet1.png")
    mallet1 = pygame.transform.scale(mallet1,(100,100))
    mallet2 = pygame.image.load("image/Mallet2.png")
    mallet2 = pygame.transform.scale(mallet2,(100,100))
    #Set up system
    surface = pygame.display.set_mode((background.get_width(), background.get_height()))
    timer_event = {}
    #Game logic
    zombie_matrix = []
    zombie_rect_list = []
    for i in range(5):
        zombie_matrix.append([])
        zombie_rect_list.append([])
        for j in range(9):
            zombie_matrix[i].append(False)
            zombie_rect_list[i].append(zombie.get_rect(center = (93+105*j,83+140*i)))
    #Set up display utility object
    timer_object = [pygame.font.SysFont(None, 50)]
    timer_object.append(timer_object[0].render(time_to_string(time), True, (255, 255, 255)))
    timer_event["countdown"] = pygame.USEREVENT+len(timer_event)+1
    pygame.time.set_timer(timer_event["countdown"], 1000)
    #Start game
    while True:
        #Input and process
        mouseclick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == timer_event["countdown"]:
                time -= 1
                timer_object[1] = timer_object[0].render(time_to_string(time), True, (255, 255, 255))
                if time == 0:
                    pygame.time.set_timer(timer_event["countdown"],0)
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseclick = True
                check = False
                for i in range(5):
                    for j in range(9):
                        if zombie_rect_list[i][j].collidepoint(pygame.mouse.get_pos()) and zombie_matrix[i][j]:
                            check = True
                            break
        # Update display
        surface.blit(background,(0,0))
        for i in range(5):
            for j in range(9):
                if zombie_matrix[i][j]:
                    surface.blit(zombie,zombie_rect_list[i][j])
        if mouseclick: surface.blit(mallet2,mallet2.get_rect(center = (pygame.mouse.get_pos()[0]+40,pygame.mouse.get_pos()[1]-20)))
        else: surface.blit(mallet1,mallet1.get_rect(center = (pygame.mouse.get_pos()[0]+40,pygame.mouse.get_pos()[1]-20)))
        surface.blit(timer_object[1], timer_object[1].get_rect(center = (900, 750)))
        pygame.cl
        pygame.display.flip()