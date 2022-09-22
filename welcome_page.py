import pygame, sys
import math

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
    



#Play
def play():
    level = 1
    isRunning = True
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
    scroll = 0
    while True:
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
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
    
        LEVEL1_BUTTON = Button(image=pygame.image.load("image/OptionRect.png"), pos=(500, 150), 
                            text_input="LEVEL 1", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        LEVEL2_BUTTON = Button(image=pygame.image.load("image/OptionRect.png"), pos=(500, 300), 
                            text_input="LEVEL 2", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        LEVEL3_BUTTON = Button(image=pygame.image.load("image/OptionRect.png"), pos=(500, 450), 
                            text_input="LEVEL 3", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PLAY_BACK = Button(image=None, pos=(100, 20), 
                            text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        for button in [LEVEL1_BUTTON, LEVEL2_BUTTON, LEVEL3_BUTTON,PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(screen)
        
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    return True, 1
                if LEVEL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    return True, 2
                if LEVEL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    return True, 3
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    pop_sound.play()
                    welcome_page()
        pygame.display.update()

#Option
def options():
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
    scroll = 0
    while True:
        clock.tick(FPS)
        for i in range(0,tiles):
            screen.blit(bg,(i * bg_width + scroll, 0))
    
        #scroll background
        scroll -= 5
        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
    

        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(500, 460), 
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pop_sound.play()
                    welcome_page()

        pygame.display.update()




#game loop
isRunning = False
run = True
def welcome_page():
    #define game variables
    isRunning = False
    level = 1
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
    
        PLAY_BUTTON = Button(image=pygame.image.load("image/PlayRect.png"), pos=(500, 200), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("image/OptionRect.png"), pos=(500, 350), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("image/QuitRect.png"), pos=(500, 500), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SOUND_BUTTON = Button(image=pygame.image.load("image/soundOnBtn.png"), pos=(50, 150), 
                            text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, SOUND_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    return play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    pygame.quit()
                    sys.exit()
                if SOUND_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pop_sound.play()
                    sound_on = not sound_on
                    if sound_on:
                        SOUND_BUTTON.update_image(off)
                    else:
                        SOUND_BUTTON.update_image(on)
        pygame.display.update()
        
    return isRunning,level       
