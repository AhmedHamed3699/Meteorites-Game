from enum import Enum
from pygame.math import Vector2

WIN_WIDTH = 900
WIN_HIGHT = 700

FRAME_RATE = 80

START_COLOR = (7, 33, 73)
RUNNING_COLOR = (3, 10, 20)
OVER_COLOR = (35, 0, 28)
TITLE_COLOR = (16, 79, 50)

PLAYER_START_SIZE = 2

FONT_SIZE = 50

SCORE_DIVIDER = 1000
SCORE_OFFSET = 20
HIGH_SCORE_FILE = "data/high_score.txt"

# player
PLAYER_SCALE = 0.65
DEACCELERATION = 0.95
ROTATION_SPEED = 4
PLAYER_SPEED = 0.4
UP = Vector2(0, -1)

# meteorites
ENEMIES_FREQ = 1500 # ms
OBSTACLES_DEFAULT_SIZE = 1
MAX_SPEED = 3
MIN_SPEED = 1
OFF_SCREEN = 50
OFF_SCREEN_RANGE = 50

# bullets
BULLET_SPEED = 20
SOUND_VOLUME = 0.1

class Mode(Enum):
    START = 0
    RUNNING = 1
    OVER = 2