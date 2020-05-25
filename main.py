# ⊥ǝʇɹıs
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg
pg.init()

from pygame.color import THECOLORS as colors

from config import config
from states.Menustate import Menustate

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(config.displaysize)
        self.screen.fill(colors['black'])

        self.states = {
            'menu': Menustate()
        }
        for statename, state in self.states.items():
            state.statename = statename
        self.state = 'menu'

        self.clock = pg.time.Clock()

    @property
    def state(self):
        return self.states.get(self.current_state)

    @state.setter
    def state(self, value):
        self.current_state = value

    def mainloop(self):
        while True:
            dt = self.clock.tick(config.fps)

            # Process events
            events = pg.event.get()
            for event in events:
                if event == pg.QUIT:
                    return False
                self.state = self.state.process_event(event)
                if not self.state:
                    break

            self.state.render(self.screen)
            pg.display.update()

if __name__ == '__main__':
    Game().mainloop()