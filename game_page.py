import pygame
from define import Constants, Zombie, Score, Text

class Game:

    def __init__(self, timer, max_zombie):
        #Init pygame
        pygame.init()
        
        #Init pygame screen
        pygame.display.set_caption("Zombie Wacking")
        self.screen = pygame.display.set_mode((Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        
        #Load background
        self.background = pygame.image.load(Constants.IMAGEBACKGROUND)
        self.background = pygame.transform.scale(self.background,(Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        
        #Load zombie
        self.zombie = pygame.image.load(Constants.IMAGEZOMBIE)
        self.zombie = pygame.transform.scale(self.zombie,(Constants.ZOMBIEWIDTH, Constants.ZOMBIEHEIGHT))
        
        #Load mallet
        self.mallet = pygame.image.load(Constants.IMAGEMALLET)
        self.mallet = pygame.transform.scale(self.mallet,(Constants.MALLETWIDTH, Constants.MALLETHEIGHT))

        #Set timer
        self.timer = timer
        
        #Set max zombie
        self.max_zombie = max_zombie
        
        #Set clock
        self.clock = pygame.time.Clock()
        
        #Set signal for loop
        self.loop = True
        
        #Init zombie list
        self.zombies = [Zombie() for _ in range(Constants.ZOMBIECOUNT)]
        
        
        # Generate hole positions
        self.holes = []
        self.used_holes = []
        for row in range(Constants.HOLEROWS):
            for column in range(Constants.HOLECOLUMNS):
                self.holes.append((Constants.HOLEBASE[0] + row*Constants.HOLEHEIGHT, Constants.HOLEBASE[1] + column*Constants.HOLEWIDTH))

        # Get the text object
        self.text = Text()

        # Get the score object
        self.score = Score(self.text)

        # Indicates whether the HUD indicators should be displayed
        self.show_hit = 0
        self.show_miss = 0

        # Allow for game timer
        self.timer_start = 0
        
    def time_to_string(time):
        if time<0: return "00:00"
        minute, second = "",""
        minute = str(time//60) if (time//60)>=10 else "0"+str(time//60)
        second = str(time%60) if (time%60)>=10 else "0"+str(time%60)
        return minute+":"+second
    
    @property
    def timerData(self):
        if self.timer is not None and self.timer_start != 0:
            remain = (pygame.time.get_ticks() - self.timer_start) / 1000
            remain = self.timer - remain
            endGame = True if remain <= 0 else False
            return (remain, endGame)
        return (None, False)

    def loop_events(self):

        hit = False
        miss = False
        clicked = False
        pos = pygame.mouse.get_pos()

        # Handle PyGame events
        for e in pygame.event.get():

            # Handle quit
            if e.type == pygame.QUIT:
                self.loop = False
                break

            _, endGame = self.timerData

            if not endGame:

                # Handle click
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == Constants.LEFTMOUSEBUTTON:

                    # Start timer if not started
                    if self.timer is not None and self.timer_start == 0:
                        self.timer_start = pygame.time.get_ticks()

                    else:
                        # Handle hit/miss
                        clicked = True
                        miss = True
                        for zombie in self.zombies:
                            if zombie.is_hit(pos) == 1:  # Hit
                                hit = True
                                miss = False
                            if zombie.is_hit(pos) == 2:  # Hit but stunned
                                miss = False

                        if hit:
                            self.score.hit()
                        if miss:
                            self.score.miss()

        return (clicked, hit, miss)

    def loop_display(self, clicked, hit, miss):
        gameTime, endGame = self.timerData
        if not gameTime and self.timer:
            gameTime = -1

        # Display bg
        self.screen.blit(self.background, (0, 0))

        # Display zombies
        for zombie in self.zombies:
            holes = [f for f in self.holes if f not in self.used_holes]
            zombie_display = zombie.do_display(holes, self.score.level, not endGame)

            # If new/old hole given
            if len(zombie_display) > 1:
                if zombie_display[1] == 0:  # New hole
                    self.used_holes.append(zombie_display[2])
                else:  # Old hole
                    if zombie_display[2] in self.used_holes:
                        self.used_holes.remove(zombie_display[2])

            # If should display
            if zombie_display[0]:
                # Get pos and display
                pos = zombie.get_hole_pos(not endGame)
                self.screen.blit(zombie.zombie, pos)

        # Hammer
        thisHammer = pygame.transform.rotate(self.mallet.copy(),
                                      (Constants.MALLETROTHIT if clicked else Constants.MALLETROTNORM))
        hammer_x, hammer_y = pygame.mouse.get_pos()
        hammer_x -= thisHammer.get_width() / 5
        hammer_y -= thisHammer.get_height() / 4
        self.screen.blit(thisHammer, (hammer_x, hammer_y))

        # Fade screen if not started or has ended
        if self.timer and (endGame or gameTime == -1):
            overlay = pygame.Surface((Constants.GAMEWIDTH, Constants.GAMEHEIGHT), pygame.SRCALPHA, 32)
            overlay = overlay.convert_alpha()
            overlay.fill((100, 100, 100, 0.9 * 255))
            self.screen.blit(overlay, (0, 0))

        # Debug data for readout
        debug_data = {}

        # Display data readout
        data = self.score.label(timer=gameTime, debug=debug_data, size=(1.5 if endGame else 1))
        self.screen.blit(data, (5, 5))

        # Display hit/miss indicators
        if not endGame:

            # Hit indicator
            if hit:
                self.show_hit = pygame.time.get_ticks()
            if self.show_hit > 0 and pygame.time.get_ticks() - self.show_hit <= Constants.ZOMBIEHITHUD:
                hit_label = self.text.get_label("Hit!", scale=3, color=(255, 50, 0))
                hit_x = (Constants.GAMEWIDTH - hit_label.get_width()) / 2
                hit_y = (Constants.GAMEHEIGHT - hit_label.get_height()) / 2
                self.screen.blit(hit_label, (hit_x, hit_y))
            else:
                self.show_hit = 0

            # Miss indicator
            if miss:
                self.show_miss = pygame.time.get_ticks()
            if self.show_miss > 0 and pygame.time.get_ticks() - self.show_miss <= Constants.ZOMBIEMISSHUD:
                miss_label = self.text.get_label("Miss!", scale=2, color=(0, 150, 255))
                miss_x = (Constants.GAMEWIDTH - miss_label.get_width()) / 2
                miss_y = (Constants.GAMEHEIGHT + miss_label.get_height()) / 2
                self.screen.blit(miss_label, (miss_x, miss_y))
            else:
                self.show_miss = 0

        # Click to start indicator
        if self.timer and gameTime == -1:
            timer_label = self.text.get_label("Click to begin...", scale=2, color=(0, 255, 255))
            timer_x = (Constants.GAMEWIDTH - timer_label.get_width()) / 2
            timer_y = (Constants.GAMEHEIGHT - timer_label.get_height()) / 2
            self.screen.blit(timer_label, (timer_x, timer_y))

        # Time's up indicator
        if self.timer and endGame:
            timer_label_1 = self.text.get_label("Time's up!", scale=3, color=(0, 150, 255))
            timer_label_2 = self.text.get_label("Press space to restart...", scale=2, color=(0, 150, 255))

            timer_x_1 = (Constants.GAMEWIDTH - timer_label_1.get_width()) / 2
            timer_x_2 = (Constants.GAMEWIDTH - timer_label_2.get_width()) / 2

            timer_y_1 = (Constants.GAMEHEIGHT / 2) - timer_label_1.get_height()
            timer_y_2 = (Constants.GAMEHEIGHT / 2)

            self.screen.blit(timer_label_1, (timer_x_1, timer_y_1))
            self.screen.blit(timer_label_2, (timer_x_2, timer_y_2))


    def game_page(self):
        while self.loop:
            clicked, hit, miss = self.loop_events()

            # Do all render
            self.loop_display(clicked, hit, miss)

            # Update display
            self.clock.tick(Constants.GAMEMAXFPS)
            
            pygame.display.flip()
                    
        pygame.quit()
        
        
        
        
        
        
# timer_event = {}
        # #Game logic
        # zombie_matrix = []
        # zombie_rect_list = []
        # for i in range(5):
        #     zombie_matrix.append([])
        #     zombie_rect_list.append([])
        #     for j in range(9):
        #         zombie_matrix[i].append(False)
        #         zombie_rect_list[i].append(zombie.get_rect(center = (93+105*j,83+140*i)))
        # #Set up display utility object
        # timer_object = [pygame.font.SysFont(None, 50)]
        # timer_object.append(timer_object[0].render(time_to_string(time), True, (255, 255, 255)))
        # timer_event["countdown"] = pygame.USEREVENT+len(timer_event)+1
        # pygame.time.set_timer(timer_event["countdown"], 1000)
        # #Start game
        # while True:
        #     #Input and process
        #     mouseclick = False
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return False
        #         if event.type == timer_event["countdown"]:
        #             time -= 1
        #             timer_object[1] = timer_object[0].render(time_to_string(time), True, (255, 255, 255))
        #             if time == 0:
        #                 pygame.time.set_timer(timer_event["countdown"],0)
        #                 return True
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             mouseclick = True
        #             check = False
        #             for i in range(5):
        #                 for j in range(9):
        #                     if zombie_rect_list[i][j].collidepoint(pygame.mouse.get_pos()) and zombie_matrix[i][j]:
        #                         check = True
        #                         break
        #     # Update display
        #     surface.blit(background,(0,0))
        #     for i in range(5):
        #         for j in range(9):
        #             if zombie_matrix[i][j]:
        #                 surface.blit(zombie,zombie_rect_list[i][j])
        #     if mouseclick: surface.blit(mallet2,mallet2.get_rect(center = (pygame.mouse.get_pos()[0]+40,pygame.mouse.get_pos()[1]-20)))
        #     else: surface.blit(mallet1,mallet1.get_rect(center = (pygame.mouse.get_pos()[0]+40,pygame.mouse.get_pos()[1]-20)))
        #     surface.blit(timer_object[1], timer_object[1].get_rect(center = (900, 750)))
        #     pygame.time.Clock.tick(framerate=60)
        #     pygame.display.flip()