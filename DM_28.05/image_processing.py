import cv2
from PIL import Image
import numpy as np


def set_sharpness(cap, sharpness_value):
    if not cap.set(cv2.CAP_PROP_SHARPNESS, sharpness_value):
        print("Не удалось установить резкость камеры")

def capture_image(cap, x1, y1, x2, y2):
    ret, frame = cap.read()
    if ret:
        cropped_frame = frame[y1:y2, x1:x2]
        cv2.imwrite('captured_frame.jpg', cropped_frame)
        return cropped_frame
    return None

def convert_to_bw(image_path):
    img = Image.open(image_path)
    img_bw = img.convert('L')
    img_bw_cv = np.array(img_bw)
    img_bw.save('captured_frame_bw.jpg')
    return img_bw_cv

def apply_threshold(img_bw_cv, threshold_value):
    _, img_bw_threshold = cv2.threshold(img_bw_cv, threshold_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite('captured_frame_bw_threshold.jpg', img_bw_threshold)
    return img_bw_threshold