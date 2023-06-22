import pygame
from sys import exit

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Meteorites")
        self.clock = pygame.time.Clock()
        
    def main_loop(self):
        while True:
            self.__input_handle()
            self.__game_logic()
            self.__update_screen
            
    def __input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
    def __game_logic(self):
        pass
    
    def __update_screen(self):
        pygame.display.update()
        self.clock.tick(60)
        
                