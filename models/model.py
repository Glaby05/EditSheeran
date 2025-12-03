import json
import os
import tkinter as tk
from tkinter import filedialog


class Card:
    def __init__(self, name="untitled ed", base="assets/blank_card.jpg"):
        self.name = name
        self.base = base
        self.overlays = []
        self.text = ""

    def set_base(self, new_path):
        self.base = new_path

    def set_text(self, text_str):
        """Save text as a string."""
        self.text = text_str

    def add_overlay(self, image_path, x=200, y=200):
        self.overlays.append({
            "image": image_path,
            "x": x,
            "y": y,
            "width": 100,
            "height": 100
        })

    def remove_overlay(self, i):
        if 0 <= i < len(self.overlays):
            self.overlays.pop(i)

    def update_overlay_size(self, index, size):
        if 0 <= index < len(self.overlays):
            self.overlays[index]["width"] = size
            self.overlays[index]["height"] = size

    def update_overlay_coor(self, index, x, y):
        if 0 <= index < len(self.overlays):
            self.overlays[index]["x"] = x
            self.overlays[index]["y"] = y

    def get_state(self):
        return {
            "base": self.base,
            "overlays": self.overlays,
            "text": self.text
        }

class Photobook:
    def __init__(self):
        self.saved_cards = []
        self.folder = "photobook"

    def add_card(self, card):
        self.saved_cards.append(card)

    def save_to_computer(self):
        os.makedirs(self.folder, exist_ok=True)

        if not self.saved_cards:
            print("No cards to save.")
            return

        card = self.saved_cards[-1]

        # last created card

        # Open a save dialog
        root = tk.Tk()
        root.withdraw()
        # Hide the small blank root window

        filepath = filedialog.asksaveasfilename(
            title="Save Your Ed Card",
            initialdir=self.folder,
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile=f"{card.name}.json"
        )

        root.destroy()

        new_name = os.path.splitext(os.path.basename(filepath))[0]
        card.name = new_name

        cleaned_overlays = []
        for ov in card.overlays:
            cleaned_overlays.append({
                "image": os.path.abspath(ov["image"]),
                "x": ov["x"],
                "y": ov["y"],
                "width": ov["width"],
                "height": ov["height"]
            })

        data_to_save = {
            "name": card.name,
            "base": os.path.abspath(card.base),
            "overlays": cleaned_overlays,
            "text": card.text
        }

        # Save JSON
        with open(filepath, "w") as f:
            json.dump(data_to_save, f, indent=4)

        print(f"Saved card to: {filepath}")
        displayed_name = card.name

        return filepath, displayed_name
