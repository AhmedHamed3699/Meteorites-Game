from random import randint, choice
from pygame import sprite, transform, key, math
import pygame
import data
from utils import load_sprite


class AdvavcedSprite(sprite.Sprite):
    def __init__(self, name: str, scale, pos, vel):
        super().__init__()
        self.pos = math.Vector2(pos)
        self.vel = math.Vector2(vel)
        self.image = load_sprite("Sprite/" + name, True)
        self.image = transform.scale_by(self.image, scale)
        self.radius = self.image.get_width()//2
        
    def move(self):
        self.pos += self.vel
        
    def draw(self, surface):
        surface.blit(self.image, self.pos - math.Vector2(self.radius))
    
    
class Player(AdvavcedSprite):
    def __init__(self, pos, name="Player_Ships/playerShip3_red", scale=0.75):
        super().__init__(name=name, scale=scale, pos=pos, vel=math.Vector2(0, 0))
        self.dir = data.UP * data.PLAYER_SPEED
    
    
    def __input_handle(self):
        pressed_keys = key.get_pressed()
        
        if pressed_keys[pygame.K_RIGHT]:
            self.dir.rotate_ip(data.ROTATION_SPEED)
            
        if pressed_keys[pygame.K_LEFT]:
            self.dir.rotate_ip(-1 * data.ROTATION_SPEED)
            
        if pressed_keys[pygame.K_UP]:
            self.vel += self.dir
            
        if pressed_keys[pygame.K_DOWN]:
            self.vel -= self.dir
        
        
    def __move(self):
        if self.pos.x > data.WIN_WIDTH + self.radius:
            self.pos.x = 0
        elif self.pos.x < 0 - self.radius:
            self.pos.x = data.WIN_WIDTH
            
        if self.pos.y > data.WIN_HIGHT + self.radius:
            self.pos.y = 0
        elif self.pos.y < 0 - self.radius:
            self.pos.y = data.WIN_HIGHT
            
        self.vel *= data.DEACCELERATION
        super().move()
        
       
    def __draw(self, surface):
        rotated_surf = transform.rotozoom(self.image, self.dir.angle_to(math.Vector2(0, -1)), 1.0)
        surface.blit(rotated_surf, self.pos - math.Vector2(rotated_surf.get_width()//2))
        
    def update(self, surface):
        self.__draw(surface)
        self.__input_handle()
        self.__move()
        

class Meteorite(AdvavcedSprite):
    def __init__(self, scale=1):
        obst_type = str(randint(1, 6))
        name = "Meteors/meteorBrown_" + obst_type
        x = (choice([-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN]), randint(-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN))
        y = (randint(-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN), choice([-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN]))
        c = choice([x,y])
        pos = (c)
        vel = data.UP * randint(2, 5)
        
        if pos[0] < 0:
            vel.rotate_ip(randint(50, 130))
        elif pos[0] > data.WIN_WIDTH:
            vel.rotate_ip(randint(-130, 50))
        elif pos[1] < 0:
            vel.rotate_ip(randint(-40, 40))
        elif pos[1] > data.WIN_HIGHT:
            vel.rotate_ip(randint(120, 240))
            
        super().__init__(name=name, scale=scale, pos=pos, vel=vel)
   
        
    def __destroy(self):
        if (self.pos.x > data.WIN_WIDTH + 2*data.OFF_SCREEN or self.pos.x < -data.OFF_SCREEN) or ( 
            self.pos.y > data.WIN_HIGHT + 2*data.OFF_SCREEN or self.pos.y < -2*data.OFF_SCREEN):
            self.kill()
            
    def update(self, surface):
        self.draw(surface)
        self.move()
        self.__destroy()
        

class Bullet(AdvavcedSprite):
    pass

class Explosion(sprite.Sprite):
    pass

class MeteoriteExplosion(sprite.Sprite):
    pass

class PlayerExplosion(sprite.Sprite):
    pass


