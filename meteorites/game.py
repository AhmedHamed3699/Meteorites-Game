import pygame
from sys import exit
import data
from utils import collision_check, bullet_collision_check
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
        self.bullets_group = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(models.Player(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
        self.obstacles_group = pygame.sprite.Group()
        self.obstacles_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacles_timer, data.ENEMIES_FREQ)

        
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
                    
            elif self.mode == data.Mode.RUNNING:
                if event.type == self.obstacles_timer:
                    self.obstacles_group.add(models.Meteorite())
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bullets_group.add(self.player.sprite.shoot())
                
    
    def __game_logic(self):
        self.background.fill((0, 0, 0))
        bullet_collision_check(self.bullets_group, self.obstacles_group)
        if collision_check(self.player.sprite, self.obstacles_group):
            self.mode = data.Mode.OVER
    
    def __over_menu(self):
        self.background.fill((118, 38, 0))
    
    def __update_screen(self):
        self.screen.blit(self.background, (0,0))
        
        if self.mode == data.Mode.START:
            self.screen.blit(self.start_text, self.start_text_rect)
            
        elif self.mode == data.Mode.RUNNING:
            self.player.update(self.screen)
            self.obstacles_group.update(self.screen)
            self.bullets_group.update(self.screen)
            
        pygame.display.update()
        self.clock.tick(data.FRAME_RATE)
        
    
        
                