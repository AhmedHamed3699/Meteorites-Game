from pygame.image import load

def load_sprite(name: str, alpha=False):     
    sprite = load(f"assets/{name}.png")
    
    if alpha: sprite.convert()
    else: sprite.convert_alpha()
    
    return sprite

def collision_check(sprite, group):
    for target in group:
        if sprite.collide(target):
            return True
    return False