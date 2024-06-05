import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import image_processing
import ocr_processing
import excel_utils
from config import x1, y1, x2, y2

class OCRApp:
    def __init__(self, window, cap):
        self.cap = cap
        self.threshold_value = 128

        self.create_gui(window)
        self.update_image()

    def create_gui(self, window):
        self.left_frame = tk.Frame(window, width=800, height=600)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.center_frame = tk.Frame(window, width=800, height=600)
        self.center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.right_frame = tk.Frame(window, width=800, height=600)
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.text_box = tk.Text(self.right_frame)
        self.text_box.pack()

        self.load_button = tk.Button(self.right_frame, text="Добавить базу данных", command=self.load_excel_data)
        self.load_button.pack()

        self.video_label = tk.Label(self.left_frame)
        self.video_label.pack(expand=True, fill=tk.BOTH)
        self.capture_label = tk.Label(self.center_frame)
        self.capture_label.pack(expand=True, fill=tk.BOTH)
        self.capture_label_bw_threshold = tk.Label(self.center_frame)
        self.capture_label_bw_threshold.pack(expand=True, fill=tk.BOTH)

        self.capture_button = tk.Button(self.right_frame, text="Захватить изображение", command=self.capture_image)
        self.capture_button.pack()

        self.threshold_scale = tk.Scale(self.right_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold", command=self.update_threshold)
        self.threshold_scale.set(self.threshold_value)
        self.threshold_scale.pack()

        self.result_label = tk.Label(self.right_frame, text="", wraplength=400)
        self.result_label.pack()

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_image)
            img = img.resize((600, int(600 * frame.shape[0] / frame.shape[1])), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.video_label.after(10, self.update_image)
        else:
            print("Ошибка: не удалось получить кадр с камеры")

    def update_threshold(self, val):
        self.threshold_value = int(val)
        self.update_captured_image()

    def load_excel_data(self):
        excel_utils.load_excel_data(self.text_box)

    def capture_image(self):
        image_processing.capture_image(self.cap, x1, y1, x2, y2)
        self.update_captured_image()

    def update_captured_image(self):
        if os.path.exists('captured_frame.jpg'):
            img = Image.open('captured_frame.jpg')
            imgtk = ImageTk.PhotoImage(image=img)
            self.capture_label.imgtk = imgtk
            self.capture_label.configure(image=imgtk)

            img_bw_cv = image_processing.convert_to_bw('captured_frame.jpg')
            img_bw_threshold = image_processing.apply_threshold(img_bw_cv, self.threshold_value)
            img_bw_threshold_pil = Image.fromarray(img_bw_threshold)
            imgtk_bw_threshold = ImageTk.PhotoImage(image=img_bw_threshold_pil)
            self.capture_label_bw_threshold.imgtk = imgtk_bw_threshold
            self.capture_label_bw_threshold.configure(image=imgtk_bw_threshold)

            text = ocr_processing.apply_ocr(img_bw_threshold)
            print("Считанный текст с изображения:")
            print(text)

            results = ocr_processing.compare_with_excel_data(text)
            if results and results[0][0] == "Ошибка":
                self.result_label.config(text=results[0][1], fg="red")
            else:
                results_text = "\n".join([f"Row {row}: {cell} ({match_type})" for row, cell, match_type in results])
                self.result_label.config(text=results_text, fg="black")