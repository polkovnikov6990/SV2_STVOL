import cv2
import tkinter as tk
import image_processing
import config
import gui

def main():
    # Инициализация видеопотока с камеры
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось подключиться к камере")
        return

    # Создание основного окна приложения
    window = tk.Tk()
    window.title("OCR Application")

    # Создание экземпляра приложения OCRApp
    app = gui.OCRApp(window, cap)

    # Запуск основного цикла обработки событий
    window.mainloop()

    # Освобождение ресурсов камеры при закрытии окна
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()