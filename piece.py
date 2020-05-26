import pygame
import random
import time
from config import config

WHITE = (255,255,255)
GRAY = (185,185,185)
BLACK = (0,0,0)
RED = (155,0,0)
GREEN = (0,155,0)
BLUE = (0,0,155)
YELLOW = (155,155,0)
ORANGE = (255,165,0)
PURPLE = (148,0,211)

COLORS = (BLUE,GREEN,RED,YELLOW,ORANGE,PURPLE)


S_SHAPE = [['.00',
            '00.',],
          ['0.',
          '00',
          '.0',]]

Z_SHAPE = [['00.',
          '.00',],
          ['.0',
          '00',
          '0.',]]

I_SHAPE = [['0',
            '0',
            '0',
            '0'],
          ['0000']]

O_SHAPE = [['00',
            '00']]

J_SHAPE = [['0..',
            '000'],
            ['00',
             '0.',
             '0.'],
            ['000',
             '..0'],
             ['.0',
              '.0',
              '00']]

L_SHAPE = [['..0',
            '000'],
           ['0.',
            '0.',
            '00'],
           ['000',
            '0..'],
            ['00',
            '.O',
            '.0.']]

T_SHAPE = [['.0.',
            '000'],
           ['0.',
            '00',
            '0.'],
           ['000',
            '.0.'],
           ['.0',
            '00',
            '.0']]

SHAPES = {'S': S_SHAPE,'Z': Z_SHAPE,'J': J_SHAPE,'L': L_SHAPE,'I': I_SHAPE,'O': O_SHAPE,'T': T_SHAPE}

class Piece(object):
    def __init__(self):
        self.color = random.randint(0,5)
        self.position = {'x' : int(config.play_area[1] + 0.5 * config.play_area[1])-35,'y' : config.play_area[0] / 3.5 }
        self.shapeIndex = random.choice(list(SHAPES.keys()))
        self.rotation = random.randint(0,len(SHAPES[self.shapeIndex])-1)
        self.shape = SHAPES[self.shapeIndex][self.rotation]
        self.shapeHeight = len(self.shape)
        self.shapeWidth = len(self.shape[0])

    def setPosition(self,x,y):
        self.position['x'] = x
        self.position['y'] = y

    def setRotation(self,rotation):
        self.rotation = rotation

    """
        field contains the playfield
    """
    def updatePosition(self,x,y,field):
        if self.positionFree(x,y,field):
            self.position['x'] += x
            self.position['y'] += y
            return True
        else:
            return False

    def positionFree(self,deltaX,deltaY,field):
        for y in range(self.shapeHeight):
            for x in range(self.shapeWidth):
                if self.shape[y][x] == '.':
                    continue
                tempX = x + int((self.position['x'] + deltaX)/config.box)
                tempY = y + int((self.position['y'] + deltaY)/config.box)

                if tempX < 0 or tempX >= config.grid[1] or tempY >= config.grid[0]:
                    return False
                #if position used also false

        return True

    def turn(self,field):
        shape = SHAPES[self.shapeIndex][(self.rotation +1)%len(SHAPES[self.shapeIndex])]
        width = len(shape[0])
        rotation = self.rotation
        shape = self.shape
        shapeHeight = self.shapeHeight
        shapeWidth = self.shapeWidth

        self.rotation = (self.rotation+1)%len(SHAPES[self.shapeIndex])
        self.shape = SHAPES[self.shapeIndex][self.rotation]
        self.shapeHeight = len(self.shape)
        self.shapeWidth = len(self.shape[0])

        if (self.position['x'] + width * config.box) <= config.play_area[1] and self.positionFree(0, 0, field):
            pass
        else:
            self.rotation = rotation
            self.shape = shape
            self.shapeWidth = shapeWidth
            self.shapeHeight = shapeHeight

    def draw(self, window):
        for y in range(self.shapeHeight):
            for x in range(self.shapeWidth):
                if self.shape[y][x] != ".":
                    pygame.draw.rect(window, COLORS[self.color], (self.position['x'] + x * config.box, self.position['y'] + y * config.box, config.box, config.box))
