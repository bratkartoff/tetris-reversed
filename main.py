# ⊥ǝʇɹıs
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg
pg.init()

from pygame.color import THECOLORS as colors

from states.Menustate import Menustate
from states.Gamestate import Gamestate
from states.Highscore import Highscore

class Game:
    fps = 60
    move_delay = 300
    displaysize = 800, 600

    def __init__(self):
        self.screen = pg.display.set_mode(self.displaysize)
        self.screen.fill(colors['black'])

        # name for state: object responsible for handling the state
        # the object must have these methods
        # render(screen): draw something on the screen
        # process_event(event) -> name of the next state: process a pygame event
        self.states = {
            'menu': Menustate(self.screen.get_size()),
            'game': Gamestate(),
            'highscore': Highscore()
        }

        self.current_state = 'menu'

        self.clock = pg.time.Clock()

        pg.time.set_timer(pg.USEREVENT, self.move_delay)

    @property
    def state(self):
        return self.states.get(self.current_state)

    @state.setter
    def state(self, value):
        self.current_state = value

    def mainloop(self):
        while True:
            dt = self.clock.tick(self.fps)

            # Process events
            events = pg.event.get()
            for event in events:
                if event == pg.QUIT:
                    return
                # Process event and possibly change state
                self.state = self.state.process_event(event)
                # exit game
                if self.state is None:
                    return

            self.screen.fill(colors['black'])
            self.state.render(self.screen)
            pg.display.update()

if __name__ == '__main__':
    Game().mainloop()