from enum import Enum
from pygame.math import Vector2

WIN_WIDTH = 800
WIN_HIGHT = 600

FRAME_RATE = 80

# player
DEACCELERATION = 0.95
ROTATION_SPEED = 4
UP = Vector2(0, -0.5)

class Mode(Enum):
    START = 0
    RUNNING = 1
    OVER = 2