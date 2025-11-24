import tkinter as tk
from tkinter import Tk, PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
from overlay_images import *
from views.preview_frame import PreviewFrame
from models.model import Overlay
from controllers.controller import Controller



class EyeSelector(tk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.keys = list(library.keys())
        self.index = 0
        for k, path in eyes.items():
            pil_img = Image.open(path).resize((100, 100))
            self.library[k] = ImageTk.PhotoImage(pil_img)

        self.btn_prev = tk.Button(self, text="◀", command=self.prev)
        self.btn_prev.grid(row=1, column=0, padx=5)

        self.label = tk.Label(self)
        self.label.grid(row=1, column=1, padx=5)
        self.label2 = tk.Label(self, text="Eyes")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(self, text="▶", command=self.next)
        self.btn_next.grid(row=1, column=2, padx=5)

        self.update_image()

    def update_image(self):
        key = self.keys[self.index]
        img = self.library[key]
        self.label.img = img  # keep reference
        self.label.config(image=img)

    def next(self):
        self.index = (self.index + 1) % len(self.keys)
        current_key = self.keys[self.index]
        self.label.config(image=self.library[current_key])

    def prev(self):
        self.index = (self.index - 1) % len(self.keys)
        current_key = self.keys[self.index]
        self.label.config(image=self.library[current_key])


class AttributesFrame(tk.Frame):
    # the left screen of the app
    def __init__(self, parent, controller: Controller):
        super().__init__(parent, width=120, height=700, bg="white")
        self.parent = parent
        self.controller = controller

        # frame = tk.Frame(self, width=1200, height=700)

        self.scale = tk.DoubleVar(value=1.0)

        tk.Scale(self, from_=0.2, to=3.0, orient="horizontal",
                 variable=self.scale, command=self.apply_scale).pack(
            fill="x", padx=10)

        tk.Button(self, text="Add Overlay", command=self.add_overlay).pack(
            pady=10
        )
        self.eye_selector = EyeSelector(self, library=eyes)
        self.eye_selector.pack(pady=10)

    def apply_scale(self):
        card = self.parent.card
        if not card or not card.overlays:
            return
        card.overlays[-1].scale = self.scale.get()
        self.parent.preview.preview_card(card)

    def add_overlay(self):
        card = self.parent.card
        overlay_path = filedialog.askopenfilename()

        new_overlay = Overlay(overlay_path, x=50, y=50, scale=1.0)
        card.overlays.append(new_overlay)
        # self.parent.preview.draw_card(card)

        self.controller.update_preview()







    # def update_overlay(self, preview_frame: PreviewFrame):
    #     card = self.parent.card
    #     # edit the Ed model
    #
    #     # scale the overlay
    #
    #     self.parent.preview_frame.preview_card(card)
    #     pass

    #
    #     self.parent.preview_frame.preview_card(card)
    #     pass
