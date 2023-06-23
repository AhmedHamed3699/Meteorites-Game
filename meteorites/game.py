import pygame
from sys import exit
import data
from utils import load_sprite
import models

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((data.WIN_WIDTH, data.WIN_HIGHT))
        pygame.display.set_caption("Meteorites")
        self.clock = pygame.time.Clock()
        self.mode = data.Mode.START
        self.background = pygame.surface.Surface((data.WIN_WIDTH, data.WIN_HIGHT))
        self.background.fill((58, 46, 63))
        self.font = pygame.font.Font("assets/Font/kenvector_future.ttf", 28)
        self.start_text = self.font.render("Press SPACE to start", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center = (data.WIN_WIDTH//2, data.WIN_HIGHT//2))
        self.__load_sprites()
        
    def __load_sprites(self):
        self.player = models.Player()
        
    def main_loop(self):
        while True:
            self.__input_handle()
            
            if self.mode == data.Mode.RUNNING:
                self.__game_logic()
            elif self.mode == data.Mode.OVER:
                self.__over_menu()
            
            self.__update_screen()
                
            
    def __input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.mode == data.Mode.START:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.mode = data.Mode.RUNNING
    
    def __game_logic(self):
        self.background.fill((0, 0, 0))
    
    def __over_menu(self):
        self.background.fill((118, 38, 0))
    
    def __update_screen(self):
        self.screen.blit(self.background, (0,0))
        
        if self.mode == data.Mode.START:
            self.screen.blit(self.start_text, self.start_text_rect)
            
        elif self.mode == data.Mode.RUNNING:
            self.player.draw(self.screen)
            
        pygame.display.update()
        self.clock.tick(data.FRAME_RATE)
        
    
        
                