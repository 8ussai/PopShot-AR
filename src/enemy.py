import random
import math
from utils import overlay_image
import config


class Enemy:
    def __init__(self, speed, enemy_images):
        self.img = random.choice(enemy_images)
        self.x = random.randint(100, config.WINDOW_WIDTH - 100)
        self.y = config.WINDOW_HEIGHT
        self.speed = speed
        self.radius = config.ENEMY_RADIUS

    def move(self):
        self.y -= self.speed

    def draw(self, img):
        h, w = self.img.shape[:2]
        x1, y1 = self.x - w // 2, self.y - h // 2
        overlay_image(img, self.img, x1, y1)

    def is_popped(self, hand_x, hand_y):
        dist = math.hypot(self.x - hand_x, self.y - hand_y)
        return dist < self.radius + 20
