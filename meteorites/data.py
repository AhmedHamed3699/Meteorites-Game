from enum import Enum
from pygame.math import Vector2

WIN_WIDTH = 900
WIN_HIGHT = 700

FRAME_RATE = 80

# colors
START_COLOR = (7, 36, 60)
RUNNING_COLOR = (3, 10, 20)
OVER_COLOR = (35, 0, 28)
TITLE_COLOR = (0, 160, 80)
GAME_OVER_COLOR = (207, 33, 41)

PLAYER_START_SIZE = 2
FONT_SIZE = 50
SOUND_VOLUME = 0.2

# score
SCORE_DIVIDER = 1000
SCORE_OFFSET = 20
HIGH_SCORE_FILE = "data/high_score.txt"

UP = Vector2(0, -1)

# player
PLAYER_SCALE = 0.65
DEACCELERATION = 0.95
ROTATION_SPEED = 4
PLAYER_SPEED = 0.4
PLAYER_BLINK_DELAY = 100
PLAYER_BLINK_TIME = 20

# meteorites
ENEMIES_FREQ = 1500 # ms
OBSTACLES_DEFAULT_SIZE = 1
MAX_SPEED = 3
MIN_SPEED = 1
OFF_SCREEN = 50         # offset from the edge of the screen before the meteorite appears
OFF_SCREEN_RANGE = 50   # range of the offset to get the meteorite to appear in the middle of the screen

# bullets
BULLET_SPEED = 20

# power ups
POWER_UPS_FREQ = 12000 # ms

class Mode(Enum):
    START = 0
    RUNNING = 1
    OVER = 2