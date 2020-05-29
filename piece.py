import random

import pygame as pg
from pygame.color import THECOLORS as colors

from config import config


SHAPES = [
    ['.00',
     '00.'],

    ['00.',
     '.00'],

    ['0000'],

    ['00',
     '00'],

    ['0..',
     '000'],

    ['..0',
     '000'],

    ['.0.',
     '000'],
]


class Grid(dict):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def __getitem__(self, key):
        return self.get(Coordinate.convert(key))

    def __setitem__(self, key, value):
        super().__setitem__(Coordinate.convert(key), value)

    def inside(self, coordinate):
        return 0 <= coordinate.x < self.width and 0 <= coordinate.y <= self.height

    def __delitem__(self, key):
        try:
            super().__delitem__(Coordinate.convert(key))
        except KeyError:
            pass

    def rotate(self, direction):
        old = self.copy()
        self.clear()
        for position, block in old.items():
            if direction == 'right':
                self[self.height - position.y - 1, position.x] = block
            elif direction == 'left':
                self[position.y, self.width - position.x - 1] = block
            else:
                raise ValueError(direction)

        self.width, self.height = self.height, self.width

    def render(self, screen):
        for position, block in self.items():
            rect = block.get_rect()
            rect.topleft = position.to_pixels()
            screen.blit(block, rect)


class Piece(Grid):
    def __init__(self):
        self.shape = random.choice(SHAPES)
        height = len(self.shape)
        width = len(self.shape[0])

        super().__init__(width, height)

        self.block = pg.Surface((config.box, config.box))
        self.block.fill(colors[random.choice(['blue', 'green', 'red', 'yellow', 'orange', 'purple'])])

        for y, column in enumerate(self.shape):
            for x, is_block in enumerate(column):
                if is_block == '0':
                    self[x, y] = self.block

        # Set random rotation
        for _ in range(random.randrange(4)):
            self.rotate('left')

        # Set initial position (bottom center)
        self.position = Coordinate(config.grid[0] // 2 - self.width // 2, config.grid[1] - 3)


    def check_collision(self, game_grid):
        """Check if any blocks are outside the game grid or colliding with existing blocks there"""
        for offset in self.keys():
            if not game_grid.inside(self.position + offset) or game_grid[self.position + offset] is not None:
                return True
        return False

    def copy_on(self, game_grid):
        """Copy all blocks to the game_grid"""
        for offset, block in self.items():
            game_grid[self.position + offset] = block

    def render(self, screen):
        for offset, block in self.items():
            rect = block.get_rect()
            rect.topleft = (self.position + offset).to_pixels()
            screen.blit(block, rect)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def convert(cls, other):
        """Copy constructor"""
        return cls(*other)

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        it = iter(other)
        return Coordinate(self.x + next(it), self.y + next(it))

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'<Coordinate({self.x}, {self.y}>'

    def to_pixels(self):
        return self.x * config.box, self.y * config.box

