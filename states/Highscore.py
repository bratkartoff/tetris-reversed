"""
@author: Matthias Bremer, Nils Löwen
@Date: 01.06.2020
This Class gets called when the game-engine switches to Highscore-State. It loads if found stored Highscores stored in the highscore.txt and displays the top 10 
Currently showing Test-Data. There is no function to store the last Score, so just Manualy writen scores are getting shown...we simply ran out of time, but we thought maybe it 
still is a nice 'function'-(not a bug), and it is not important for the game to work and just an extra-functionality
"""

import pygame as pg
from pygame.color import THECOLORS as colors
from os import path


class Highscore:
    font = pg.font.SysFont(None, 60)
    font_medium = pg.font.SysFont(None, 40)
    font_small = pg.font.SysFont(None, 25)
    message=""
    highscores = []

    def __init__(self):
        #try to load the Highscores
        try:
            file = open("highscores.txt","r")
            self.highscores = file.readlines()
            file.close()
        except:
            self.message = "No Highscores stored"





    def render(self, screen):
        screen.fill(colors['darkgray'])

        #show this if no highscores are stored
        if self.message!="":
            txt_surf = self.font.render(self.message, True, colors['black'])
            txt_rect = txt_surf.get_rect()
            txt_rect.topleft = (200)-(txt_rect.width/2),10
            title_x = 400-(txt_rect.width/2)
            screen.blit(txt_surf, (title_x,10))
        
        else:
            lines=self.highscores      

            all_score = []
            for line in lines:
                score = int(line.replace('\n',''))
                all_score.append(score)
            all_score.sort(reverse=True)  # sort from largest to smallest
            best = all_score[:10]  # top 10 values

            # render title
            txt_surf = self.font.render("HIGHSCORE", True, colors['black'])  # headline
            txt_rect = txt_surf.get_rect(center=(400//2, 30))
            screen.blit(txt_surf, txt_rect)

            # write the top-10 data
            for i, entry in enumerate(best):
                txt_surf = self.font.render(str(entry), True, colors['black'])
                txt_rect = txt_surf.get_rect(center=(400//2, 30*i+60))
                screen.blit(txt_surf, txt_rect)
    
            


    def process_event(self, event):
        while True:
            # terminate if mouse1 clicked
            pos = pg.mouse.get_pos()
            left, _, _ = pg.mouse.get_pressed()
            if left:
                return 'menu'
            else :
                return 'highscore'


