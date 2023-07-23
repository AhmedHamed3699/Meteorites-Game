from sys import exit
from random import choice
from pathlib import Path
from utils import collision_check, bullet_collision_check, print_text, load_sound, load_sprite
import models
import data
import pygame

class Meteorites:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((data.WIN_WIDTH, data.WIN_HIGHT))
        pygame.display.set_caption("Meteorites")
        pygame.display.set_icon(load_sprite("Sprite/icon"))
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.mode = data.Mode.START
        self.background = pygame.surface.Surface((data.WIN_WIDTH, data.WIN_HIGHT))
        self.background.fill(data.START_COLOR)
        
        # fonts
        self.font = pygame.font.Font("assets/Font/kenvector_future.ttf", data.FONT_SIZE)
        self.font2 = pygame.font.Font("assets/Font/AlienRavager.ttf", int(data.FONT_SIZE * 1.5))
        self.font3 = pygame.font.Font("assets/Font/PixelGamingRegular.ttf", int(data.FONT_SIZE * 1.5))
        self.font4 = pygame.font.Font("assets/Font/UglyByte.otf", int(data.FONT_SIZE * 2.3))
        
        # logo at the start
        self.player_start = pygame.sprite.GroupSingle()
        self.player_start.add(models.PlayerStart(pos = (data.WIN_WIDTH//2 - 10, data.WIN_HIGHT//2)))
        
        # player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(models.Player(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
        
        # blinking
        self.change_time = 0
        self.blink = False
        
        # groups
        self.bullets_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()
        self.power_ups_group = pygame.sprite.Group()
        
        # sounds
        self.shieldUp_sound = load_sound("sfx_shieldUp")
        self.shieldDown_sound = load_sound("sfx_shieldDown")
        
        # timers
        self.obstacles_timer = pygame.USEREVENT + 1
        self.power_ups_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacles_timer, data.ENEMIES_FREQ)
        pygame.time.set_timer(self.power_ups_timer, data.POWER_UPS_FREQ) 
          
        # score and high score
        self.score = 0
        self.new_high_score = False
        Path("data").mkdir(exist_ok=True)
        score_file = Path(data.HIGH_SCORE_FILE)
        score_file.touch(exist_ok=True)
        with open(score_file, "r") as f:
            try:
                self.high_score = int(f.readline())
            except:
                self.high_score = 0
            
          
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bullets_group.add(self.player.sprite.shoot())
                if event.type == self.obstacles_timer:
                    self.obstacles_group.add(models.Meteorite(scale=data.OBSTACLES_DEFAULT_SIZE*1))
                if event.type == self.power_ups_timer and choice([True, False, False]):
                    self.power_ups_group.add(models.PowerUps())
                    
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_time = int(pygame.time.get_ticks()//data.SCORE_DIVIDER)
                    self.mode = data.Mode.RUNNING
                        
    
    def __game_logic(self):
        self.background.fill(data.RUNNING_COLOR)

        # score
        current_time = int(pygame.time.get_ticks()//data.SCORE_DIVIDER) - self.start_time
        self.score = current_time
        print_text(self.background, f"Score: {self.score}", self.font, 'tl', (data.SCORE_OFFSET, data.SCORE_OFFSET), size=0.3)

        
        # game gets harder
        data.MAX_SPEED = 3 + self.score//50
        
        # player blinking after hit and was shielded
        if pygame.time.get_ticks() >= self.change_time and self.blink:
            self.change_time = pygame.time.get_ticks() + data.PLAYER_BLINK_DELAY
            if not self.player.sprite.blink():
                self.blink = False
                self.change_time = 0
        
        # collision check for power ups
        power_up = collision_check(self.player.sprite, self.power_ups_group)
        if power_up:
            if power_up.type == "shield":
                self.player.sprite.shield = True
                self.shieldUp_sound.play()
            power_up.kill()
            
        # collision check between obstacles and bullets
        destroyed_obstacle = bullet_collision_check(self.bullets_group, self.obstacles_group)
        if destroyed_obstacle:
            new_obstacles = destroyed_obstacle.split()
            if new_obstacles:
                self.obstacles_group.add(new_obstacles)
            destroyed_obstacle.kill()
        
        # collision check between player and obstacles
        obstacle = collision_check(self.player.sprite, self.obstacles_group)
        if obstacle:
            if self.player.sprite.shield:
                obstacle.kill()
                self.shieldDown_sound.play()
                self.player.sprite.shield = False
                self.blink = True
            elif not self.blink:
                # reseting the game
                self.bullets_group.empty()
                self.obstacles_group.empty()
                self.power_ups_group.empty()
                self.player.empty()
                self.player.add(models.Player(pos = (data.WIN_WIDTH//2, data.WIN_HIGHT//2)))
                
                # checking for new high score
                if(self.score > self.high_score):
                    self.new_high_score = True
                    self.high_score = self.score
                    with open(data.HIGH_SCORE_FILE, "w") as f:
                        f.write(str(self.high_score))
                else:
                    self.new_high_score = False
                
                # game over    
                self.mode = data.Mode.OVER
                self.background.fill(data.OVER_COLOR)

    
    def __update_screen(self):
        self.screen.blit(self.background, (0,0))
        
        if self.mode == data.Mode.START:
            self.player_start.draw(self.screen)
            temp_rect = self.player_start.sprite.rect
            print_text(self.screen, "Meteorites", self.font2, 'mb', temp_rect.midtop, (0,-100), color=data.TITLE_COLOR)
            print_text(self.screen, "Press SPACE to start", self.font4, 'mt', temp_rect.midbottom, (10,60), size = 0.5)
            
        elif self.mode == data.Mode.RUNNING:
            self.obstacles_group.update(self.screen)
            self.power_ups_group.update(self.screen)
            self.bullets_group.update(self.screen)
            self.player.update(self.screen)
            
        else:
            temp_rect = print_text(self.screen, f"GAME OVER", self.font3, color=data.GAME_OVER_COLOR)
            print_text(self.screen, f"Your Score: {self.score}", self.font, 'mt', temp_rect.midbottom, (0,data.SCORE_OFFSET), size=0.5)
            score_text = f"High Score:  {self.high_score}"
            if self.new_high_score:
                score_text = "New " + score_text            
            print_text(self.screen, score_text, self.font, 'mt', (data.WIN_WIDTH//2, data.SCORE_OFFSET), size=0.4)
                     
        pygame.display.update()
        self.clock.tick(data.FRAME_RATE)
        
    
        
                