import cv2
import os
import time
import pygame
import numpy as np
from hand_detector import HandDetector
from enemy import Enemy
import config
import database
import scoreboard_gui


pygame.mixer.init()
pop_sound = pygame.mixer.Sound(config.POP_SOUND)

finger_img = cv2.imread(config.FINGER_IMAGE, cv2.IMREAD_UNCHANGED)
finger_img = cv2.resize(finger_img, (120, 120))

enemy_images = []
for filename in os.listdir(config.ENEMY_FOLDER):
    if filename.lower().endswith((".png", ".jpg")):
        path = os.path.join(config.ENEMY_FOLDER, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            img = cv2.resize(img, (120, 120))
            enemy_images.append(img)

cap = cv2.VideoCapture(0)
cap.set(3, config.WINDOW_WIDTH)
cap.set(4, config.WINDOW_HEIGHT)\

cv2.namedWindow("PopShot AR", cv2.WINDOW_NORMAL)
cv2.resizeWindow("PopShot AR", config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

scoreboard_gui.run_scoreboard() 

detector = HandDetector(detectionCon=0.8, trackCon=0.7)
enemies = [Enemy(config.BASE_SPEED, enemy_images) for _ in range(3)]

database.init_db()
high_name, high_score = database.get_high_score()

score = 0
lost = False
lost_time = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not lost:
        img = detector.findHands(img, draw=False)
        lmList = detector.findPosition(img, draw=True, finger_img=finger_img)

        index_tip = None
        for id, x, y in lmList:
            if id == 8:
                index_tip = (x, y)
                break

        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(img)

            if index_tip and enemy.is_popped(index_tip[0], index_tip[1]):
                enemies.remove(enemy)
                score += 1
                new_speed = config.BASE_SPEED + score // 5
                enemies.append(Enemy(new_speed, enemy_images))
                pop_sound.play()
            elif enemy.y < -enemy.radius:
                lost = True
                lost_time = time.time()
                break

        cv2.putText(img, f"Score: {score}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

    else:
        cv2.putText(img, "You Lost!", (300, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

        if score > high_score:
            cv2.imshow("PopShot AR", img)
            cv2.waitKey(2000)
            cap.release()
            cv2.destroyAllWindows()
            player_name = input("New High Score! Enter your name: ")
            database.update_high_score(player_name, score)
            break

        else:
            cv2.putText(img, "Restarting...", (340, 320),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            if time.time() - lost_time > 2:
                score = 0
                enemies = [Enemy(config.BASE_SPEED, enemy_images) for _ in range(3)]
                lost = False

    cv2.imshow("PopShot AR", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
