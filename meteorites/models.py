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
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = self.image.get_width()//2
        self.rect = self.image.get_rect(center = self.pos)
        
    def _move(self):
        self.pos += self.vel
        self.rect.center = round(self.pos.x), round(self.pos.y)
        
    def _draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def _destroy(self):
        if (self.pos.x > data.WIN_WIDTH + data.OFF_SCREEN or self.pos.x < -data.OFF_SCREEN) or ( 
            self.pos.y > data.WIN_HIGHT + data.OFF_SCREEN or self.pos.y < -data.OFF_SCREEN):
            self.kill()
            
    def update(self, surface):
        self._draw(surface)
        self._move()
        self._destroy()
    
    
class Player(AdvavcedSprite):
    def __init__(self, pos, name="Player_Ships/playerShip3_red", scale=0.65):
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
        super()._move()
        
        
    def shoot(self):
        bullet_vel = self.dir * data.BULLET_SPEED + self.vel
        bullet_pos = self.pos + self.dir.normalize() * self.radius
        bullet = Bullet(bullet_pos, bullet_vel)
        return bullet
        
       
    def __draw(self, surface):
        rotated_surf = transform.rotozoom(self.image, self.dir.angle_to(math.Vector2(0, -1)), 1.0)
        self.radius = rotated_surf.get_width()//2
        self.mask = pygame.mask.from_surface(rotated_surf)
        self.rect = rotated_surf.get_rect(center = self.pos)
        surface.blit(rotated_surf, self.rect)
        
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
        vel = data.UP * randint(2, 4)
        
        if pos[0] < 0:
            vel.rotate_ip(randint(50, 130))
        elif pos[0] > data.WIN_WIDTH:
            vel.rotate_ip(randint(-130, 50))
        elif pos[1] < 0:
            vel.rotate_ip(randint(-40, 40))
        elif pos[1] > data.WIN_HIGHT:
            vel.rotate_ip(randint(120, 240))
            
        super().__init__(name=name, scale=scale, pos=pos, vel=vel)
        

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
        

class Explosion(sprite.Sprite):
    pass

class MeteoriteExplosion(sprite.Sprite):
    pass

class PlayerExplosion(sprite.Sprite):
    pass


