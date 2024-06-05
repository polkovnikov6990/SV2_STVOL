import tkinter.filedialog
import pandas as pd
from config import excel_data, excel_path
import tkinter as tk


def load_excel_data(text_box):
    global excel_data, excel_path
    # Открываем диалоговое окно для выбора файла Excel
    excel_path = tkinter.filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if excel_path:
        # Загружаем данные из выбранного файла Excel в DataFrame
        excel_data = pd.read_excel(excel_path, engine='openpyxl')
        print("Данные из Excel загружены")
        # Отображаем загруженные данные в интерфейсе
        show_excel_data(text_box)

def show_excel_data(text_box):
    if excel_data is not None:
        # Преобразуем данные DataFrame в строку и отображаем их в текстовом поле
        data_str = excel_data.to_string(index=False)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, data_str)