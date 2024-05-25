# gui/app_gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from camera.camera import Camera
from image_processing.image_processing import ImageProcessor
from data.excel_utils import ExcelUtils

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.camera = Camera()  # Используемый ID камеры может быть указан здесь
        self.image_processor = ImageProcessor()
        self.excel_utils = ExcelUtils()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.geometry('1200x800')
        
        # Создание рабочих областей
        self.create_frames()
        
        # Создаем и регулируем элементы GUI
        self.setup_widgets()
    
    def create_frames(self):
        self.left_frame = ttk.Frame(self.root, width=800, height=600)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.center_frame = ttk.Frame(self.root, width=800, height=600)
        self.center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.right_frame = ttk.Frame(self.root, width=800, height=600)
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def setup_widgets(self):
        # Виджеты для потокового видео и захваченного изображения
        self.video_label = ttk.Label(self.left_frame)
        self.video_label.pack(expand=True, padx=10, pady=10)
        self.capture_label = ttk.Label(self.center_frame)
        self.capture_label.pack(expand=True, padx=10, pady=10)

        # Кнопка для загрузки файла Excel
        self.load_button = ttk.Button(self.right_frame, text="Добавить базу данных", command=self.select_excel_file)
        self.load_button.pack(pady=10)
        
        # Кнопка для захвата изображения
        self.capture_button = ttk.Button(self.right_frame, text="Захватить изображение", command=self.capture_image)
        self.capture_button.pack(pady=10)

        # Виджет для отображения результатов и настроек
        self.create_additional_widgets()

        # Запускаем обновление изображения
        self.update_image()

    def create_additional_widgets(self):
        # Здесь создаются слайдеры для настройки параметров, а также виджеты для вывода результатов
        pass

    def select_excel_file(self):
        # Используем filedialog для выбора файла Excel
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            print(f"Выбран файл: {file_path}")
            # Загрузка и обработка Excel файла
            self.excel_utils.load_excel_data(file_path)

    def capture_image(self):
        # Действие по кнопке для захвата изображения
        pass

    def update_image(self):
        # Обновление изображения с камеры в реальном времени
        pass

    def run(self):
        # Код, который должен выполняться в методе 'run'
        print("Запуск приложения...")