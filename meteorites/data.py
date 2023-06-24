from enum import Enum
from pygame.math import Vector2

WIN_WIDTH = 800
WIN_HIGHT = 600

FRAME_RATE = 60

# player
DEACCELERATION = 0.95
ROTATION_SPEED = 4

class Mode(Enum):
    START = 0
    RUNNING = 1
    OVER = 2