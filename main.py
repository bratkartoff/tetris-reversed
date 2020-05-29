# ⊥ǝʇɹıs
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg
pg.init()

from pygame.color import THECOLORS as colors

from config import config
from states.Menustate import Menustate
from states.Gamestate import Gamestate

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(config.displaysize)
        self.screen.fill(colors['black'])

        self.states = {
            'menu': Menustate(self.screen.get_size()),
            'game': Gamestate()
        }

        self.current_state = 'menu'

        self.clock = pg.time.Clock()

        pg.time.set_timer(pg.USEREVENT, config.move_delay)

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
                    return
                self.state = self.state.process_event(event)
                if self.state is None:
                    return

            self.screen.fill(colors['black'])
            self.state.render(self.screen)
            pg.display.update()

if __name__ == '__main__':
    Game().mainloop()