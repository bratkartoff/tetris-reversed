import pygame as pg

class Config:
    def __init__(self):
        self.font = pg.font.SysFont(None, 20)
        self.displaysize = (800, 600)
        self.play_area = (600,300)
        self.grid = (20,10)
        self.box = 30
        self.fps = 5

config = Config()
