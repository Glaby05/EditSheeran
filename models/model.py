# anything in this model will be displayed in the attribute frame
import tkinter as tk
from overlay_images import *


class State:
    def __init__(self):
        pass


class Card:
    def __init__(self, base_image_path="blank_card.jpg"):
        # self.type = None
        self.base = os.path.join(BASE_DIR, "assets", base_image_path)
        self.ed = EdSheeran("ed_normal.png", x=50, y=50, scale=1.0)
        self.overlays = []  # list of Overlay objects, can class State object
        self.name = "Untitled Ed"
        self.facts = ""

    def to_dict(self):
        return {
            "base": self.base,
            "name": self.name,
            "facts": self.facts,
            "overlays": [
                {
                    "img_path": ov.img_path,
                    "x": ov.x,
                    "y": ov.y,
                    "scale": ov.scale,
                }
                for ov in self.overlays
            ],
        }

    @staticmethod
    def from_dict(data):
        c = Card(data.get("base", ""))
        c.name = data.get("name", "Untitled Ed")
        c.facts = data.get("facts", "")
        for ov in data.get("overlays", []):
            c.overlays.append(
                Overlay(ov["img_path"], ov["x"], ov["y"], ov["scale"])
            )
        return c


class EdSheeran:
    def __init__(self, img="assets/ed.ico", x=0, y=0, scale=5.0):
        self.image = img
        self.x = x
        self.y = y
        self.scale = scale


class Overlay:
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        self.img_path = img_path
        self.x = x
        self.y = y
        self.scale = scale


class Eyes(Overlay):
    def __init__(self, library, parent, img_path):
        super().__init__(img_path)
        self.library = eyes
        self.keys = list(library.keys())
        self.index = 0
        self.label = tk.Label(parent)
        self.label.pack()


class Lips(Overlay):
    def __init__(self, library, parent, img_path):
        super().__init__(img_path)
        self.library = mouths
        self.keys = list(library.keys())
        self.index = 0
        self.label = tk.Label(parent)
        self.label.pack()


class Accessory(Overlay):
    def __init__(self, library, parent, img_path):
        super().__init__(img_path)
        self.library = accessories
        self.keys = list(library.keys())
        self.index = 0
        self.label = tk.Label(parent)
        self.label.pack()
