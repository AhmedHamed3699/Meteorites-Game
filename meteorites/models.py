from pygame import sprite, transform, key, math
import pygame
import data
from utils import load_sprite


class AdvavcedSprite(sprite.Sprite):
    def __init__(self, *groups, name: str, scale, pos, vel):
        super().__init__(*groups)
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
    def __init__(self, *groups, pos, name="Player_Ships/playerShip3_red", scale=0.75):
        sprite.GroupSingle(super().__init__(*groups, name=name, scale=scale, pos=pos, vel=math.Vector2(0, 0)))
        self.dir = data.UP
        
    def move(self):
        pressed_keys = key.get_pressed()
        
        if pressed_keys[pygame.K_RIGHT]:
            self.dir.rotate_ip(data.ROTATION_SPEED)
            
        if pressed_keys[pygame.K_LEFT]:
            self.dir.rotate_ip(-1 * data.ROTATION_SPEED)
            
        if pressed_keys[pygame.K_UP]:
            self.vel += self.dir
            
        if pressed_keys[pygame.K_DOWN]:
            self.vel -= self.dir
            
        
        if self.pos.x > data.WIN_WIDTH + self.radius:
            self.pos.x = 0
        elif self.pos.x < 0 - self.radius:
            self.pos.x = data.WIN_WIDTH
            
        if self.pos.y > data.WIN_HIGHT + self.radius:
            self.pos.y = 0
        elif self.pos.y < 0 - self.radius:
            self.pos.y = data.WIN_HIGHT
            
        super().move()
        self.vel *= data.DEACCELERATION
       
    def draw(self, surface):
        rotated_surf = transform.rotozoom(self.image, self.dir.angle_to(math.Vector2(0, -1)), 1.0)
        surface.blit(rotated_surf, self.pos - math.Vector2(rotated_surf.get_width()//2))
        

class Meteorite(AdvavcedSprite):
    pass

class Bullet(AdvavcedSprite):
    pass

class Explosion(sprite.Sprite):
    pass

class MeteoriteExplosion(sprite.Sprite):
    pass

class PlayerExplosion(sprite.Sprite):
    pass


