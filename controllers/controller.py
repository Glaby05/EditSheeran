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
        self.selected_index = -1

        self.card_state = {"text": None}
        self.view = View(self)
        self.refresh_preview()

    def new_card(self):
        self.current_card = Card()
        self.selected_index = -1
        self.card_state["text"] = None
        if getattr(self.view, "text_item_id", None):
            self.view.canvas.delete(self.view.text_item_id)
        self.view.text_item_id = None
        self.view.text_entry.delete(0, tk.END)
        self.view.text_entry.insert(0, "Set Custom Greeting")
        self.refresh_preview()

    def select_item(self, index):
        self.selected_index = index
        self.refresh_preview()

    def refresh_preview(self):
        data = self.current_card.get_state()
        self.view.update_canvas(data, self.selected_index)


    def change_template(self, path):
        self.current_card.set_base(path)
        self.refresh_preview()

    def add_accessory(self, path, x=None, y=None):
        if x is None:
            x = 300
        if y is None:
            y=350
        self.current_card.add_overlay(path, x, y)
        self.refresh_preview()

    def get_selected_overlay(self):
        if self.selected_index != -1:
            return self.current_card.overlays[self.selected_index]
        return None

    def resize_current_item(self, new_size):
        if self.selected_index != -1:
            self.current_card.update_overlay_size(self.selected_index, int(new_size))

            self.refresh_preview()

    def move_current_item(self, new_x, new_y):
        if self.selected_index != -1:
            self.current_card.update_overlay_coor(self.selected_index, int(new_x), int(new_y))
            self.refresh_preview()

    def del_current_item(self, i):
        if self.selected_index != -1:
            self.current_card.remove_overlay(i)
            self.refresh_preview()

    def run(self):
        self.view.mainloop()

    def save_card(self):
        text_content = self.view.text_entry.get().strip()
        self.current_card.set_text(text_content if len(text_content) > 0 else "")
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

                    self.view.text_item_id = None
                    self.view.text_entry.delete(0, tk.END)
                    self.view.text_entry.insert(0, "Set Custom Greeting")

                    loaded = Card()
                    loaded.name = data.get("name", "untitled ed")
                    loaded.base = data["base"]
                    loaded.overlays = data.get("overlays", [])
                    loaded.text = data.get("text")

                    self.current_card = loaded
                    self.selected_index = -1  # reset selection

                    # now redraw using controller
                    self.refresh_preview()


            except:
                pass

        else:
            root.destroy()
        root.destroy()


