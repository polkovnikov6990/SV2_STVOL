# data/excel_utils.py
import pandas as pd
from tkinter import messagebox

class ExcelUtils:
    def __init__(self):
        # Инициализация, если требуется
        pass
    
    def load_excel_data(self, file_path):
        '''Загружает данные из Excel файла.'''
        try:
            self.dataframe = pd.read_excel(file_path)
            print("Данные успешно загружены из файла", file_path)
            return self.dataframe
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Произошла ошибка при загрузке Excel файла: {str(e)}")
            return None
    
    def save_data_to_excel(self, dataframe, output_path):
        '''Сохраняет pandas DataFrame в Excel файл.'''
        try:
            dataframe.to_excel(output_path, index=False)
            messagebox.showinfo("Успех", f"Данные успешно сохранены в {output_path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные в Excel файл: {str(e)}")

    def get_column_data(self, column_name):
        '''Извлекает данные из определенной колонки DataFrame.'''
        try:
            if column_name in self.dataframe.columns:
                return self.dataframe[column_name]
            else:
                messagebox.showerror("Ошибка", f"Колонка '{column_name}' не найдена.")
                return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при извлечении данных из колонки '{column_name}': {str(e)}")
            return None

    def add_row(self, row_data):
        '''Добавляет строку данных в DataFrame.'''
        try:
            self.dataframe = self.dataframe.append(row_data, ignore_index=True)
            messagebox.showinfo("Успех", "Данные успешно добавлены.")
        except Exception as e:
            messagebox.showerror("Ошибка добавления", f"Не удалось добавить данные: {str(e)}")