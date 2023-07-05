from enum import Enum
from pygame.math import Vector2

WIN_WIDTH = 800
WIN_HIGHT = 600

FRAME_RATE = 80

# player
DEACCELERATION = 0.95
ROTATION_SPEED = 3
PLAYER_SPEED = 0.4
UP = Vector2(0, -1)

# meteorites
ENEMIES_FREQ = 1000 # ms
OFF_SCREEN = 50

# bullets
BULLET_SPEED = 20

class Mode(Enum):
    START = 0
    RUNNING = 1
    OVER = 2