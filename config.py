import pygame as pg

class Config:
    def __init__(self):
        self.font = pg.font.SysFont(None, 20)
        self.displaysize = (800, 600)
        self.fps = 5

config = Config()
