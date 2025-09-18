import os
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720

BASE_SPEED = 5
ENEMY_RADIUS = 40

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")
ENEMY_FOLDER = os.path.join(ASSETS_FOLDER, "enemies_pics")
FINGER_IMAGE = os.path.join(ASSETS_FOLDER, "yassin 105.png")
POP_SOUND = os.path.join(ASSETS_FOLDER, "pop_sound.mp3")

LOGO_IMAGE=os.path.join(ASSETS_FOLDER, "logo.png")

DB_PATH = os.path.join(BASE_DIR, "scores.db")
