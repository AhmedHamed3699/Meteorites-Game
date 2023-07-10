import pygame
from sys import exit
import data
from utils import collision_check, bullet_collision_check, print_text
import models

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((data.WIN_WIDTH, data.WIN_HIGHT))
        pygame.display.set_caption("Meteorites")
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.mode = data.Mode.START
        self.background = pygame.surface.Surface((data.WIN_WIDTH, data.WIN_HIGHT))
        self.background.fill(data.START_COLOR)
        self.font = pygame.font.Font("assets/Font/kenvector_future.ttf", data.FONT_SIZE)
        self.font2 = pygame.font.Font("assets/Font/AlienRavager.ttf", int(data.FONT_SIZE * 1.5))
        self.bullets_group = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(models.Player(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
        self.obstacles_group = pygame.sprite.Group()
        self.obstacles_timer = pygame.USEREVENT + 1
        self.player_start = pygame.sprite.GroupSingle() # the picture of the player at the start
        self.player_start.add(models.PlayerStart(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
        self.score = 0
        pygame.time.set_timer(self.obstacles_timer, data.ENEMIES_FREQ)

        
    def main_loop(self):
        while True:
            self.__input_handle()
            
            if self.mode == data.Mode.RUNNING:
                self.__game_logic()
            
            self.__update_screen()
                
            
    def __input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.mode == data.Mode.RUNNING:
                if event.type == self.obstacles_timer:
                    self.obstacles_group.add(models.Meteorite())
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bullets_group.add(self.player.sprite.shoot())
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_time = int(pygame.time.get_ticks()//data.SCORE_DIVIDER)
                    self.mode = data.Mode.RUNNING
                    
                
    
    def __game_logic(self):
        self.background.fill(data.RUNNING_COLOR)

        current_time = int(pygame.time.get_ticks()//data.SCORE_DIVIDER) - self.start_time
        self.score = current_time
        print_text(self.background, f"Score: {self.score}", self.font, 'tl', (data.SCORE_OFFSET, data.SCORE_OFFSET), size=0.3)
        
        destroyed_obstacle = bullet_collision_check(self.bullets_group, self.obstacles_group)
        if destroyed_obstacle:
            new_obstacles = destroyed_obstacle.split()
            if new_obstacles:
                self.obstacles_group.add(new_obstacles)
            destroyed_obstacle.kill()
            
        if collision_check(self.player.sprite, self.obstacles_group):
            self.bullets_group.empty()
            self.obstacles_group.empty()
            self.player.empty()
            self.player.add(models.Player(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
            self.mode = data.Mode.OVER
            self.background.fill(data.OVER_COLOR)
    
    def __update_screen(self):
        self.screen.blit(self.background, (0,0))
        if self.mode == data.Mode.START:
            self.player_start.draw(self.screen)
            temp_rect = self.player_start.sprite.rect
            print_text(self.screen, "Meteorites", self.font2, 'mb', temp_rect.midtop, (0,-100), color=data.TITLE_COLOR)
            print_text(self.screen, "Press SPACE to start", self.font, 'mt', temp_rect.midbottom, (0,50), size = 0.5)
            
        elif self.mode == data.Mode.RUNNING:
            self.player.update(self.screen)
            self.obstacles_group.update(self.screen)
            self.bullets_group.update(self.screen)
            
        elif self.mode == data.Mode.OVER:
            temp_rect = print_text(self.screen, f"GAME OVER", self.font)
            print_text(self.screen, f"Your Score: {self.score}", self.font, 'mt', temp_rect.midbottom, size=0.5)
            
        pygame.display.update()
        self.clock.tick(data.FRAME_RATE)
        
    
        
                