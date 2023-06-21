import pygame
from sys import exit

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Meteorites")
        
    def main_loop(self):
        while True:
            self._input_handle()
            
    def _input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                