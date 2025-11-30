import os
from tkinter import PhotoImage

BASE_DIR = os.path.dirname(__file__)

cards = {
    "christmas card": os.path.join(BASE_DIR, "assets", "christmas card.jpg"),
    "base card": os.path.join(BASE_DIR, "assets", "base card.jpg"),
    "floral card": os.path.join(BASE_DIR, "assets", "floral_card.jpg"),
    "halloween card": os.path.join(BASE_DIR, "assets", "halloween card.jpg"),
    "st patties card": os.path.join(BASE_DIR, "assets", "st patties card.jpg")
}
eds = {
    "normal ed": os.path.join(BASE_DIR, "assets", "ed_normal.png"),
    "monkey ed": os.path.join(BASE_DIR, "assets", "ed_monkey.png"),
    "speaking ed": os.path.join(BASE_DIR, "assets", "ed_speaking.png")
}
eyes = {
    "heart eyes": os.path.join(BASE_DIR, "assets", "HEART_EYES.png"),
    "blue eyes": os.path.join(BASE_DIR, "assets", "BIG_BLUE_EYES.png"),
    "brown eyes": os.path.join(BASE_DIR, "assets", "BROWN_EYES.png")
}

mouths = {
    "open mouth": os.path.join(BASE_DIR, "assets", "open_mouth.png"),
    "smiling mouth": os.path.join(BASE_DIR, "assets", "smiling_mouth.png"),
    "tongue mouth": os.path.join(BASE_DIR, "assets", "tongue_mouth.png"),
}
accessories = {
    "cowboy hat": os.path.join(BASE_DIR, "assets", "cowboy_hat.png"),
    "witch hat": os.path.join(BASE_DIR, "assets", "witch_hat.png"),

    "leprechaun hat": os.path.join(BASE_DIR, "assets", "leprechaun_hat.png"),
}

eds = {
    "ed normal": os.path.join(BASE_DIR, "assets", "ed_normal.png"),
    "ed monkey": os.path.join(BASE_DIR, "assets", "ed_monkey.png"),
    "ed speaking": os.path.join(BASE_DIR, "assets", "ed_speaking.png")
}


def load_eyes():

    BASE_DIR = os.path.dirname(__file__)
    return {
        name: PhotoImage(file=os.path.join(BASE_DIR, path))
        for name, path in eyes.items()
    }


def load_mouths():

    BASE_DIR = os.path.dirname(__file__)
    return {
        name: PhotoImage(file=os.path.join(BASE_DIR, path))
        for name, path in mouths.items()
    }


def load_accessories():

    BASE_DIR = os.path.dirname(__file__)
    return {
        name: PhotoImage(file=os.path.join(BASE_DIR, path))
        for name, path in accessories.items()
    }

