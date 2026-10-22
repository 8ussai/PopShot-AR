import os

# Size we ask the camera for. Webcams may give a different size,
# so the game always uses the real frame size from the camera.
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
WINDOW_TITLE = "PopShot AR"

# Speeds are in pixels per second, so the game plays the same on fast and slow PCs.
BASE_SPEED = 150
SPEED_STEP = 30          # added for every POPS_PER_LEVEL pops
POPS_PER_LEVEL = 5
ENEMY_COUNT = 3
ENEMY_SIZE = 120
POP_DISTANCE = 60        # fingertip within this many pixels of an enemy's center pops it
FINGER_SIZE = 120

LOST_SCREEN_SECONDS = 2
MAX_NAME_LENGTH = 12
SCOREBOARD_ROWS = 4

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")
ENEMY_FOLDER = os.path.join(ASSETS_FOLDER, "enemies_pics")
FINGER_IMAGE = os.path.join(ASSETS_FOLDER, "yassin_105.png")
POP_SOUND = os.path.join(ASSETS_FOLDER, "pop_sound.mp3")
LOGO_IMAGE = os.path.join(ASSETS_FOLDER, "logo.png")

FONTS_FOLDER = os.path.join(BASE_DIR, "fonts")
FONTS_CACHE = os.path.join(FONTS_FOLDER, "_extracted")

DB_PATH = os.path.join(BASE_DIR, "scores.db")
