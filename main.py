import tkinter as tk
from gui.app_gui import MainApplication

def main():
    root = tk.Tk()
    root.title("Камера")
    app = MainApplication(root)
    app.run()

if __name__ == "__main__":
    main()