from pygame.color import THECOLORS as colors

from config import config

class Menustate:
    def render(self, screen):
        self.render_item(screen, 'Hello World')

    def process_event(self, event):
        # Todo here:
        # Check if menu item was clicked
        # Return the new state if it was, else return self.statename
        return self.statename

    def render_item(self, screen, text):
        surf = config.font.render(text, True, colors['green'])
        rect = surf.get_rect()
        rect.topleft = (20, 20)
        screen.blit(surf, rect)
