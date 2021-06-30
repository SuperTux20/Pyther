# Pygame Frogger-like "Pyther"

# Set up display

# Import pygame
import pygame as g

# Define height, width, and name
SCR_NAME = "Pyther"
SCR_W = 384
SCR_H = 512

# Define colors
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

clock = g.time.Clock()
g.font.init()
font = g.font.SysFont('Liberation Mono', 56)

class Game:
    # Define game clock, determines max FPS and base game speed
    TICKSPEED = 60

    def __init__(self, title, w, h, activeGoals, bgPath=None):
        self.title = title
        self.w = w
        self.h = h
        self.aGs = activeGoals

        # Create window and fill with color
        self.SCR = g.display.set_mode((w, h))
        self.SCR.fill(WHT)
        g.display.set_caption(title)
        if bgPath:
            self.bg = g.image.load(bgPath)
        else:
            self.bg = bgPath

    def resetBG(self):
        self.SCR.fill(WHT)
        if self.bg:
            self.SCR.blit(self.bg, (0, 0))
    
    def gameLoop(self):
        GAMEOVER = False
        WIN = False
        direction = 1

        player = PlayerChar(160, 448, 64, 64, 64, 'player-fwd.png', 'player-bck.png', 'player-rgh.png', 'player-lft.png')
        enemy0 = EnemyChar(8, 320, 64, 64, 2, 'enemy-rgh.png', 'enemy-lft.png')
        enemy1 = EnemyChar(8, 192, 64, 64, 3, 'enemy-rgh.png', 'enemy-lft.png')
        enemy2 = EnemyChar(8, 64, 64, 64, 4, 'enemy-rgh.png', 'enemy-lft.png')
        enemies = [enemy0, enemy1, enemy2]
        goals = []
        if self.aGs[0]:
            goal0 = GameOBJ(0, 0, 64, 64, 0, 'treasure.png')
            goals.append(goal0)
        else:
            goals.append(None)
        if self.aGs[1]:
            goal1 = GameOBJ(80, 0, 64, 64, 0, 'treasure.png')
            goals.append(goal1)
        else:
            goals.append(None)
        if self.aGs[2]:
            goal2 = GameOBJ(160, 0, 64, 64, 0, 'treasure.png')
            goals.append(goal2)
        else:
            goals.append(None)
        if self.aGs[3]:
            goal3 = GameOBJ(240, 0, 64, 64, 0, 'treasure.png')
            goals.append(goal3)
        else:
            goals.append(None)
        if self.aGs[4]:
            goal4 = GameOBJ(320, 0, 64, 64, 0, 'treasure.png')
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
            self.resetBG()
                
            # Re-draw sprites
            if self.aGs[0]:
                goal0.draw(self.SCR)
            if self.aGs[1]:
                goal1.draw(self.SCR)
            if self.aGs[2]:
                goal2.draw(self.SCR)
            if self.aGs[3]:
                goal3.draw(self.SCR)
            if self.aGs[4]:
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
                    text = font.render('You lose :(', True, BLK)
                    self.SCR.blit(text, (0, 192))
                    g.display.update()
                    clock.tick(1)
                    break
            for j in range(len(goals)):
                if goals[j]:
                    if player.collisionCheck(goals[j]):
                        GAMEOVER = True
                        WIN = True
                        text = font.render('You win! :)', True, BLK)
                        self.SCR.blit(text, (0, 192))
                        self.aGs[j] = False
                        g.display.update()
                        clock.tick(1)
                        break
                elif goals[0] == None and goals[1] == None and goals[2] == None and goals[3] == None and goals[4] == None:
                    GAMEOVER = True
                    WIN = False
                    text = font.render('You beat', True, RED)
                    self.SCR.blit(text, (64, 150))
                    text = font.render('the game!', True, GRN)
                    self.SCR.blit(text, (64, 200))
                    text = font.render(':D', True, BLU)
                    self.SCR.blit(text, (160, 250))
                    g.display.update()
                    clock.tick(1)
                    break
            
            # Update screen
            g.display.flip()

            # Tick tock, tick tock...
            clock.tick(self.TICKSPEED)

        if WIN:
            self.gameLoop()
        else:
            return

class GameOBJ:
    def __init__(self, x, y, w, h, s, imgpath, imgpath2=None, imgpath3=None, imgpath4=None,):
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
    def move(self, direction, maxH, maxW):
        if direction == 1:
            self.OBJ_Y -= self.OBJ_S
        elif direction == -1:
            self.OBJ_Y += self.OBJ_S
        elif direction == 2:
            self.OBJ_X -= self.OBJ_S
        elif direction == -2:
            self.OBJ_X += self.OBJ_S
        
        if self.OBJ_Y >= maxH - 64:
            self.OBJ_Y = maxH - 64
        if self.OBJ_Y <= 0:
            self.OBJ_Y = 0

        if self.OBJ_X >= maxW - 64:
            self.OBJ_X = maxW - 64
        if self.OBJ_X <= 0:
            self.OBJ_X = 0            
            
    def turn(self, direction):
        if direction == 1:
            self.IMG = g.transform.scale(g.image.load(self.image), (self.OBJ_W, self.OBJ_H))
        elif direction == -1:
            self.IMG = g.transform.scale(g.image.load(self.image2), (self.OBJ_W, self.OBJ_H))
        elif direction == -2:
            self.IMG = g.transform.scale(g.image.load(self.image3), (self.OBJ_H, self.OBJ_W))
        elif direction == 2:
            self.IMG = g.transform.scale(g.image.load(self.image4), (self.OBJ_H, self.OBJ_W))

    def collisionCheck(self, otherChar):
        if self.OBJ_Y > otherChar.OBJ_Y + otherChar.OBJ_H - 1:
            return False
        elif self.OBJ_Y + self.OBJ_H < otherChar.OBJ_Y + 1:
            return False
        
        if self.OBJ_X > otherChar.OBJ_X + otherChar.OBJ_W - 1:
            return False
        elif self.OBJ_X + self.OBJ_W < otherChar.OBJ_X + 1:
            return False
        
        return True

class EnemyChar(GameOBJ):
    
    def __init__(self, x, y, w, h, s, imgpath, imgpath2):
        super().__init__(x, y, w, h, s, imgpath, imgpath2)



    # Move up or down. - is up, + is down
    def move(self, maxW):
        if self.OBJ_X <= -self.OBJ_S:
            self.OBJ_S = abs(self.OBJ_S)
            self.IMG = g.transform.scale(g.image.load(self.image), (self.OBJ_W, self.OBJ_H))
        elif self.OBJ_X >= maxW - 72:
            self.OBJ_S = -abs(self.OBJ_S)
            self.IMG = g.transform.scale(g.image.load(self.image2), (self.OBJ_W, self.OBJ_H))
        self.OBJ_X += self.OBJ_S

# Initialize pygame
g.init()

# Start a new game. The array of Trues determined which treasure chests are enabled.
newGame = Game(SCR_NAME, SCR_W, SCR_H, [True, True, True, True, True], 'bg.png')
newGame.gameLoop()

g.quit()
