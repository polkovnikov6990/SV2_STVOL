import cv2
import pytesseract
import pandas as pd

def process_image(image):
    """
    Обрабатывает изображение, конвертируя его в оттенки серого и выполняя бинаризацию.
    
    :param image: Входное изображение в формате BGR.
    :return: Обработанное бинарное изображение.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return thresh

def perform_ocr(image):
    """
    Выполняет OCR (распознавание текста) на входном изображении.
    
    :param image: Входное бинарное изображение.
    :return: Распознанный текст.
    """
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def load_excel_data(filepath='data.xlsx'):
    """
    Загружает данные из Excel файла.
    
    :param filepath: Путь к Excel файлу.
    :return: Строковое представление данных из Excel.
    """
    df = pd.read_excel(filepath)
    return df.to_string()