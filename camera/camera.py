# camera/camera.py
import cv2

class Camera:
    def __init__(self, camera_id=1):
        # Инициализируем камеру
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        self.check_camera()

    def check_camera(self):
        # Проверяем, открылась ли камера успешно
        if not self.cap.isOpened():
            raise ValueError(f"Не удалось подключиться к камере с ID {self.camera_id}")

    def get_frame(self):
        # Захватываем один кадр из потока видео
        ret, frame = self.cap.read()
        if not ret:
            raise IOError("Не удалось захватить изображение с камеры")
        return frame

    def release(self):
        # Освобождаем камеру при закрытии приложения
        self.cap.release()