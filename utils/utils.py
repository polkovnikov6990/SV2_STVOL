# utils/utils.py
import os
import json
from datetime import datetime

def read_json(file_path):
    '''Читает JSON файл и возвращает данные.'''
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка при чтении JSON из файла {file_path}.")
        return None

def write_json(data, file_path):
    '''Записывает данные в JSON файл.'''
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def convert_size(size_bytes):
    '''Конвертирует размер в байтах в читаемый формат.'''
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_current_time(format='%Y-%m-%d %H:%M:%S'):
    '''Возвращает текущее время в заданном формате.'''
    return datetime.now().strftime(format)

def create_directory_if_not_exists(directory_path):
    '''Создает директорию, если она не существует.'''
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Директория {directory_path} создана.")
    else:
        print(f"Директория {directory_path} уже существует.")