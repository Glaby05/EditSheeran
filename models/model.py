# anything in this model will be displayed in the attribute frame
import tkinter as tk
from overlay_images import *
from PIL import Image, ImageTk

class State:
    def __init__(self):
        pass



class Card:
    def __init__(self, base_image_path= "assets/blank card.jpg", scale=1.0):
        # self.type = None
        self.base = base_image_path
        self.cardtemplate = CardTemplate
        self.ed = EdSheeran("ed_normal.png")
        self.overlays = []  # list of Overlay objects, can class State object
        self.name = "Untitled Ed"
        self.facts = ""
        self.scale = scale

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
    def __init__(self, img="ed.ico", x=50, y=90, scale=0.75):
        self.image = os.path.join(BASE_DIR, "assets", img)
        self.x = x
        self.y = y
        self.scale = scale

class CardTemplate:
    def __init__(self, img_path):
        self.library = cards
        pil_img = Image.open(img_path).resize((300, 300))
        self.tk_image = ImageTk.PhotoImage(pil_img)


class Overlay:
    def __init__(self, img_path, x=0, y=0, scale=2.0):
        self.img_path = os.path.join(BASE_DIR, "assets", img_path)
        self.x = x
        self.y = y
        self.scale = scale



class Eyes(Overlay):
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        super().__init__(img_path, x, y, scale)
        self.library = eyes
        # self.keys = list(library.keys())
        # self.index = 0
        # self.label = tk.Label(parent)
        # self.label.pack()


class Lips(Overlay):
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        super().__init__(img_path, x, y, scale)
        self.library = mouths
        # self.keys = list(self.library.keys())
        # self.index = 0
        # self.label = tk.Label(parent)
        # self.label.pack()


class Accessory(Overlay):
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        super().__init__(img_path, x, y, scale)
        self.library = accessories
        # self.keys = list(self.library.keys())
        # self.index = 0
        # self.label = tk.Label(parent)
        # self.label.pack()
