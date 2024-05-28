import cv2
import tkinter as tk
import image_processing
import config
import gui

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось подключиться к камере")
        return

    image_processing.set_sharpness(cap, config.sharpness_value)

    window = tk.Tk()
    window.title("Камера")

    app = gui.OCRApp(window, cap)
    
    window.mainloop()

if __name__ == "__main__":
    main()