import json
import os


class Card:
    def __init__(self, name="Untitled Ed", base="assets/blank_card.jpg"):
        self.name = name
        self.base = base
        self.overlays = []

    def set_base(self, new_path):
        self.base = new_path

    def add_overlay(self, image_path, x=200, y=200):
        self.overlays.append({
            "image": image_path,
            "x": x,
            "y": y,
            "width": 100,
            "height": 100
        })

    def remove_overlay(self, path, x, y, w, h):
        for overlay in self.overlays:
            if overlay["image"] == path and overlay["x"] == x and \
                    overlay["y"] == y and overlay["w"] == w and overlay["h"] == h:
                self.overlays.pop(overlay)

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
            "overlays": self.overlays
        }


class Photobook:
    def __init__(self):
        self.saved_cards = []
        self.filename = "photobook.json"

    def add_card(self, card):
        self.saved_cards.append(card)

    def save_to_computer(self):
        data = []
        for card in self.saved_cards:
            data.append({
                "name": card.name,
                "base": card.base,
                "overlays": card.overlays
            })

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
