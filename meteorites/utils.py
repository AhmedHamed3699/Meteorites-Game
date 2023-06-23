from pygame.image import load

def load_sprite(name: str, alpha=False):     
    sprite = load(f"../assets/sprite/{name}.png")
    
    if alpha: sprite.convert()
    else: sprite.convert_alpha()
    
    return sprite