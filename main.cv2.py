import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import pytesseract

# Глобальные переменные для координат прямоугольника
x1, y1, x2, y2 = 300, 300, 900, 500
# Глобальная переменная для порогового значения
threshold_value = 128

def update_threshold(val):
    global threshold_value
    threshold_value = int(val)
    update_captured_image()  # Обновляем изображение с новым порогом


def update_image():
    ret, frame = cap.read()
    if ret:
# Используем глобальные переменные для координат
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

def update_y1(val):
    global y1
    y1 = int(val)

def update_x2(val):
    global x2
    x2 = int(val)

def update_y2(val):
    global y2
    y2 = int(val)



def capture_image():
    ret, frame = cap.read()
    if ret:
        global x1, y1, x2, y2
        # Обрезаем изображение до размеров зеленого прямоугольника
        cropped_frame = frame[y1:y2, x1:x2]
        cv2.imwrite('captured_frame.jpg', cropped_frame)
        update_captured_image()

def update_captured_image():
    img_bw_cv = None  # Инициализация переменной

    if os.path.exists('captured_frame.jpg'):
        img = Image.open('captured_frame.jpg')
        imgtk = ImageTk.PhotoImage(image=img)
        capture_label.imgtk = imgtk
        capture_label.configure(image=imgtk)
        # Преобразование в черно-белое
        img_bw = img.convert('L')
        img_bw_cv = np.array(img_bw)  # Преобразование из PIL Image в NumPy массив для OpenCV

        # Применение пороговой обработки
        _, img_bw_threshold = cv2.threshold(img_bw_cv, threshold_value, 255, cv2.THRESH_BINARY)


# # Теперь обрабатываем сохраненный скриншот
# if os.path.exists(img_bw):
#     img = cv2.imread(img_bw)
#     text = pytesseract.image_to_string(img)
#     print("Считанный текст с изображения:")
#     print(text)
# else:
#     print("Файл изображения не найден.")




        # Преобразование обратно в PIL Image и отображение
        img_bw_threshold = Image.fromarray(img_bw_threshold)
        imgtk_bw_threshold = ImageTk.PhotoImage(image=img_bw_threshold)
        capture_label_bw_threshold.imgtk = imgtk_bw_threshold
        capture_label_bw_threshold.configure(image=imgtk_bw_threshold)


#def update_captured_image():
#    if os.path.exists('captured_frame.jpg'):
#        img = Image.open('captured_frame.jpg')
#        # Убираем изменение размера, чтобы отображать изображение в оригинальном размере
#        imgtk = ImageTk.PhotoImage(image=img)
#        capture_label.imgtk = imgtk
#        capture_label.configure(image=imgtk)
#        # Преобразование в черно-белое и отображение
#        img_bw = img.convert('L')  # Преобразование в черно-белое
#        imgtk_bw = ImageTk.PhotoImage(image=img_bw)
#        capture_label_bw.imgtk = imgtk_bw
#        capture_label_bw.configure(image=imgtk_bw)


cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Не удалось подключиться к камере")
    exit()

root = tk.Tk()
root.title("Камера")

# Создание рабочих областей
left_frame = tk.Frame(root, width=800, height=600)
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
center_frame = tk.Frame(root, width=800, height=600)
center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
right_frame = tk.Frame(root, width=800, height=600)
right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Виджеты для потокового видео и захваченного изображения
video_label = tk.Label(left_frame)
video_label.pack(expand=True)
capture_label = tk.Label(center_frame)
capture_label.pack(expand=True)
# Добавление виджета Label для черно-белого изображения
capture_label_bw_threshold = tk.Label(center_frame)
capture_label_bw_threshold.pack(expand=True)

# Кнопка для захвата изображения
capture_button = tk.Button(right_frame, text="Захватить изображение", command=capture_image)
capture_button.pack()

# Бегунки для изменения координат прямоугольника
scale_x1 = tk.Scale(right_frame, from_=0, to=1280, orient=tk.HORIZONTAL, label="X1", command=update_x1)
scale_x1.set(x1)
scale_x1.pack()
scale_y1 = tk.Scale(right_frame, from_=0, to=720, orient=tk.HORIZONTAL, label="Y1", command=update_y1)
scale_y1.set(y1)
scale_y1.pack()
scale_x2 = tk.Scale(right_frame, from_=0, to=1280, orient=tk.HORIZONTAL, label="X2", command=update_x2)
scale_x2.set(x2)
scale_x2.pack()
scale_y2 = tk.Scale(right_frame, from_=0, to=720, orient=tk.HORIZONTAL, label="Y2", command=update_y2)
scale_y2.set(y2)
scale_y2.pack()
# создаем бегунок для изменения значения преобразования в ЧБ
threshold_scale = tk.Scale(right_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold", command=update_threshold)
threshold_scale.set(threshold_value)  # Устанавливаем начальное значение
threshold_scale.pack()



update_image()
update_captured_image()

root.mainloop()
cap.release()
