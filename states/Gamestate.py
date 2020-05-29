import pygame as pg
from pygame.color import THECOLORS as colors

from config import config
from piece import Grid, Piece

class Gamestate:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = Grid(*config.grid)
        self.active_piece = Piece()

    def render(self, screen):
        self.grid.render(screen)
        self.active_piece.render(screen)

    def process_event(self, event):
        ap = self.active_piece # Shortcut
        old_position = ap.position
        if event.type == pg.USEREVENT:
            ap.position += (0, -1)
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                ap.rotate('left')
            elif event.key == pg.K_DOWN:
                ap.rotate('right')
            elif event.key == pg.K_LEFT:
                ap.position += (-1, 0)
            elif event.key == pg.K_RIGHT:
                ap.position += (1, 0)
        if ap.check_collision(self.grid):
            ap.position = old_position
            ap.copy_on(self.grid)
            # Create new piece
            self.active_piece = Piece()
            if self.active_piece.check_collision(self.grid):
                # Game over
                self.reset()
                return 'menu'
        return 'game'