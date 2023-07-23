from random import randint
from typing import Any
from pygame import sprite, transform, key, math
import pygame
import data
from utils import load_sprite, load_sound, random_init


class AdvavcedSprite(sprite.Sprite):
    def __init__(self, name: str, scale, pos, vel):
        super().__init__()
        self.scale = scale
        self.pos = math.Vector2(pos)
        self.vel = math.Vector2(vel)
        self.name = name
        self.image = load_sprite("Sprite/" + name, True)
        self.image = transform.rotozoom(self.image, 0, scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = self.image.get_width()//2
        self.rect = self.image.get_rect(center = self.pos)
        
    def _move(self):
        self.pos += self.vel
        self.rect.center = round(self.pos.x), round(self.pos.y)
        
    def _draw(self, surface):
        surface.blit(self.image, self.rect)
        
    # OFF_SCREEN is multiplied by 2. Because if not, the sprite may be destroyed immediately after it is created    
    def _destroy(self):
        if (self.pos.x > data.WIN_WIDTH + 2*data.OFF_SCREEN or self.pos.x < -2*data.OFF_SCREEN) or ( 
            self.pos.y > data.WIN_HIGHT + 2*data.OFF_SCREEN or self.pos.y < -2*data.OFF_SCREEN):
            self.kill()
            
    def update(self, surface):
        self._draw(surface)
        self._move()
        self._destroy()
    
    
class Player(AdvavcedSprite):
    def __init__(self, pos, name="Player_Ships/playerShip3_red", scale=data.PLAYER_SCALE):
        super().__init__(name=name, scale=scale, pos=pos, vel=math.Vector2(0, 0))
        self.image_orig = self.image
        self.empty_image = load_sprite("Sprite/Empty", True)
        self.dir = data.UP * data.PLAYER_SPEED
        self.shoot_sound = load_sound("sfx_laser1")
        self.shield = False
        # blinking
        self.show = True
        self.blink_time = 0
    
    
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
        super()._move()
        
        
    def shoot(self):
        bullet_vel = self.dir * data.BULLET_SPEED + self.vel
        bullet_pos = self.pos + self.dir.normalize() * self.radius
        bullet = Bullet(bullet_pos, bullet_vel)
        self.shoot_sound.play()
        return bullet
    
    def blink(self):
        if self.blink_time == data.PLAYER_BLINK_TIME:
            self.blink_time = 0
            return False
        
        self.show = not self.show
        if not self.show:
            self.image = self.empty_image
        else:
            self.image = self.image_orig
            
        self.blink_time += 1
        return True
        
       
    def __draw(self, surface):
        rotated_surf = transform.rotozoom(self.image, self.dir.angle_to(data.UP), 1.0)
        self.radius = rotated_surf.get_width()//2
        self.mask = pygame.mask.from_surface(rotated_surf)
        self.rect = rotated_surf.get_rect(center = self.pos)
        surface.blit(rotated_surf, self.rect)
        
    def update(self, surface):
        self.__draw(surface)
        self.__input_handle()
        self.__move()
        

class Meteorite(AdvavcedSprite):
    def __init__(self, name="", scale=1, pos=None, vel=None):
        if pos is None or vel is None:
            obst_type = str(randint(1, 4))
            name = "Meteors/meteorBrown_" + obst_type
            pos, vel = random_init()
        else:
            vel.rotate_ip(randint(-180, 180))
            
        super().__init__(name=name, scale=scale, pos=pos, vel=vel)
        
        
    def split(self):
        if self.scale > 0.25:
            return [Meteorite(self.name, self.scale/2, self.pos, self.vel), Meteorite(self.name, self.scale/2, self.pos, self.vel)]
        else:
            return []
        

class Bullet(AdvavcedSprite):
    def __init__(self, pos, vel):
        super().__init__(name="Lasers/laserRed07", scale=0.4, pos=pos, vel=vel)
    
    def __draw(self, surface):   
        rotated_surf = transform.rotozoom(self.image, self.vel.angle_to(math.Vector2(0, -1)), 1.0)
        self.radius = rotated_surf.get_width()//2
        self.mask = pygame.mask.from_surface(rotated_surf)
        self.rect = rotated_surf.get_rect(center = self.pos)
        surface.blit(rotated_surf, self.rect)
    
    def update(self, surface):
        self.__draw(surface)
        self._move()
        self._destroy()


class PlayerStart(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_sprite("Sprite/Player_Ships/playerShip3_red", True)
        self.image = transform.rotozoom(self.image, 0, data.PLAYER_START_SIZE)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        

class PowerUps(AdvavcedSprite):
    def __init__(self, type_power="shield"):
        name = "Power-ups/powerupBlue_" + type_power
        pos = (randint(10, data.WIN_WIDTH - 10), -20)
        vel = data.UP * -1
        self.type = type_power
        super().__init__(name=name, scale=1, pos=pos, vel=vel)
        
    def update(self, surface):
        self._draw(surface)
        self._move()
        self._destroy()

