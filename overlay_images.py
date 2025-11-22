import os
from tkinter import PhotoImage

BASE_DIR = os.path.dirname(__file__)

eyes = {
"heart eyes": os.path.join(BASE_DIR, "assets", "HEART_EYES.png"),
    "blue eyes": os.path.join(BASE_DIR, "assets", "BIG_BLUE_EYES.png"),
    "brown eyes": os.path.join(BASE_DIR, "assets", "BROWN_EYES_.png")
}

def load_eyes():

    BASE_DIR = os.path.dirname(__file__)
    return {
        name: PhotoImage(file=os.path.join(BASE_DIR, path))
        for name, path in eyes.items()
    }
