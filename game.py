#!/bin/python3

import pygame as g
from pyther_libs import Game

SCR_NAME = "Pyther"
SCR_W = 384
SCR_H = 512
g.init()
# Start a new game. The array of Trues determined which treasure chests are enabled.
newGame = Game(SCR_NAME, SCR_W, SCR_H, [True, True, True, True, True], "img/bg.png")
g.mixer.music.play(5760)  # A 15-second audio piece, looping for 24 hours. LMAO
newGame.game_loop()
g.quit()
