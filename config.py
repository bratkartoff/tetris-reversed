import pygame as pg

class Config:
    def __init__(self):
        self.menu_font = pg.font.SysFont(None, 100)
        self.score_font = pg.font.SysFont(None, 40)
        self.displaysize = (800, 600)
        self.grid = (10,20)
        self.box = 30
        self.menu_spacing = 50
        self.menu_width = 400
        self.menu_height = 100
        self.fps = 60
        self.move_delay = 300

config = Config()
