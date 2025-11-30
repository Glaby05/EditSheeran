import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

class CardTemplatePicker:
    def __init__(self, parent, image_paths):
        self.top = Toplevel()
        self.top.title("Select a template")
        self.selected_path = None
        self.selected_image = None
        self.tk_images = []

        row = 0
        col = 0
        max_cols = 3

        for path in image_paths:
            try:
                image = Image.open(image_paths[path])
                resized_image = image.resize((450, 350))
                img = ImageTk.PhotoImage(resized_image)
                self.tk_images.append(img)

                btn = tk.Button(self.top, image=img,
                                command=lambda p=path: self.on_select(p, image_paths[p]))
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            except Exception as e:
                print(f"Error loading {path}: {e}")

        self.top.grab_set()
        self.top.wait_window()

    def on_select(self, name, path):
        self.selected_image = name
        self.selected_path = path
        self.top.destroy()
