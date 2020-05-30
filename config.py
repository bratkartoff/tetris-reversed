import pygame as pg

class Config:
    def __init__(self):
        self.fontsize = 100
        self.font = pg.font.SysFont(None, self.fontsize)
        self.displaysize = (800, 600)
        self.grid = (10,20)
        self.box = 30
        self.menu_spacing = 50
        self.menu_width = 400
        self.menu_height = 100
        self.fps = 60
        self.move_delay = 300

config = Config()
