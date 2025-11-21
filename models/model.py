# anything in this model will be displayed in the attribute frame

class State:
    def __init__(self):
        pass


class Card:
    def __init__(self, base_image_path=""):
        # self.type = None
        self.base = base_image_path
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


class Overlay:
    def __init__(self, img_path, x=0, y=0, scale=1.0):
        self.img_path = img_path
        self.x = x
        self.y = y
        self.scale = scale


class Eyes(Overlay):
    pass


class Nose(Overlay):
    pass


class Lips(Overlay):
    pass


class Accessory(Overlay):
    pass
