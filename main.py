import tkinter as tk
from gui.app_gui import MainApplication

def main():
    root = tk.Tk()
    root.title("Камера")

    # Создаем экземпляр приложения
    app = MainApplication(root)
    app.run()
    
    # Обработчик закрытия окна
    def on_close():
        # Здесь вызовите метод release для камеры
        app.camera.release()
        root.destroy()

    # При закрытии окна будет вызываться функция on_close
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    main()