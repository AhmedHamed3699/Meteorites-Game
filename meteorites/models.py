from pygame import sprite, transform, key, math
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
    def __init__(self, *groups, pos=(data.WIN_WIDTH//2, data.WIN_HIGHT//2), name="Player_Ships/playerShip3_red", scale=0.75):
        sprite.GroupSingle(super().__init__(*groups, name=name, scale=scale, pos=pos, vel=math.Vector2(0, 0)))
        

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


