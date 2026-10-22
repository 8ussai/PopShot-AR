import cv2


def load_image(path, size):
    """Load an image (keeping transparency) resized to size x size. Returns None if it can't be read."""
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return cv2.resize(img, (size, size))


def overlay_image(bg, overlay, x, y):
    """Draw overlay onto bg with its top-left corner at (x, y).

    Parts that fall outside bg are cut off, so images stay visible
    while partly off-screen.
    """
    bh, bw = bg.shape[:2]
    h, w = overlay.shape[:2]
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + w, bw), min(y + h, bh)
    if x1 >= x2 or y1 >= y2:
        return bg

    part = overlay[y1 - y:y2 - y, x1 - x:x2 - x]
    roi = bg[y1:y2, x1:x2]
    if part.shape[2] == 4:
        alpha = part[:, :, 3:4] / 255.0
        roi[:] = (1 - alpha) * roi + alpha * part[:, :, :3]
    else:
        roi[:] = part[:, :, :3]
    return bg


def draw_text(img, text, org, scale, color, thickness, center=False):
    """Draw text with a dark outline so it reads on any camera background."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    if center:
        (tw, _), _ = cv2.getTextSize(text, font, scale, thickness)
        org = (org[0] - tw // 2, org[1])
    cv2.putText(img, text, org, font, scale, (0, 0, 0), thickness + 4, cv2.LINE_AA)
    cv2.putText(img, text, org, font, scale, color, thickness, cv2.LINE_AA)
