import collections
import copy

import pygame as pg
from pygame.color import THECOLORS as colors

from piece import Grid, Piece, to_pixels

class Gamestate:
    font = pg.font.SysFont(None, 40)

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = Grid(10, 20)
        self.active_piece = Piece(self.grid)
        # Score counts down from a high value
        self.score = 999999

    def render(self, screen):
        screen.fill(colors['grey'])

        # Render grid
        grid_surface = pg.Surface(to_pixels((self.grid.width, self.grid.height)))
        self.grid.render(grid_surface)
        self.active_piece.render(grid_surface)
        grid_rect = grid_surface.get_rect()
        grid_rect.midtop = pg.display.get_surface().get_width() / 2, 0
        screen.blit(grid_surface, grid_rect)

        # Render score
        score_surface = self.font.render(f'Score: {self.score}', True, colors['blue'])
        score_rect = score_surface.get_rect()
        score_rect.topleft = 10, 10
        screen.blit(score_surface, score_rect)


    def process_event(self, event):
        ap = self.active_piece # Shortcut

        old = copy.copy(ap)
        if event.type == pg.USEREVENT or event.type == pg.KEYUP and event.key == pg.K_SPACE: # Clock tick
            ap.position += (0, -1)
        if ap.check_collision(self.grid) or ap.position.y < 0:
            old.copy_on(self.grid)
            self.remove_full_rows()
            # Create new piece
            self.active_piece = Piece(self.grid)
            if self.active_piece.check_collision(self.grid):
                # Game over
                self.reset()
                return 'menu'
            return 'game'

        old = copy.copy(ap)
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
            self.active_piece = ap = old # Reset move

        if not ap.check_inside(self.grid):
            if ap.position.x < 0: # left border
                ap.position.x = 0
            else: # right border
                ap.position.x = self.grid.width - ap.grid.width
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

        # Update score
        scores = [0, 40, 100, 300, 1200] # Score values of the original tetris game
        self.score -= scores[len(full_rows)]
