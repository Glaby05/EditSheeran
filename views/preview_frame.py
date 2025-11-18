import tkinter as tk
from PIL import Image, ImageTk

from models.model import Card


# note:
# - Frame -> the container (like layout management),
# - Canvas -> to draw shapes & images
class PreviewFrame(tk.Frame):
    # The center screen of the application
    def __init__(self, parent):
        super().__init__(parent, bg="#eeeeee")
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

    def preview_card(self, card: Card):
        # render the base image and overlay(s)
        base = Image.open(card.base)
        tk_base = ImageTk.PhotoImage(base)

        pass
