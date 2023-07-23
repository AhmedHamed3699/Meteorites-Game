from pygame.image import load
from pygame.sprite import collide_mask
from pygame.mixer import Sound
from pygame.transform import rotozoom
from pygame import math
from random import randint, choice
import data

def load_sprite(name: str, alpha=False):     
    sprite = load(f"assets/{name}.png")
    
    if alpha: sprite.convert()
    else: sprite.convert_alpha()
    
    return sprite

def load_sound(name: str):
    sound = Sound(f"assets/Sound/{name}.mp3")
    sound.set_volume(data.SOUND_VOLUME)
    return sound
    
# it is made to get the position and velocity of the meteorite at the beginning of the game
def random_init():
    # I made x1, x2, x and the same for y, 
    # because I wanted to increase the probability of the meteorite appearing in the middle of the screen
    x1 = (choice([-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN]), randint(-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN))
    x2 = (choice([-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN]), randint(-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN))
    x = x1 if abs(x1[1] - data.WIN_HIGHT//2) < abs(x2[1] - data.WIN_HIGHT//2) else x2

    y1 = (randint(-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN), choice([-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN]))
    y2 = (randint(-data.OFF_SCREEN, data.WIN_WIDTH + data.OFF_SCREEN), choice([-data.OFF_SCREEN, data.WIN_HIGHT + data.OFF_SCREEN]))
    y = y1 if abs(y1[0] - data.WIN_WIDTH//2) < abs(y2[0] - data.WIN_WIDTH//2) else y2
    
    c = choice([x,y])
    pos = (c)
    vel = data.UP*1
    
    def rand(start, end, pos):
        return randint(max(start, pos - data.OFF_SCREEN_RANGE), min(end, pos + data.OFF_SCREEN_RANGE)) - pos
    
    if pos[0] < 0:
        vel.update(math.Vector2(0 - pos[0], rand(0,data.WIN_HIGHT, pos[1])))
    elif pos[0] > data.WIN_WIDTH:
        vel.update(math.Vector2(data.WIN_WIDTH - pos[0], rand(0, data.WIN_HIGHT, pos[1])))
    elif pos[1] < 0:
        vel.update(math.Vector2(rand(0, data.WIN_WIDTH, pos[0]), 0 - pos[1]))
    elif pos[1] > data.WIN_HIGHT:
        vel.update(math.Vector2(rand(0, data.WIN_WIDTH, pos[0]), data.WIN_HIGHT - pos[1]))
    
    vel.scale_to_length(1)    
    vel *= randint(data.MIN_SPEED, data.MAX_SPEED)
    
    return pos, vel

def collision_check(sprite, group):
    for target in group:
        if collide_mask(sprite, target):
            return target
    return None

def bullet_collision_check(bullets, obstacles):

    for bullet in bullets:
        for target in obstacles:
            if collide_mask(bullet, target):
                bullet.kill()
                return target
    return None


def print_text(surface, text, font, place='c', pos=(data.WIN_WIDTH//2, data.WIN_HIGHT//2), move=(0,0), color=(255, 255, 255), size=1.0):
    text_surf = font.render(text, True, color)
    text_surf = rotozoom(text_surf, 0, size)
    text_rect = text_surf.get_rect()
    
    if place == 'tl':
        text_rect.topleft = pos
    elif place == 'mt':
        text_rect.midtop = pos
    elif place == 'mb':
        text_rect.midbottom = pos
    else:
        text_rect.center = pos
        
    text_rect.move_ip(move)
        
    surface.blit(text_surf, text_rect)
    
    return text_rect