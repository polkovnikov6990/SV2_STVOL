import sys
import os

# Добавляем директорию, содержащую dm.py, в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from PIL import Image, ImageTk
import cv2
from dm import process_image, perform_ocr, load_excel_data  # Импортируем конкретные функции
from config import x1, y1, x2, y2

class OCRApp:
    def __init__(self, window, cap):
        self.cap = cap
        self.threshold_value = 128

        print("Инициализация GUI...")
        self.create_gui(window)
        print("GUI инициализировано.")
        self.update_image()

    def create_gui(self, window):
        # Создаем Canvas виджеты для каждого фрейма
        self.left_canvas = tk.Canvas(window, width=392, height=402)
        self.left_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.left_canvas.create_rectangle(1, 1, 391, 401, outline="red", width=2)

        self.center_canvas = tk.Canvas(window, width=392, height=402)
        self.center_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.center_canvas.create_rectangle(1, 1, 391, 401, outline="red", width=2)

        self.right_canvas = tk.Canvas(window, width=392, height=402)
        self.right_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.right_canvas.create_rectangle(1, 1, 391, 401, outline="red", width=2)

        # Создаем фреймы внутри Canvas
        self.left_frame = tk.Frame(self.left_canvas, width=390, height=400)
        self.left_frame.place(x=1, y=1)
        print("Created left_frame")

        self.center_frame = tk.Frame(self.center_canvas, width=390, height=400)
        self.center_frame.place(x=1, y=1)
        print("Created center_frame")

        self.right_frame = tk.Frame(self.right_canvas, width=390, height=400)
        self.right_frame.place(x=1, y=1)
        print("Created right_frame")

        # Создаем текстовое поле
        self.text_box = tk.Text(self.right_frame)
        self.text_box.pack()

        # Кнопка для загрузки данных из Excel
        self.load_button = tk.Button(self.right_frame, text="Добавить базу данных", command=self.load_excel_data)
        self.load_button.pack()

        # Метки для отображения видеопотока и изображений
        self.video_label = tk.Label(self.left_frame)
        self.video_label.pack(expand=True, fill=tk.BOTH)
        self.capture_label = tk.Label(self.center_frame)
        self.capture_label.pack(expand=True, fill=tk.BOTH)
        self.capture_label_bw_threshold = tk.Label(self.center_frame)
        self.capture_label_bw_threshold.pack(expand=True, fill=tk.BOTH)

        # Кнопка для захвата изображения
        self.capture_button = tk.Button(self.right_frame, text="Захватить изображение", command=self.capture_image)
        self.capture_button.pack()

        # Ползунок для настройки порога
        self.threshold_scale = tk.Scale(self.right_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold", command=self.update_threshold)
        self.threshold_scale.set(self.threshold_value)
        self.threshold_scale.pack()

        # Метка для отображения результатов OCR
        self.result_label = tk.Label(self.right_frame, text="", wraplength=400)
        self.result_label.pack()

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_image)
            img = img.resize((390, int(390 * frame.shape[0] / frame.shape[1])), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.video_label.after(10, self.update_image)

    def capture_image(self):
        print("Захват изображения...")
        ret, frame = self.cap.read()
        if ret:
            print("Изображение захвачено, обработка...")
            # Обработка изображения и выполнение OCR
            processed_image = process_image(frame)
            ocr_result = perform_ocr(processed_image)

            # Отображение результатов OCR в текстовом поле
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, ocr_result)

            # Отображение обработанного изображения
            processed_image = Image.fromarray(processed_image)
            imgtk = ImageTk.PhotoImage(image=processed_image)
            self.capture_label.imgtk = imgtk
            self.capture_label.configure(image=imgtk)
            print("Изображение обработано и отображено.")

    def load_excel_data(self):
        print("Загрузка данных из Excel...")
        # Загрузка данных из Excel файла
        data = load_excel_data()
        self.text_box.insert(tk.END, data)
        print("Данные загружены и отображены.")

    def update_threshold(self, value):
        self.threshold_value = int(value)
        print(f"Пороговое значение обновлено: {self.threshold_value}")

if __name__ == "__main__":
    import tkinter as tk
    import cv2

    def main():
        print("Инициализация видеопотока...")
        # Инициализация видеопотока с камеры
        cap = None
        for i in range(1, -1, -1):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Успешно подключились к камере {i}")
                break
            else:
                print(f"Не удалось подключиться к камере {i}")
                cap.release()
                cap = None

        if cap is None:
            print("Не удалось подключиться ни к одной камере")
            return

        print("Создание основного окна приложения...")
        # Создание основного окна приложения
        window = tk.Tk()
        window.title("OCR Application")
        window.geometry("1600x1200")  # Устанавливаем размеры основного окна

        # Создание экземпляра приложения OCRApp
        app = OCRApp(window, cap)

        print("Запуск основного цикла обработки событий...")
        # Запуск основного цикла обработки событий
        window.mainloop()

        # Освобождение ресурсов камеры при закрытии окна
        cap.release()
        cv2.destroyAllWindows()

    main()