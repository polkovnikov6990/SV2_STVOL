import tkinter as tk
from gui import setup_gui
from camera import Camera

def main():
    # Создание объекта камеры, возможно передав сюда конкретный ID устройства
    camera = Camera(camera_id=1)
    
    # Запуск GUI
    root = tk.Tk()
    setup_gui(root, camera)
    root.mainloop()

    # Освобождаем камеру после закрытия окна
    camera.release()

if __name__ == "__main__":
    main()