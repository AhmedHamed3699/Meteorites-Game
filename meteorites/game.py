import pygame
from sys import exit
import data
import utils

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((data.WIN_WIDTH, data.WIN_HIGHT))
        pygame.display.set_caption("Meteorites")
        self.clock = pygame.time.Clock()
        self.mode = data.Mode.STOP
        self.__load_sprites()
        
    def __load_sprites(self):
        self.background = utils.load_sprite("Backgrounds/blue")
        self.background = pygame.transform.scale(self.background, (data.WIN_WIDTH, data.WIN_HIGHT))
        
    def main_loop(self):
        while True:
            self.__input_handle()
            self.__game_logic()
            self.__update_screen()
            
    def __input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
    def __game_logic(self):
        pass
    
    def __update_screen(self):
        self.screen.blit(self.background, (0,0))
        pygame.display.update()
        self.clock.tick(60)
        
                