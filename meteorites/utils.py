from pygame.image import load
from pygame.sprite import collide_mask

def load_sprite(name: str, alpha=False):     
    sprite = load(f"assets/{name}.png")
    
    if alpha: sprite.convert()
    else: sprite.convert_alpha()
    
    return sprite

def collision_check(sprite, group):
    for target in group:
        if collide_mask(sprite, target):
            return True
    return False

def bullet_collision_check(bullets, obstacles):
    for bullet in bullets:
        for target in obstacles:
            if collide_mask(bullet, target):
                bullet.kill()
                target.kill()