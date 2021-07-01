#!/bin/python3

import pygame as g

SCR_NAME = "Pyther"
SCR_W = 384
SCR_H = 512
g.init()
# Start a new game. The array of Trues determined which treasure chests are enabled.
new_game = __import__(
    "libs"  # Since I only need to use it once, why not import and use in one line?
).Game(
    SCR_NAME,
    SCR_W,
    SCR_H,
    [True, True, True, True, True],
    "img/bg.png",
)
g.mixer.music.play(5760)  # A 15-second audio piece, looping for 24 hours. LMAO
new_game.game_loop()
g.quit()
