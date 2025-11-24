import tkinter as tk
from PIL import Image, ImageTk

from models.model import Card
from controllers.controller import Controller


# note:
# - Frame -> the container (like layout management),
# - Canvas -> to draw shapes & images
class PreviewFrame(tk.Frame):
    # The center screen of the application
    def __init__(self, parent, controller: Controller):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="lightgray")
        self.canvas.pack(fill="both", expand=True)

        self._image_cache = []

    def preview_card(self, card: Card):
        # clear canvas
        self.canvas.delete("all")
        self._image_cache = []

        # render the base image and overlay(s)
        base = Image.open(card.base)
        tk_base = ImageTk.PhotoImage(base)
        self.canvas.create_image(0, 0, anchor="nw", image=tk_base)
        self._image_cache.append(tk_base)

        for ov in card.overlays:
            try:
                img = Image.open(ov.img_path)
                w, h = img.size
                img = img.resize((int(w * ov.scale), int(h * ov.scale)))

                tk_img = ImageTk.PhotoImage(img)
                self.canvas.create_image(ov.x, ov.y, anchor="nw", image=tk_img)
                self._image_cache.append(tk_img)
            except:
                pass
