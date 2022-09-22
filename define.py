import pygame
from random import randint, choice

class TextConstants:

    TEXTTITLE       = "Zombie Wacking"
    TEXTFONTSIZE    = 15
    TEXTFONTFILE    = "image/font.ttf"

class GameConstants:
    GAMEWIDTH      = 1280
    GAMEHEIGHT     = 900
    GAMEMAXFPS     = 60
    FIELDCORDINATE = [((20/1280)*GAMEWIDTH,(0/900)*GAMEHEIGHT),((1240/1280)*GAMEWIDTH,(0/900)*GAMEHEIGHT),((20/1280)*GAMEWIDTH,(850/900)*GAMEHEIGHT),((1240/1280)*GAMEWIDTH,(850/900)*GAMEHEIGHT)]

class LevelConstants:
    LEVELGAP          = 10
    LEVELZOMBIESPEED  = 5
    LEVELZOMBIECHANCE = 50

class ImageConstants:
    IMAGEBASE = "image/"
    IMAGEBACKGROUND = IMAGEBASE + "Background.jpg"
    IMAGEZOMBIE = IMAGEBASE + "Zombie.png"
    IMAGEMALLET = IMAGEBASE + "Mallet.png"
    
class HoleConstants:
    HOLEROWS        = 5
    HOLECOLUMNS     = 9
    HOLEWIDTH       = (GameConstants.FIELDCORDINATE[1][0] - GameConstants.FIELDCORDINATE[0][0]) / HOLEROWS
    HOLEHEIGHT      = (GameConstants.FIELDCORDINATE[2][1] - GameConstants.FIELDCORDINATE[0][1]) / HOLECOLUMNS
    HOLEBASE        = (HOLEHEIGHT+GameConstants.FIELDCORDINATE[0][0]+HOLEHEIGHT/2, HOLEWIDTH+GameConstants.FIELDCORDINATE[0][1]+HOLEWIDTH/2)
    
class ZombieConstants:
    ZOMBIEWIDTH       = int(HoleConstants.HOLEWIDTH*(1/3))
    ZOMBIEHEIGHT      = int(ZOMBIEWIDTH)
    ZOMBIEDEPTH       = 15
    ZOMBIECOOLDOWN    = 500
    
    ZOMBIESTUNNED     = 1000
    ZOMBIEHITHUD      = 500
    ZOMBIEMISSHUD     = 250

    ZOMBIECHANCE      = 1/30
    ZOMBIECOUNT       = 1
    ZOMBIEUPMIN       = 0.3
    ZOMBIEUPMAX       = 2
    
class MalletConstants:
    MALLETWIDTH     = int(HoleConstants.HOLEWIDTH)/1.5
    MALLETHEIGHT    = int(MALLETWIDTH)

    MALLETROTNORM   = -30
    MALLETROTHIT    = 0
    
class Constants(GameConstants, HoleConstants, LevelConstants, ZombieConstants, ImageConstants, MalletConstants):
    LEFTMOUSEBUTTON = 1

class Zombie:

    def __init__(self):
        # Load images
        self.zombie = pygame.image.load(Constants.IMAGEZOMBIE)
        self.zombie = pygame.transform.scale(self.zombie, (Constants.ZOMBIEWIDTH, Constants.ZOMBIEHEIGHT))

        # State of showing animation
        # 0 = No, 1 = Doing Up, -1 = Doing Down
        self.showing_state = 0

        # Hold timestamp for staying up
        self.showing_counter = 0

        # Hold how long zombie will stay up
        self.show_time = 0

        # Our current hole data
        self.current_hole = (0, 0)
        self.last_hole = (0, 0)

        # Current frame of showing animation
        self.show_frame = 0

        # Total number of frames to show for popping up (not timed)
        self.frames = 5

        # Cooldown from last popup
        self.cooldown = 0

        # Indicates if zombie is hit
        # False = Not hit, timestamp for stunned freeze
        self.hit = False

    def chance(self, level):
        level -= 1  # Start at 0

        levelChance = 1 + ((Constants.LEVELZOMBIECHANCE / 100) * level)

        chance = int((Constants.ZOMBIECHANCE ** -1) * levelChance)
        return chance

    def timeLimits(self, level):
        level -= 1  # Start at 0

        levelTime = 1 - ((Constants.LEVELZOMBIESPEED / 100) * level)
        if levelTime < 0: levelTime = 0  # No wait, just up & down

        timeMin = int(Constants.ZOMBIEUPMIN * 1000 * levelTime)
        timeMax = int(Constants.ZOMBIEUPMAX * 1000 * levelTime)

        return (timeMin, timeMax)

    def do_display(self, holes, level, do_tick=True):
        # If in cooldown
        if self.cooldown != 0:
            if pygame.time.get_ticks() - self.cooldown < Constants.ZOMBIECOOLDOWN:
                return [False]
            else:
                self.cooldown = 0
                return [False, 1, self.last_hole]

        # If doing a tick
        if do_tick:

            # Random choice if not showing
            new_hole = False
            if self.showing_state == 0 and holes:
                # Reset
                self.show_frame = 0
                self.hit = False

                # Pick
                random = randint(0, self.chance(level))
                if random == 0:
                    self.showing_state = 1
                    self.showing_counter = 0

                    self.show_time = randint(*self.timeLimits(level))

                    # Pick a new hole, don't pick the last one, don't infinite loop
                    self.current_hole = self.last_hole
                    if len(holes) > 1 or self.current_hole != holes[0]:
                        while self.current_hole == self.last_hole:
                            self.current_hole = choice(holes)
                        self.last_hole = self.current_hole
                        new_hole = True

            # Show as popped up for a bit
            if self.showing_state == 1 and self.showing_counter != 0:
                if pygame.time.get_ticks() - self.showing_counter >= self.show_time:
                    self.showing_state = -1
                    self.showing_counter = 0

            # Return if game should display, including new hole data
            if new_hole:
                return [True, 0, self.current_hole]

        # Return if game should display
        return [(not self.showing_state == 0)]

    def get_base_pos(self):
        holeX, holeY = self.current_hole
        offset = (Constants.HOLEWIDTH - Constants.ZOMBIEWIDTH) / 2

        zombieX = holeX + offset
        zombieY = (holeY + Constants.HOLEHEIGHT) - (Constants.ZOMBIEHEIGHT * 1.2)
        return (zombieX, zombieY)

    def get_hole_pos(self, do_tick=True):
        zombieX, zombieY = self.get_base_pos()

        frame = 0

        # Stunned
        if self.hit != False:
            if pygame.time.get_ticks() - self.hit >= Constants.ZOMBIESTUNNED:
                # Unfrozen after hit, hide
                if self.showing_state != 0:
                    self.showing_state = -1
            else:
                # Frozen from hit
                do_tick = False

        # Going Up
        if self.showing_state == 1:
            if self.show_frame <= self.frames:
                frame = Constants.ZOMBIEDEPTH / self.frames * (self.frames - self.show_frame)
                if do_tick: self.show_frame += 1
            else:
                # Hold
                if self.showing_counter == 0:
                    self.showing_counter = pygame.time.get_ticks()

        # Going Down
        if self.showing_state == -1:
            if do_tick: self.show_frame -= 1
            if self.show_frame >= 0:
                frame = Constants.ZOMBIEDEPTH / self.frames * (self.frames - self.show_frame)
            else:
                # Reset
                self.showing_state = 0
                frame = Constants.ZOMBIEDEPTH
                # Begin cooldown
                if do_tick: self.cooldown = pygame.time.get_ticks()

        zombieY += (Constants.ZOMBIEHEIGHT * (frame / 100))

        return (zombieX, zombieY)

    def is_hit(self, pos):
        mouseX, mouseY = pos

        # Top Left
        zombieX1, zombieY1 = self.get_hole_pos(False)
        # Bottom Right
        zombieX2, zombieY2 = (zombieX1 + Constants.ZOMBIEWIDTH, zombieY1 + Constants.ZOMBIEHEIGHT)

        # Check is in valid to-be hit state
        if self.showing_state != 0:
            # Check x
            if mouseX >= zombieX1 and mouseX <= zombieX2:
                # Check y
                if mouseY >= zombieY1 and mouseY <= zombieY2:
                    # Check is not stunned
                    if self.hit is False:
                        self.hit = pygame.time.get_ticks()
                        return 1
                    else:
                        return 2
        return False
        
class Text:
    def font(self, size):
        # f = font.SysFont("monospace", int(size))
        f = pygame.font.Font(TextConstants.TEXTFONTFILE, int(size))
        # Generate test char
        test = f.render("a", 1, (0, 0, 0))
        # Calc line sizes
        line_width = test.get_width()
        return (f, line_width)

    def wrap(self, unsafe, length, break_char):
        safe_lines = []

        # While text needs wrapping
        while len(unsafe) > length:

            # Find closest (to left) break_char from index length
            slash_index = unsafe.rfind(break_char, 0, length)

            # If not found, give up, unbreakable
            if slash_index == -1:
                break

            # Save warpped text and continue looping
            safe_lines.append(unsafe[0:slash_index].strip())
            unsafe = unsafe[slash_index + 1:].strip()

        safe_lines.append(unsafe)
        return safe_lines

    def get_lines(self, string, break_char, width, scale, color):
        # Font Size
        font_size = TextConstants.TEXTFONTSIZE * scale
        font, line_width = self.font(font_size)

        # Get wrapped text
        if width:
            lines = self.wrap(string, width // line_width, break_char)
        else:
            lines = [string]

        # Render font
        labels = []
        for line in lines:
            render = font.render(line, 1, color)
            labels.append(render)

        return labels

    def get_label(self, string, break_char="", *, width=None, height=None, scale=1, color=(255, 255, 0),
                  background=None):
        # Scaling
        if width:
            width = int(width * (scale ** -1))
        if height:
            height = int(height * (scale ** -1))

        # Get labels
        labels = self.get_lines(string, break_char, width, scale, color)

        # Generate blank surface
        if not width:
            width = max([f.get_width() for f in labels])
        if not height:
            height = sum([f.get_height() + 2 for f in labels])
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        if background:
            surface.fill(background)

        # Add lines
        y = 0
        for label in labels:
            surface.blit(label, (0, y))
            y += label.get_height() + 2

        return surface

class Score:
    def __init__(self, text: Text):
        self.hits = 0
        self.misses = 0
        self.text = text

    @property
    def score(self):
        return (self.hits - (self.misses / 2)) * 2

    @property
    def level(self):
        if self.score < 0:
            return 1
        else:
            return int(1 + (self.score // LevelConstants.LEVELGAP))

    @property
    def attempts(self):
        return self.hits + self.misses

    def disp_score(self, timer, debug):
        # Generate hit/miss data
        hits = [self.hits, 0 if self.attempts == 0 else self.hits / self.attempts * 100]
        misses = [self.misses, 0 if self.attempts == 0 else self.misses / self.attempts * 100]

        # Generate score text
        text = "Score: {:,.0f} / Hits: {:,} ({:,.1f}%) / Misses: {:,} ({:,.1f}%) / Level: {:,.0f}".format(
            self.score, hits[0], hits[1], misses[0], misses[1], self.level
        )

        # Display timer
        if timer:
            display = None
            if timer == -1: display = "Click to begin..."
            if timer < 0: timer = 0
            if not display: display = "{:,.0f}s".format(timer)
            text += " / Time Remaining: {}".format(display)

        # Add any extra readout data
        if debug:
            ext_data_comp = []
            for key, val in debug.items():
                ext_data_comp.append("{}: {}".format(key, val))
            ext_data = " / ".join(ext_data_comp)
            text += " / {}".format(ext_data)

        return text

    def label(self, *, timer=None, debug={}, size=1):
        return self.text.get_label(self.disp_score(timer, debug), "/", scale=size,
                                   width=GameConstants.GAMEWIDTH, background=(0, 0, 0, 0.4 * 255))

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1