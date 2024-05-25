import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import numpy as np
import pandas as pd
import threading

# Глобальные переменные для пути к файлу Excel и данных
excel_file_path = None
excel_data = None

# Загрузка предварительно обученной модели EAST
east_model_path = 'frozen_east_text_detection.pb'

# Пороговые значения для фильтрации слабых предсказаний
confThreshold = 0.5
nmsThreshold = 0.4

# Функция для загрузки файла Excel
def load_excel_data(file_path):
    try:
        data = pd.read_excel(file_path)
        messagebox.showinfo("Успех", "Файл Excel загружен успешно.")
        return data
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл Excel: {str(e)}")
        return None

# Функция для сравнения распознанного текста с данными из Excel
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

# Функция для захвата изображения и распознавания текста
def capture_image():
    ret, frame = cap.read()
    if ret:
        results_text.set("Обрабатываю изображение...")
        threading.Thread(target=process_frame, args=(frame,)).start()

def process_frame(frame):
    (H, W) = frame.shape[:2]
    newW, newH = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    frame_resized = cv2.resize(frame, (newW, newH))
    blob = cv2.dnn.blobFromImage(frame_resized, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)

    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    rects = []
    confidences = []
    for i in range(0, scores.shape[2]):
        for j in range(0, scores.shape[3]):
            if scores[0, 0, i, j] >= confThreshold:
                (offsetX, offsetY) = (j * 4.0, i * 4.0)
                angle = geometry[0, 4, i, j]
                cos = np.cos(angle)
                sin = np.sin(angle)
                h = geometry[0, 0, i, j]
                w = geometry[0, 1, i, j]
                endX = int(offsetX + (cos * w) + (sin * h))
                endY = int(offsetY - (sin * w) + (cos * h))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scores[0, 0, i, j])

    boxes = non_max_suppression(np.array(rects), probs=confidences)

    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        roi = frame[startY:endY, startX:endX]
        text = pytesseract.image_to_string(roi)
        if text.strip():
            results_text.set(f"Найден текст: {text}")
            compare_with_excel_data(text, excel_data)

    cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv_image)
    imgtk = ImageTk.PhotoImage(image=img)
    capture_label.imgtk = imgtk
    capture_label.configure(image=imgtk)

def select_excel_file():
    global excel_file_path, excel_data
    excel_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if excel_file_path:
        excel_data = load_excel_data(excel_file_path)

def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = y2 if probs is None else probs

    idxs = np.argsort(idxs)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось подключиться к камере")
    exit()

root = tk.Tk()
root.title("Камера и Распознавание Текста")

# Используем ttk для улучшенных виджетов
style = ttk.Style()
style.theme_use('clam')

# Создание рабочих областей
left_frame = ttk.Frame(root, width=800, height=600)
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
right_frame = ttk.Frame(root, width=800, height=600)
right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Кнопка для загрузки файла Excel
load_button = ttk.Button(right_frame, text="Добавить базу данных", command=select_excel_file)
load_button.pack(pady=10)

# Виджеты для потокового видео и захваченного изображения
video_label = ttk.Label(left_frame)
video_label.pack(expand=True, padx=10, pady=10)
capture_label = ttk.Label(right_frame)
capture_label.pack(expand=True, padx=10, pady=10)

# Кнопка для захвата изображения
capture_button = ttk.Button(right_frame, text="Захватить изображение", command=capture_image)
capture_button.pack(pady=10)

# Виджет для отображения результатов
ttk.Label(right_frame, text="Результаты:", font=('Helvetica', 12, 'bold')).pack(pady=5)
results_text = tk.StringVar()
results_label = ttk.Label(right_frame, textvariable=results_text, wraplength=400, justify=tk.LEFT)
results_label.pack(expand=True, padx=10, pady=10)

# Загрузка модели EAST
print("Загрузка модели EAST...")
net = cv2.dnn.readNet(east_model_path)
layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

def update_image():
    ret, frame = cap.read()
    if ret:
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        img = img.resize((600, int(600 * frame.shape[0] / frame.shape[1])), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.after(10, update_image)

update_image()
root.mainloop()
cap.release()
