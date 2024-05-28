import cv2
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import numpy as np
import pytesseract
import tkinter.filedialog
import pandas as pd
import threading

# Глобальные переменные для координат прямоугольника и пути к файлу Excel
x1, y1, x2, y2 = 300, 300, 900, 500
threshold_value = 128
excel_file_path = None

def load_excel_data(file_path):
    try:
        data = pd.read_excel(file_path)
        messagebox.showinfo("Успех", "Файл Excel загружен успешно.")
        return data
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл Excel: {str(e)}")
        return None

def compare_with_excel_data(text, data):
    if data is None:
        messagebox.showwarning("Предупреждение", "Данные Excel не загружены.")
        return

    found_matches = []
    for index, row in data.iterrows():
        if text.strip() in row.to_string():
            found_matches.append(row)
    if found_matches:
        results_text.set(f"Найдено {len(found_matches)} совпадений:\n" + "\n".join([str(match) for match in found_matches]))
    else:
        results_text.set("Совпадений не найдено.")

def update_threshold(val):
    global threshold_value
    threshold_value = int(val)
    update_captured_image()

def update_image():
    ret, frame = cap.read()
    if ret:
        global x1, y1, x2, y2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        img = img.resize((600, int(600 * frame.shape[0] / frame.shape[1])), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.after(10, update_image)

def update_x1(val):
    global x1
    x1 = int(val)
    update_image()

def update_y1(val):
    global y1
    y1 = int(val)
    update_image()

def update_x2(val):
    global x2
    x2 = int(val)
    update_image()

def update_y2(val):
    global y2
    y2 = int(val)
    update_image()

def capture_image():
    ret, frame = cap.read()
    if ret:
        global x1, y1, x2, y2, capture_image_bw
        cropped_frame = frame[y1:y2, x1:x2]
        capture_image_bw = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)  # Сохраняем черно-белое изображение
        update_captured_image()  # вызов функции обновления изображения сразу после захвата кадра


def update_captured_image():
    def process_image():
        img_bw_cv = None
        if os.path.exists('captured_frame.jpg'):
            img = Image.open('captured_frame.jpg')
            imgtk = ImageTk.PhotoImage(image=img)
            capture_label.imgtk = imgtk
            capture_label.configure(image=imgtk)
            img_bw = img.convert('L')
            img_bw_cv = np.array(img_bw)
            img_bw_path = 'captured_frame_bw.jpg'
            img_bw.save(img_bw_path)
            _, img_bw_threshold = cv2.threshold(img_bw_cv, threshold_value, 255, cv2.THRESH_BINARY)
            img_bw_threshold = Image.fromarray(img_bw_threshold)
            imgtk_bw_threshold = ImageTk.PhotoImage(image=img_bw_threshold)
            capture_label_bw_threshold.imgtk = imgtk_bw_threshold
            capture_label_bw_threshold.configure(image=imgtk_bw_threshold)
            if os.path.exists(img_bw_path):
                img = cv2.imread(img_bw_path)
                text = pytesseract.image_to_string(img)
                results_text.set(f"Считанный текст:\n{text}")
                data = load_excel_data(excel_file_path)
                compare_with_excel_data(text, data)
            else:
                results_text.set("Файл изображения не найден.")
        else:
            results_text.set("Файл изображения не найден.")
    
    threading.Thread(target=process_image).start()

def select_excel_file():
    global excel_file_path
    excel_file_path = tk.filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if excel_file_path:
        print(f"Выбран файл: {excel_file_path}")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось подключиться к камере")
    exit()

root = tk.Tk()
root.title("Камера")

# Используем ttk для улучшенных виджетов
style = ttk.Style()
style.theme_use('clam')

# Создание рабочих областей
left_frame = ttk.Frame(root, width=800, height=600)
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
center_frame = ttk.Frame(root, width=800, height=600)
center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
right_frame = ttk.Frame(root, width=800, height=600)
right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Кнопка для загрузки файла Excel
load_button = ttk.Button(right_frame, text="Добавить базу данных", command=select_excel_file)
load_button.pack(pady=10)

# Виджеты для потокового видео и захваченного изображения
video_label = ttk.Label(left_frame)
video_label.pack(expand=True, padx=10, pady=10)
capture_label = ttk.Label(center_frame)
capture_label.pack(expand=True, padx=10, pady=10)

# Виджет для черно-белого изображения
capture_label_bw_threshold = ttk.Label(center_frame)
capture_label_bw_threshold.pack(expand=True, padx=10, pady=10)

# Кнопка для захвата изображения
capture_button = ttk.Button(right_frame, text="Захватить изображение", command=capture_image)
capture_button.pack(pady=10)

# Разделители и заголовки для интерфейса
ttk.Label(right_frame, text="Координаты прямоугольника:", font=('Helvetica', 12, 'bold')).pack(pady=5)
scale_x1 = ttk.Scale(right_frame, from_=0, to=1280, orient=tk.HORIZONTAL, command=update_x1)
ttk.Label(right_frame, text="X1").pack()
scale_x1.set(x1)
scale_x1.pack()

scale_y1 = ttk.Scale(right_frame, from_=0, to=720, orient=tk.HORIZONTAL, command=update_y1)
ttk.Label(right_frame, text="Y1").pack()
scale_y1.set(y1)
scale_y1.pack()

scale_x2 = ttk.Scale(right_frame, from_=0, to=1280, orient=tk.HORIZONTAL, command=update_x2)
ttk.Label(right_frame, text="X2").pack()
scale_x2.set(x2)
scale_x2.pack()

scale_y2 = ttk.Scale(right_frame, from_=0, to=720, orient=tk.HORIZONTAL, command=update_y2)
ttk.Label(right_frame, text="Y2").pack()
scale_y2.set(y2)
scale_y2.pack()

ttk.Label(right_frame, text="Пороговое значение:", font=('Helvetica', 12, 'bold')).pack(pady=5)
threshold_scale = ttk.Scale(right_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=update_threshold)
ttk.Label(right_frame, text="Threshold").pack()
threshold_scale.set(threshold_value)
threshold_scale.pack()

# Виджет для отображения результатов
ttk.Label(right_frame, text="Результаты:", font=('Helvetica', 12, 'bold')).pack(pady=5)
results_text = tk.StringVar()
results_label = ttk.Label(right_frame, textvariable=results_text, wraplength=400, justify=tk.LEFT)
results_label.pack(expand=True, padx=10, pady=10)

update_image()
root.mainloop()
cap.release()
