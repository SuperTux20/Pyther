#!/bin/python3
import pygame as g
from pygame.mixer import music as m, Sound as s
from time import sleep
from sys import argv as args

g.mixer.init()
m.load("sound/music.ogg")
clock = g.time.Clock()
g.font.init()
font = g.font.SysFont("Liberation Mono", 56)


class Colors:
    WHT = (255, 255, 255)
    BLK = (0, 0, 0)
    RED = (255, 0, 0)
    GRN = (0, 255, 0)
    BLU = (0, 0, 255)
    CYN = (0, 255, 255)
    MAG = (255, 0, 255)
    YEL = (255, 255, 0)
    ONG = (255, 127, 0)
    LIM = (127, 255, 0)
    TEL = (0, 255, 127)
    SKY = (0, 127, 255)
    PRP = (127, 0, 255)
    PNK = (255, 0, 127)


class Sounds:
    goal_sound = s("sound/goal.wav")
    win_sound = s("sound/win.wav")
    die_sound = s("sound/die.wav")


class Game:
    # Define game clock, determines max FPS and base game speed
    TICKSPEED = 60

    def __init__(self, title, w, h, the_active_goals, background=None):
        self.title = title
        self.w = w
        self.h = h
        self.active_goals = the_active_goals
        # Create window and fill with color
        self.SCR = g.display.set_mode((w, h))
        self.SCR.fill(Colors.WHT)
        g.display.set_caption(title)
        if background:
            self.bg = g.image.load(background)
        else:
            self.bg = background

    def reset_bg(self):
        self.SCR.fill(Colors.WHT)
        if self.bg:
            self.SCR.blit(self.bg, (0, 0))

    def game_loop(self):
        GAMEOVER = False
        WIN = False
        direction = 1
        try:
            if args[1] == "--debug":
                player = PlayerChar(
                    160,
                    0,
                    64,
                    64,
                    64,
                    "img/player/fwd.png",
                    "img/player/bck.png",
                    "img/player/rgh.png",
                    "img/player/lft.png",
                )
            else:
                player = PlayerChar(
                    160,
                    448,
                    64,
                    64,
                    64,
                    "img/player/fwd.png",
                    "img/player/bck.png",
                    "img/player/rgh.png",
                    "img/player/lft.png",
                )
        except IndexError:
            player = PlayerChar(
                160,
                448,
                64,
                64,
                64,
                "img/player/fwd.png",
                "img/player/bck.png",
                "img/player/rgh.png",
                "img/player/lft.png",
            )
        enemy0 = EnemyChar(8, 320, 64, 64, 2, "img/enemy/rgh.png", "img/enemy/lft.png")
        enemy1 = EnemyChar(8, 192, 64, 64, 3, "img/enemy/rgh.png", "img/enemy/lft.png")
        enemy2 = EnemyChar(8, 64, 64, 64, 4, "img/enemy/rgh.png", "img/enemy/lft.png")
        enemies = [enemy0, enemy1, enemy2]
        goals = []
        if self.active_goals[0]:
            goal0 = GameOBJ(0, 0, 64, 64, 0, "img/treasure.png")
            goals.append(goal0)
        else:
            goals.append(None)
        if self.active_goals[1]:
            goal1 = GameOBJ(80, 0, 64, 64, 0, "img/treasure.png")
            goals.append(goal1)
        else:
            goals.append(None)
        if self.active_goals[2]:
            goal2 = GameOBJ(160, 0, 64, 64, 0, "img/treasure.png")
            goals.append(goal2)
        else:
            goals.append(None)
        if self.active_goals[3]:
            goal3 = GameOBJ(240, 0, 64, 64, 0, "img/treasure.png")
            goals.append(goal3)
        else:
            goals.append(None)
        if self.active_goals[4]:
            goal4 = GameOBJ(320, 0, 64, 64, 0, "img/treasure.png")
            goals.append(goal4)
        else:
            goals.append(None)
        # Main loop, updates all elements
        while not GAMEOVER:
            # Get all events
            for event in g.event.get():
                # Quit if the red X on the corner of the window is clicked
                if event.type == g.QUIT:
                    GAMEOVER = True
                elif event.type == g.KEYDOWN:
                    if event.key == g.K_w or event.key == g.K_UP:
                        direction = 1
                        player.turn(direction)
                    if event.key == g.K_s or event.key == g.K_DOWN:
                        direction = -1
                        player.turn(direction)
                    if event.key == g.K_a or event.key == g.K_LEFT:
                        direction = 2
                        player.turn(direction)
                    if event.key == g.K_d or event.key == g.K_RIGHT:
                        direction = -2
                        player.turn(direction)
                    if event.key == g.K_SPACE:
                        player.move(direction, self.h, self.w)
                        player.draw(self.SCR)
                    if event.key == g.K_q or event.key == g.K_ESCAPE:
                        GAMEOVER = True
            # Fill to prevent sprite cloning
            self.reset_bg()
            # Re-draw sprites
            if self.active_goals[0]:
                goal0.draw(self.SCR)
            if self.active_goals[1]:
                goal1.draw(self.SCR)
            if self.active_goals[2]:
                goal2.draw(self.SCR)
            if self.active_goals[3]:
                goal3.draw(self.SCR)
            if self.active_goals[4]:
                goal4.draw(self.SCR)
            player.draw(self.SCR)
            # Move and re-draw sprites
            enemy0.move(self.w)
            enemy0.draw(self.SCR)
            enemy1.move(self.w)
            enemy1.draw(self.SCR)
            enemy2.move(self.w)
            enemy2.draw(self.SCR)
            # Detect collision
            for i in range(len(enemies)):
                if player.collisionCheck(enemies[i]):
                    GAMEOVER = True
                    WIN = False
                    text = font.render("You lose :(", True, Colors.BLK)
                    self.SCR.blit(text, (0, 192))
                    g.display.update()
                    m.stop()
                    Sounds.die_sound.play()
                    clock.tick(1)
                    break
            for j in range(len(goals)):
                if goals[j]:
                    if player.collisionCheck(goals[j]):
                        GAMEOVER = True
                        WIN = True
                        text = font.render("You win! :)", True, Colors.BLK)
                        self.SCR.blit(text, (0, 192))
                        self.active_goals[j] = False
                        g.display.update()
                        Sounds.goal_sound.play()
                        clock.tick(1)
                        break
                elif (
                    goals[0] == None
                    and goals[1] == None
                    and goals[2] == None
                    and goals[3] == None
                    and goals[4] == None
                ):
                    GAMEOVER = True
                    WIN = False
                    text = font.render("You beat", True, Colors.RED)
                    self.SCR.blit(text, (64, 150))
                    text = font.render("the game!", True, Colors.GRN)
                    self.SCR.blit(text, (64, 200))
                    text = font.render(":D", True, Colors.BLU)
                    self.SCR.blit(text, (160, 250))
                    g.display.update()
                    m.stop()
                    Sounds.win_sound.play()
                    sleep(Sounds.win_sound.get_length())
                    clock.tick(1)
                    break
            # Update screen
            g.display.flip()
            # Tick tock, tick tock...
            clock.tick(self.TICKSPEED)
        if WIN:
            self.game_loop()
        else:
            return


class GameOBJ:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        s,
        imgpath,
        imgpath2=None,
        imgpath3=None,
        imgpath4=None,
    ):
        self.image = imgpath
        self.image2 = imgpath2
        self.image3 = imgpath3
        self.image4 = imgpath4
        self.IMG = g.transform.scale(g.image.load(self.image), (w, h))
        self.OBJ_X = x
        self.OBJ_Y = y
        self.OBJ_W = w
        self.OBJ_H = h
        self.OBJ_S = s

    def draw(self, bg):
        bg.blit(self.IMG, (self.OBJ_X, self.OBJ_Y))


class PlayerChar(GameOBJ):
    def __init__(self, x, y, w, h, s, imgpath, imgpath2, imgpath3, imgpath4):
        super().__init__(x, y, w, h, s, imgpath, imgpath2, imgpath3, imgpath4)

    # Move up or down. - is up, + is down
    def move(self, direction, max_height, max_width):
        if direction == 1:
            self.OBJ_Y -= self.OBJ_S
        elif direction == -1:
            self.OBJ_Y += self.OBJ_S
        elif direction == 2:
            self.OBJ_X -= self.OBJ_S
        elif direction == -2:
            self.OBJ_X += self.OBJ_S
        if self.OBJ_Y >= max_height - 64:
            self.OBJ_Y = max_height - 64
        if self.OBJ_Y <= 0:
            self.OBJ_Y = 0
        if self.OBJ_X >= max_width - 64:
            self.OBJ_X = max_width - 64
        if self.OBJ_X <= 0:
            self.OBJ_X = 0

    def turn(self, direction):
        if direction == 1:
            self.IMG = g.transform.scale(
                g.image.load(self.image), (self.OBJ_W, self.OBJ_H)
            )
        elif direction == -1:
            self.IMG = g.transform.scale(
                g.image.load(self.image2), (self.OBJ_W, self.OBJ_H)
            )
        elif direction == -2:
            self.IMG = g.transform.scale(
                g.image.load(self.image3), (self.OBJ_H, self.OBJ_W)
            )
        elif direction == 2:
            self.IMG = g.transform.scale(
                g.image.load(self.image4), (self.OBJ_H, self.OBJ_W)
            )

    def collisionCheck(self, other_character):
        if (
            self.OBJ_Y > other_character.OBJ_Y + other_character.OBJ_H - 1
            or self.OBJ_Y + self.OBJ_H < other_character.OBJ_Y + 1
        ):
            return False
        if (
            self.OBJ_X > other_character.OBJ_X + other_character.OBJ_W - 1
            or self.OBJ_X + self.OBJ_W < other_character.OBJ_X + 1
        ):
            return False
        return True


class EnemyChar(GameOBJ):
    def __init__(self, x, y, w, h, s, imgpath, imgpath2):
        super().__init__(x, y, w, h, s, imgpath, imgpath2)

    # Move up or down. - is up, + is down
    def move(self, max_width):
        if self.OBJ_X <= -self.OBJ_S:
            self.OBJ_S = abs(self.OBJ_S)
            self.IMG = g.transform.scale(
                g.image.load(self.image), (self.OBJ_W, self.OBJ_H)
            )
        elif self.OBJ_X >= max_width - 72:
            self.OBJ_S = -abs(self.OBJ_S)
            self.IMG = g.transform.scale(
                g.image.load(self.image2), (self.OBJ_W, self.OBJ_H)
            )
        self.OBJ_X += self.OBJ_S
