import collections
import copy
import random

import pygame as pg
from pygame.color import THECOLORS as colors

from piece import Grid, Piece, to_pixels

class Gamestate:
    font = pg.font.SysFont(None, 40)
    font_medium = pg.font.SysFont(None, 30)
    font_small = pg.font.SysFont(None, 25)
    ctr_left = 'Arrow-Left'
    ctr_right = 'Arrow-Right'
    ctr_rotate = 'Arrow-Up/Down'
    # Times between steps for different control modes
    movedelay = { 
        'hard': 100,
        'normal': 300
    }

    def __init__(self, controlmode):
        # Controlmode should be either 'normal' or 'hard' (invert controls)
        self.controlmode = controlmode
        self.reset()

        self.invert_control = False

        # Set timers for different modes
        for i, (mode, delay) in enumerate(self.movedelay.items()):
            pg.time.set_timer(pg.USEREVENT + i, delay)


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

        # Render controls (only in normal mode)
        if self.controlmode == 'normal':
            controls_surface = self.font_medium.render(f'',True,colors['white']) #spacing
            move_left_surface = self.font_medium.render(f'Move left:',True,colors['black'])
            move_right_surface = self.font_medium.render(f'Move right:',True,colors['black'])
            rotate_surface = self.font_medium.render(f'Rotate:',True,colors['black'])
            speed_up_surface = self.font_medium.render(f'Speed Up:',True,colors['black'])        
            move_left_ctr_surface = self.font_small.render(f'{self.ctr_left}',True,colors['blue'])
            move_right_ctr_surface = self.font_small.render(f'{self.ctr_right}',True,colors['blue'])
            rotate_ctr_surface = self.font_small.render(f'{self.ctr_rotate}',True,colors['blue'])
            speed_up_ctr_surface = self.font_small.render(f'Space',True,colors['blue'])

            controls_rect = controls_surface.get_rect()
            controls_rect.topleft = 10,40        
            move_left_rect = move_left_surface.get_rect()
            move_left_rect.topleft = 10,65        
            move_rigth_rect = move_right_surface.get_rect()
            move_rigth_rect.topleft = 10,115         
            rotate_rect = rotate_surface.get_rect()
            rotate_rect.topleft = 10,165        
            speed_up_rect = speed_up_surface.get_rect()
            speed_up_rect.topleft = 10,215

            move_left_ctr_rect = move_left_ctr_surface.get_rect()
            move_left_ctr_rect.topleft = 10,90        
            move_rigth_ctr_rect = move_right_ctr_surface.get_rect()
            move_rigth_ctr_rect.topleft = 10,140         
            rotate_ctr_rect = rotate_ctr_surface.get_rect()
            rotate_ctr_rect.topleft = 10,190        
            speed_up_ctr_rect = speed_up_ctr_surface.get_rect()
            speed_up_ctr_rect.topleft = 10,240                

            screen.blit(controls_surface,controls_rect)
            screen.blit(move_left_surface,move_left_rect)
            screen.blit(move_right_surface,move_rigth_rect)
            screen.blit(rotate_surface,rotate_rect)
            screen.blit(speed_up_surface,speed_up_rect)
            screen.blit(move_left_ctr_surface,move_left_ctr_rect)
            screen.blit(move_right_ctr_surface,move_rigth_ctr_rect)
            screen.blit(rotate_ctr_surface,rotate_ctr_rect)
            screen.blit(speed_up_ctr_surface,speed_up_ctr_rect)


    def process_event(self, event):
        ap = self.active_piece # Shortcut

        old = copy.copy(ap)
        # Check for clock tick
        # Different modes emit different events (see __init__)
        clock_tick = event.type == pg.USEREVENT + list(self.movedelay.keys()).index(self.controlmode)

        if clock_tick and self.controlmode == 'hard' and random.randrange(50) == 0:
            self.invert_control = not self.invert_control # confuse player

        if clock_tick or event.type == pg.KEYUP and event.key == pg.K_SPACE: # move normally or if space is pressed
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
            return self.statename

        old = copy.copy(ap)
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                ap.rotate('left')
            elif event.key == pg.K_DOWN:
                ap.rotate('right')
            elif event.key == pg.K_LEFT:
                ap.position += (-1, 0) if not self.invert_control else (1, 0)
            elif event.key == pg.K_RIGHT:
                ap.position += (1, 0) if not self.invert_control else (-1, 0)
        if ap.check_collision(self.grid):
            self.active_piece = ap = old # Reset move

        if not ap.check_inside(self.grid):
            if ap.position.x < 0: # left border
                ap.position.x = 0
            else: # right border
                ap.position.x = self.grid.width - ap.grid.width
        return self.statename

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
