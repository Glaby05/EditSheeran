import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from views.preview_frame import PreviewFrame
from models.model import Overlay
from controllers.controller import Controller


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
