import cv2
import numpy as np
import os
from PIL import Image

# Глобальная переменная для порогового значения
threshold_value = 128

def update_threshold(val):
    global threshold_value
    threshold_value = int(val)

def capture_image(cropped_frame):
    # Используем функцию вместо глобальных переменных
    cv2.imwrite('captured_frame.jpg', cropped_frame)

def process_captured_image(img_path='captured_frame.jpg'):
    if os.path.exists(img_path):
        # Чтение изображения
        img = Image.open(img_path)
        img_bw = img.convert('L')
        img_bw_cv = np.array(img_bw)  # Преобразование из PIL Image в NumPy массив для OpenCV

        # Применение пороговой обработки
        _, img_bw_threshold = cv2.threshold(img_bw_cv, threshold_value, 255, cv2.THRESH_BINARY)
        return img_bw_threshold
    else:
        raise FileNotFoundError("Файл изображения не найден.")