import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from models.model import Card
from views.attribute_frame import AttributesFrame
from views.photobook_frame import PhotobookFrame
from views.preview_frame import PreviewFrame
from views.welcome_frame import choose_image
from controllers.controller import Controller


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x600")
        self.title("EditSheeran")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'assets', 'ed.ico')
        self.iconbitmap(icon_path)

        self.controller = Controller(self)


        self.preview = PreviewFrame(self, self.controller, self.controller.card)

        self.photobook = PhotobookFrame(self, self.controller, self.controller.card)

        self.attributes = AttributesFrame(self, self.controller,self.controller.card)
        self.attributes.pack(side="left",fill="y")
        self.preview.pack(side="left", fill="both", expand=True)
        self.photobook.pack(side="right", fill="y")

        self.create_menu()




    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Card", command=self.controller.new_card)
        # file_menu.add_command(label="Open Base Image", command=self.controller.load_base)
        file_menu.add_command(label="Save to Photobook", command=self.controller.save_card)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
