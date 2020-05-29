import pygame as pg
from pygame.color import THECOLORS as colors

from config import config

class Menustate:
    def __init__(self, dimensions):
        width, height = dimensions

        # (Button text, name of next state (in Game.states))
        texts = [
            ('Start', 'game'),
            ('Dummy1', 'menu'),
            ('Dummy2', 'menu'),
            ('Exit', None)
        ]


        self.items_group = pg.sprite.Group()
        # self.items is required because sprite groups are unordered
        self.items = []

        # Calculate button positions: centered bot horizontally and vertically, with config.menu_spacing vertical spacing
        menu_height = (len(texts) - 1) * config.menu_spacing + len(texts) * config.menu_height
        current_height = (height - menu_height) / 2
        for text, onclick in texts:
            item = Button((width / 2, current_height), text, onclick)
            self.items.append(item)
            self.items_group.add(item)
            current_height += config.menu_spacing + config.menu_height

        # select first button
        self.select_index = 0
        self.items[0].state = 'selected'

    def render(self, screen):
        self.items_group.draw(screen)

    def process_event(self, event):
        def move_selection(direction):
            self.items[self.select_index].state = 'normal'
            self.select_index = (self.select_index + direction) % len(self.items)
            self.items[self.select_index].state = 'selected'

        selected = self.items[self.select_index]
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                move_selection(-1)
            elif event.key == pg.K_DOWN:
                move_selection(1)
            elif event.key == pg.K_RETURN:
                selected.state = 'clicked'
        elif event.type == pg.KEYUP:
            # the input "RETURN down, UP (the arrow key) down, UP up, RETURN up"
            # should not activate the button, which is why selected.state == 'clicked' is required
            if event.key == pg.K_RETURN and selected.state == 'clicked':
                selected.state = 'selected'
                return selected.onclick

        return 'menu'


class Button(pg.sprite.Sprite):
    def __init__(self, pos, text, onclick):
        super().__init__()

        self.onclick = onclick

        # create a sprite of the size (config.menu_width, config.menu_height) and blit the text onto it
        def render_text(foreground, background):
            surface = pg.Surface((config.menu_width, config.menu_height))
            surface.fill(colors[background])
            # blit text
            textsurface = config.font.render(text, True, colors[foreground])
            textrect = textsurface.get_rect()
            textrect.center = config.menu_width / 2, config.menu_height / 2
            surface.blit(textsurface, textrect)
            return surface

        self.surfaces = {
            'normal': render_text('darkgreen', 'darkgrey'),
            'selected': render_text('darkgreen', 'lightgrey'),
            'clicked': render_text('yellow', 'lightgrey')
        }

        self.current_state = 'normal'

        self.image = self.surfaces[self.current_state]
        self.rect = self.image.get_rect(midtop=pos)


    @property
    def state(self):
        return self.current_state

    @state.setter
    def state(self, value):
        self.image = self.surfaces[value]
        self.current_state = value