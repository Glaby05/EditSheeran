import json
import os
from tkinter import filedialog, messagebox
from models.model import Card

class Controller:
    # handles updates & interactions between components
    def __init__(self, app):
        self.app = app
        self.card = None

    def update_preview(self):
        self.app.preview.preview_card(self.card)

    def new_card(self):
        self.card = Card()
        self.update_preview()

    def load_base(self):
        path = filedialog.askopenfilename(title="Choose a picture of Ed")
        if not path:
            return
        self.card.base = path
        self.update_preview()

    def save_card(self):
        directory = "photobook"
        if not os.path.exists(directory):
            os.makedirs(directory)

        name = self.card.name.replace(" ", "_") or "Untitled_Ed"
        filename = f"{directory}/{name}.json"

        try:
            with open(filename, "w") as f:
                json.dump(self.card.to_dict(), f, indent=4)
            messagebox.showinfo("Saved", "Card saved to photobook!")
            self.app.photobook_frame.update_list()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save card: {e}")
