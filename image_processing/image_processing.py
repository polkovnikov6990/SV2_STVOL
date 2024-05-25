# image_processing/image_processing.py
import cv2
from PIL import Image
import numpy as np
import pytesseract
from tkinter import messagebox

class ImageProcessor:
    def __init__(self):
        # Установка пути к Tesseract, если он не в PATH
        # pytesseract.pytesseract.tesseract_cmd = r'<полный_путь_к_установленному_tesseract>'
        pass
    
    def process_image_for_ocr(self, image_path, threshold_value=128):
        '''Подготавливает изображение для распознавания текста и запускает OCR.'''
        # Загружаем изображение и конвертируем его в черно-белое с пороговым фильтром
        try:
            img_bw = Image.open(image_path).convert('L')
            _, img_bw_threshold = cv2.threshold(np.array(img_bw), threshold_value, 255, cv2.THRESH_BINARY)
            return img_bw_threshold
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обработке изображения: {str(e)}")
            return None

    def recognize_text_from_image(self, image):
        '''Использует OCR для распознавания текста на подготовленном изображении.'''
        try:
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при распознавании текста: {str(e)}")
            return None

    def save_processed_image(self, image, output_path):
        '''Сохраняет обработанное изображение в файл.'''
        try:
            image_to_save = Image.fromarray(image)
            image_to_save.save(output_path)
            messagebox.showinfo("Информация", "Обработанное изображение сохранено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить обработанное изображение: {str(e)}")