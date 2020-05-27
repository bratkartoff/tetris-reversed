import pygame as pg
from pygame.color import THECOLORS as colors

from config import config

class Menustate:
    def __init__(self, dimensions):
        width, height = dimensions
        texts = ['Dummy0', 'Dummy1', 'Dummy2','Dummy3']

        menu_height = (len(texts) - 1) * config.menu_spacing + len(texts) * config.menu_height

        self.items = []
        self.items_group = pg.sprite.Group()

        current_height = (height - menu_height) / 2
        for text in texts:
            item = Menuitem((width / 2, current_height), text)
            self.items.append(item)
            self.items_group.add(item)
            current_height += config.menu_spacing + config.menu_height

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
            if event.key == pg.K_RETURN and selected.state == 'clicked':
                selected.state = 'selected'

        # Check if menu item was clicked
        # Return the new state if it was, else return self.statename
        return self.statename


class Menuitem(pg.sprite.Sprite):
    def __init__(self, pos, text):
        super().__init__()

        def render_text(foreground, background):
            surface = pg.Surface((config.menu_width, config.menu_height))
            surface.fill(colors[background])
            # Add text
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
