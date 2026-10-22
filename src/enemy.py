import random
import math
from utils import overlay_image
import config


class Enemy:
    def __init__(self, speed, enemy_images, frame_w, frame_h, start_delay_px=0):
        self.img = random.choice(enemy_images)
        half = config.ENEMY_SIZE // 2
        margin = min(half + 10, frame_w // 2)
        self.x = random.randint(margin, frame_w - margin)
        # Start just below the bottom edge; start_delay_px pushes it further down
        # so enemies don't all arrive at once.
        self.y = frame_h + half + start_delay_px
        self.speed = speed  # pixels per second

    def move(self, dt):
        self.y -= self.speed * dt

    def draw(self, img):
        h, w = self.img.shape[:2]
        overlay_image(img, self.img, int(self.x) - w // 2, int(self.y) - h // 2)

    def is_popped(self, hand_x, hand_y):
        return math.hypot(self.x - hand_x, self.y - hand_y) < config.POP_DISTANCE

    def escaped(self):
        """True once the enemy has fully left through the top of the screen."""
        return self.y < -config.ENEMY_SIZE // 2
