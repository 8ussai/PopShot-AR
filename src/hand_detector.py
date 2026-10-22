import cv2
import mediapipe as mp

INDEX_FINGER_TIP = 8


class HandDetector:
    def __init__(self, max_hands=2, detection_con=0.8, track_con=0.7):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con,
        )

    def find_index_tips(self, img):
        """Return the (x, y) pixel position of the index fingertip of every detected hand."""
        h, w = img.shape[:2]
        results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        tips = []
        for hand in results.multi_hand_landmarks or []:
            lm = hand.landmark[INDEX_FINGER_TIP]
            tips.append((int(lm.x * w), int(lm.y * h)))
        return tips

    def close(self):
        self.hands.close()
