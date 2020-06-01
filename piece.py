import math
import random

import pygame as pg
from pygame.color import THECOLORS as colors

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

    def render(self, screen):
        for position, block in self.items():
            rect = block.get_rect()
            rect.topleft = to_pixels(position)
            screen.blit(block, rect)


class Piece:
    blocksize = 30

    def __init__(self, game_grid):
        self.shape = random.choice(SHAPES)
        height = len(self.shape)
        width = len(self.shape[0])

        self.grid = Grid(width, height)

        self.block = pg.Surface((self.blocksize, self.blocksize))
        self.block.fill(colors[random.choice(['blue', 'green', 'red', 'yellow', 'orange', 'purple'])])

        # Set initial position (bottom center)
        self.position = Coordinate((game_grid.width - self.grid.width) // 2, game_grid.height - 3)

        for y, column in enumerate(self.shape):
            for x, is_block in enumerate(column):
                if is_block == '0':
                    self.grid[x, y] = self.block

        # Set random rotation
        for _ in range(random.randrange(4)):
            self.rotate('left')

    def check_collision(self, game_grid):
        """Check if any blocks are colliding with existing blocks on the game grid"""
        for offset in self.grid.keys():
            if game_grid[self.position + offset] is not None:
                return True
        return False

    def check_inside(self, game_grid):
        """Return true if all blocks are inside game_grid"""
        for offset in self.grid.keys():
            if not game_grid.inside(self.position + offset):
                return False
        return True

    def rotate(self, direction):
        """
        Rotate the grid and adjust the position in order to rotate around the center of the grid
        'direction' can be either 'left' or 'right'
        """
        h, w = self.grid.height, self.grid.width
        new = Grid(h, w) # The rotated grid

        # Assign blocks to the rotated position on the new grid
        for pos, block in self.grid.items():
            if direction == 'right':
                # - 1 because pos.y = 0 should be mapped to the highest index, which is h - 1
                new[h - pos.y - 1, pos.x] = block
            elif direction == 'left':
                new[pos.y, w - pos.x - 1] = block
            else:
                raise ValueError(direction)

        # the code above just rotates the grid without moving it, which is why the position needs to be adjusted
        # Explanation: think of a rectangle with width > height and rotate it 90 degrees
        # the new topleft corner will be (width - height) / 2 to the right
        # and (width - height) / 2 above (negative y-direction) the old one
        # this is also true for width < height ((width - height) is negative), but we need to use
        # math.trunc to always round the division towards 0 ('//' always rounds down)
        diff = math.trunc((w - h) / 2)
        self.position += diff, -diff

        self.grid = new

    def copy_on(self, game_grid):
        """Copy all blocks to the game_grid"""
        for offset, block in self.grid.items():
            game_grid[self.position + offset] = block

    def render(self, screen):
        for offset, block in self.grid.items():
            rect = block.get_rect()
            rect.topleft = to_pixels(self.position + offset)
            screen.blit(block, rect)


class Coordinate:
    """
    A coordinate behaves almost like a tuple, except that
    (+) adds coordinates and that the members can be accessed with .x and .y"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def convert(cls, other):
        """Convert an iteratable (e. g. a tuple) to a Coordinate"""
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


def to_pixels(coordinate):
    """Convert coordinates in grid blocks to coordinates in pixels"""
    it = iter(coordinate)
    return next(it) * Piece.blocksize, next(it) * Piece.blocksize
