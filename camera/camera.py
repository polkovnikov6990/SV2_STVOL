import cv2

class Camera:
    def __init__(self, camera_id=1):
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise Exception("Не удалось подключиться к камере")
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Не удалось получить изображение с камеры")
            return None
        return frame
    
    def capture_image(self, path='captured_frame.jpg'):
        frame = self.get_frame()
        if frame is not None:
            # Обрезаем изображение до размеров зеленого прямоугольника
            # Эти значения должны быть переданы или установлены в классе
            cropped_frame = frame[self.y1:self.y2, self.x1:self.x2]
            cv2.imwrite(path, cropped_frame)
    
    def release(self):
        self.cap.release()

if __name__ == "__main__":
    main()