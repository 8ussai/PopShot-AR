import os
import sys
import time

import cv2
import pygame

import config
import database
from enemy import Enemy
from hand_detector import HandDetector
from scoreboard_gui import Scoreboard
from utils import draw_text, load_image, overlay_image

KEY_ESC, KEY_ENTER, KEY_BACKSPACE = 27, 13, 8
MAX_FAILED_READS = 30

PLAYING, LOST, ENTER_NAME = "playing", "lost", "enter_name"


def load_sound():
    try:
        pygame.mixer.init()
        return pygame.mixer.Sound(config.POP_SOUND)
    except pygame.error as e:
        print(f"Sound disabled: {e}")
        return None


def load_enemy_images():
    images = []
    for filename in sorted(os.listdir(config.ENEMY_FOLDER)):
        if filename.lower().endswith((".png", ".jpg")):
            img = load_image(os.path.join(config.ENEMY_FOLDER, filename), config.ENEMY_SIZE)
            if img is not None:
                images.append(img)
    if not images:
        sys.exit(f"No enemy images found in {config.ENEMY_FOLDER}")
    return images


def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Couldn't open the webcam. Is it connected and not in use by another app?")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    ok, frame = cap.read()
    if not ok:
        cap.release()
        sys.exit("The webcam opened but isn't sending any video.")
    return cap, frame.shape[1], frame.shape[0]


def new_wave(enemy_images, frame_w, frame_h):
    # Space the starting enemies out so they don't arrive together.
    gap = frame_h // config.ENEMY_COUNT
    return [Enemy(config.BASE_SPEED, enemy_images, frame_w, frame_h, i * gap)
            for i in range(config.ENEMY_COUNT)]


def window_closed():
    try:
        return cv2.getWindowProperty(config.WINDOW_TITLE, cv2.WND_PROP_VISIBLE) < 1
    except cv2.error:
        return True


def main():
    database.init_db()
    pop_sound = load_sound()
    finger_img = load_image(config.FINGER_IMAGE, config.FINGER_SIZE)
    enemy_images = load_enemy_images()

    cap, frame_w, frame_h = open_camera()
    cv2.namedWindow(config.WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(config.WINDOW_TITLE, frame_w, frame_h)

    scoreboard = Scoreboard()
    detector = HandDetector()

    state = PLAYING
    score = 0
    enemies = new_wave(enemy_images, frame_w, frame_h)
    lost_time = 0.0
    player_name = ""
    failed_reads = 0
    last_time = time.time()

    try:
        while not scoreboard.closed:
            ok, img = cap.read()
            if not ok:
                failed_reads += 1
                if failed_reads > MAX_FAILED_READS:
                    print("Lost the webcam feed.")
                    break
                scoreboard.pump()
                continue
            failed_reads = 0
            img = cv2.flip(img, 1)

            now = time.time()
            dt = min(now - last_time, 0.1)  # cap so a slow frame doesn't teleport enemies
            last_time = now

            if state == PLAYING:
                tips = detector.find_index_tips(img)

                for enemy in enemies[:]:
                    enemy.move(dt)
                    if any(enemy.is_popped(x, y) for x, y in tips):
                        enemies.remove(enemy)
                        score += 1
                        speed = config.BASE_SPEED + (score // config.POPS_PER_LEVEL) * config.SPEED_STEP
                        enemies.append(Enemy(speed, enemy_images, frame_w, frame_h))
                        if pop_sound:
                            pop_sound.play()
                    elif enemy.escaped():
                        state, lost_time = LOST, now

                for enemy in enemies:
                    enemy.draw(img)
                if finger_img is not None:
                    for x, y in tips:
                        overlay_image(img, finger_img, x - config.FINGER_SIZE // 2,
                                      y - config.FINGER_SIZE // 2)

                draw_text(img, f"Score: {score}", (40, 70), 2, (255, 255, 255), 3)

            elif state == LOST:
                draw_text(img, "You Lost!", (frame_w // 2, frame_h // 2 - 40), 3, (0, 0, 255), 5, center=True)
                draw_text(img, f"Score: {score}", (frame_w // 2, frame_h // 2 + 30), 1.5,
                          (255, 255, 255), 3, center=True)
                if now - lost_time > config.LOST_SCREEN_SECONDS:
                    if database.makes_scoreboard(score):
                        state, player_name = ENTER_NAME, ""
                    else:
                        state, score = PLAYING, 0
                        enemies = new_wave(enemy_images, frame_w, frame_h)

            elif state == ENTER_NAME:
                cx, cy = frame_w // 2, frame_h // 2
                draw_text(img, f"New top score: {score}!", (cx, cy - 80), 1.6, (0, 215, 255), 3, center=True)
                draw_text(img, "Type your name:", (cx, cy - 20), 1.2, (255, 255, 255), 2, center=True)
                cursor = "_" if int(now * 2) % 2 == 0 else " "
                draw_text(img, player_name + cursor, (cx, cy + 50), 1.6, (255, 255, 255), 3, center=True)
                draw_text(img, "Enter = save   Esc = skip", (cx, cy + 110), 0.9, (200, 200, 200), 2, center=True)

            cv2.imshow(config.WINDOW_TITLE, img)
            key = cv2.waitKey(1) & 0xFF

            if state == ENTER_NAME:
                if key == KEY_ENTER:
                    database.add_score(player_name.strip() or "Player", score)
                    scoreboard.refresh()
                if key in (KEY_ENTER, KEY_ESC):
                    state, score = PLAYING, 0
                    enemies = new_wave(enemy_images, frame_w, frame_h)
                    last_time = time.time()
                elif key == KEY_BACKSPACE:
                    player_name = player_name[:-1]
                elif 32 <= key <= 126 and len(player_name) < config.MAX_NAME_LENGTH:
                    player_name += chr(key)
            elif key == KEY_ESC:
                break

            if window_closed():
                break
            scoreboard.pump()
    finally:
        cap.release()
        detector.close()
        cv2.destroyAllWindows()
        if not scoreboard.closed:
            scoreboard.destroy()
        pygame.mixer.quit()


if __name__ == "__main__":
    main()
