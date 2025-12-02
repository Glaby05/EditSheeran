from views.view import View, PHOTBOOK_DIR
from models.model import Card, Photobook
import tkinter as tk
from tkinter import messagebox
import os
import json

class EditSheeranController:
    def __init__(self):
        self.photobook = Photobook()

        self.current_card = Card()

        self.view = View(self)

        self.refresh_preview()

    def new_card(self):
        self.current_card = Card()  # ← reset model too
        self.refresh_preview()

    def refresh_preview(self):
        data = self.current_card.get_state()
        self.view.update_canvas(data)

    def change_template(self, path):
        self.current_card.set_base(path)
        self.refresh_preview()

    def add_accessory(self, path, x=None, y=None):
        if x is None:
            x = 200
        if y is None:
            y=250
        self.current_card.add_overlay(path, x, y)
        self.refresh_preview()

    def run(self):
        self.view.mainloop()

    def save_card(self):
        self.photobook.add_card(self.current_card)

        filepath, displayed_name = self.photobook.save_to_computer()

        if filepath is None:
            return  # user cancelled

        # Update the card's name in the controller
        self.current_card.name = displayed_name

        self.view.load_photobook()


    def load_card(self, filename):
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno("Confirmaiton", "Do you want to Edit this Card?")
        if response:
            json_path = os.path.join(PHOTBOOK_DIR, filename)

            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                    self.view.update_canvas(data)
            except:
                pass

        else:
            root.destroy()
        root.destroy()


