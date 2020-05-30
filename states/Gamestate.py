import collections

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
        if event.type == pg.USEREVENT or event.type == pg.KEYUP and event.key == pg.K_SPACE: # Clock tick
            ap.position += (0, -1)
        if ap.check_collision(self.grid) or ap.position.y < 0:
            ap.position = old_position # Reset move
            ap.copy_on(self.grid)
            self.remove_full_rows()
            # Create new piece
            self.active_piece = Piece()
            if self.active_piece.check_collision(self.grid):
                # Game over
                self.reset()
                return 'menu'

        old_position = ap.position
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

        if not ap.check_inside(self.grid):
            if ap.position.x < 0: # left border
                ap.position.x = 0
            else: # right border
                ap.position.x = config.grid[0] - ap.width
        return 'game'

    def remove_full_rows(self):
        # Get full rows
        blocks_per_row = collections.Counter((position.y for position in self.grid.keys()))
        full_rows = set((row for row, count in blocks_per_row.items() if count == self.grid.width))

        # Remove rows
        old = self.grid.copy()
        self.grid.clear()
        for position, value in old.items():
            if position.y not in full_rows:
                self.grid[position + (0, -len([row for row in full_rows if row < position.y]))] = value
