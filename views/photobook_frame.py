import json
import os
import tkinter as tk
from tkinter import messagebox

from models.model import Card
from views.preview_frame import PreviewFrame
from controllers.controller import Controller


class PhotobookFrame(tk.Frame):
    # right screen of the app
    # /photobook is a directory that stores all created cards

    def __init__(self, parent, controller: Controller):
        super().__init__(parent, width=250)
        self.parent = parent
        self.controller = controller

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # add some command buttons
        tk.Button(self, text="Load", command=self.load_card).pack(pady=5)
        tk.Button(self, text="Delete", command=self.delete_card).pack(pady=5)

        self.update_list()

    def photobook_dir(self):
        path = "photobook"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def load_card(self, preview_frame: PreviewFrame):
        # load .json file to get the model, redraw model to preview latest version
        # card = read_card_json(filename)
        # parent.card = card
        # parent.preview_frame.preview_card(card)

        selection = self.listbox.curselection()
        if not selection:
            return

        filename = self.listbox.get(selection[0])
        full = os.path.join(self.photobook_dir(), filename)
        with open(full, "r") as f:
            data = json.load(f)

        card = Card.from_dict(data)
        self.controller.card = card
        self.controller.update_preview()

    def delete_card(self, preview_frame: PreviewFrame):
        selection = self.listbox.curselection()
        if not selection:
            return

        filename = self.listbox.get(selection[0])
        full = os.path.join(self.photobook_dir(), filename)
        if messagebox.askyesno("Confirm", f"Delete {filename}?"):
            try:
                os.remove(full)
                self.update_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")

    def update_list(self):
        directory = self.photobook_dir()
        self.listbox.delete(0, tk.END)
        for f in os.listdir(directory):
            if f.endswith(".json"):
                self.listbox.insert(tk.END, f)
