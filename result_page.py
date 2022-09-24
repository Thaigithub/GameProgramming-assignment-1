import pygame, sys
import math
import welcome_page as wcp
import os
import json

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#create display window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie Wacking')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("image/font.ttf", size)

#load background images
bg = pygame.image.load("image/bg.png").convert()
bg_width = bg.get_width()
on = pygame.image.load('image/soundOnBtn.png')
off = pygame.image.load('image/soundOffBtn.png')

#Music
music = pygame.mixer.music.load("audio/musicbackground.ogg")
pop_sound = pygame.mixer.Sound("audio/pop.ogg")
pygame.mixer.music.play(-1)

#button class
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    def update_image(self,img):
        self.image = pygame.transform.scale(img, self.scale)

def save_highscore(high_score):
    file = open('highscore.txt', 'w+') # open the highscore file (in write mode)
    file.write(str(high_score)) # write the data to it
    file.close() # close it

def load_highscore():    
    file = open('highscore.txt', 'r') # open the highscore file (in read mode)
    high_score = file.read() # read it
    high_score = int(high_score) # convert it back to int (from string)
    file.close()    
    return high_score



#game loop
isRunning = False
run = True
def result_page(score):
    #define game variables
    isRunning = False
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
    scroll = 0
    sound_on = True
    while run:
        clock.tick(FPS)
    
        #draw srcolling background
        for i in range(0,tiles):
            screen.blit(bg,(i * bg_width + scroll, 0))
    
        #scroll background
        scroll -= 5
        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
    
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))    
        
        #highscore        
        if score > load_highscore():            
            save_highscore(score)        

        HIGH_SCORE1 = Button(image=pygame.image.load("image/goldcrown.png"), pos=(500, 200), 
                            text_input="Best:"+str(load_highscore()), font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HIGH_SCORE2 = Button(image=pygame.image.load("image/silvercrown.png"), pos=(500, 400), 
                            text_input="Yours:"+str(score), font=get_font(75), base_color="#d7fcd4", hovering_color="White")        
        for button in [HIGH_SCORE1,HIGH_SCORE2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
            button.update(screen)
        

        PLAYAGAIN_BUTTON = Button(image=pygame.image.load("image/ResetRect.png"), pos=(500, 550), 
                             text_input="PLAY AGAIN", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        PLAY_BACK = Button(image=None, pos=(100, 20), 
                            text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        for button in [PLAY_BACK, PLAYAGAIN_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:                
                if PLAYAGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    return wcp.play()
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()                    
                    return wcp.welcome_page()
        pygame.display.update()

    return isRunning