import tkinter as tk
from PIL import Image, ImageTk

from views.preview_frame import PreviewFrame


class AttributesFrame(tk. Frame):
    # the left screen of the app
    def __init__(self, parent):
        super().__init__(parent, width=120, height=700, bg="#eeeeee")
        # frame = tk.Frame(self, width=1200, height=700)

        pass

    def update_overlay(self, preview_frame: PreviewFrame):
        # edit the Ed model

        # scale the overlay

        parent.preview_frame.preview_card(parent.card)
        pass
