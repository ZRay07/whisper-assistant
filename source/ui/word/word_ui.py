from source.core.model_interface import *

import tkinter as tk
from tkinter import ttk

import pyautogui

class WordWindow(tk.Tk):
    def __init__(self, title, size, start_position):
        super().__init__()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}+{start_position[0]}+{start_position[1]}")
        self.minsize(size[0], size[1])

        self.menu = Menu(self)

        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def create_menu(self):
        ttk.Label(self, bg = "slate", text = "Word Menu", font = ("Franklin Gothic Medium", 12)).grid(row = 0, column = 0)




WordWindow = WordWindow("Microsoft Word Menu", (600 , 600), (300 , 300))
