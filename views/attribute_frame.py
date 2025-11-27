import tkinter as tk
from tkinter import Tk, PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
from overlay_images import *
from views.preview_frame import PreviewFrame
from models.model import Card, Overlay, EdSheeran
from controllers.controller import Controller


class Selector(tk.Frame):
    # TO MAKE THE CLASSES CLEANER BY REFACTORING THE CODE
    def update_image(self):
        key = self.keys[self.index]
        tk_img = self.library[key][2]
        self.label.img = tk_img  # keep reference
        self.label.config(image=tk_img)

    def next(self):
        self.index = (self.index + 1) % len(self.keys)
        current_key = self.keys[self.index]
        tk_img = self.library[current_key][2]
        self.label.config(image=tk_img)

    def prev(self):
        self.index = (self.index - 1) % len(self.keys)
        current_key = self.keys[self.index]
        tk_img = self.library[current_key][2]
        self.label.config(image=tk_img)


class EdSelector(Selector):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.keys = list(library.keys())
        self.index = 0
        for k, path in eds.items():
            self.path = path
            self.pil_img = Image.open(path).resize((100, 100))
            self.library[k] = [self.path, self.pil_img, ImageTk.PhotoImage(self.pil_img)]

        self.btn_prev = tk.Button(self, text="◀", command=self.prev)
        self.btn_prev.grid(row=1, column=0, padx=5)

        self.label = tk.Label(self)
        self.label.grid(row=1, column=1, padx=5)
        self.label2 = tk.Label(self, text="Ed")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(self, text="▶", command=self.next)
        self.btn_next.grid(row=1, column=2, padx=5)

        self.update_image()


class EyeSelector(Selector):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.keys = list(library.keys())
        self.index = 0
        for k, path in eyes.items():
            self.path = path
            self.pil_img = Image.open(path).resize((100, 100))
            self.library[k] = [self.path, self.pil_img, ImageTk.PhotoImage(self.pil_img)]

        self.btn_prev = tk.Button(self, text="◀", command=self.prev)
        self.btn_prev.grid(row=1, column=0, padx=5)

        self.label = tk.Label(self)
        self.label.grid(row=1, column=1, padx=5)
        self.label2 = tk.Label(self, text="Eyes")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(self, text="▶", command=self.next)
        self.btn_next.grid(row=1, column=2, padx=5)

        self.update_image()


class MouthSelector(Selector):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.keys = list(library.keys())
        self.index = 0
        for k, path in mouths.items():
            self.path = path
            self.pil_img = Image.open(path).resize((100, 100))
            self.library[k] = [self.path, self.pil_img, ImageTk.PhotoImage(self.pil_img)]

        self.btn_prev = tk.Button(self, text="◀", command=self.prev)
        self.btn_prev.grid(row=1, column=0, padx=5)

        self.label = tk.Label(self)
        self.label.grid(row=1, column=1, padx=5)
        self.label2 = tk.Label(self, text="Mouths")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(self, text="▶", command=self.next)
        self.btn_next.grid(row=1, column=2, padx=5)

        self.update_image()


class AccessoriesSelector(Selector):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.keys = list(library.keys())
        self.index = 0
        for k, path in accessories.items():
            self.path = path
            self.pil_img = Image.open(path).resize((100, 100))
            self.library[k] = [self.path, self.pil_img, ImageTk.PhotoImage(self.pil_img)]

        self.btn_prev = tk.Button(self, text="◀", command=self.prev)
        self.btn_prev.grid(row=1, column=0, padx=5)

        self.label = tk.Label(self)
        self.label.grid(row=1, column=1, padx=5)
        self.label2 = tk.Label(self, text="Accessories")
        self.label2.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(self, text="▶", command=self.next)
        self.btn_next.grid(row=1, column=2, padx=5)

        self.update_image()


class AttributesFrame(tk.Frame):
    # the left screen of the app
    def __init__(self, parent, controller: Controller, card: Card):
        super().__init__(parent, width=120, height=700, bg="white")
        self.parent = parent
        self.controller = controller
        self.card = card
        # frame = tk.Frame(self, width=1200, height=700)

        self.scale = tk.DoubleVar(value=1.0)

        self.ed_selector = EdSelector(self, library=eds)
        self.ed_selector.pack(pady=20)

        tk.Button(self,
                  text="Add Ed",
                  command=lambda: self.add_base_ed(self.ed_selector.index)
                  ).pack(pady=10)

        self.eye_selector = EyeSelector(self, library=eyes)
        self.eye_selector.pack(pady=10)
        self.mouth_selector = MouthSelector(self, library=mouths)
        self.mouth_selector.pack(pady=20)
        self.accessories_selector = AccessoriesSelector(self,
                                                        library=accessories)
        self.accessories_selector.pack(pady=30)

        tk.Button(self, text="Add Overlay", command=self.add_overlay).pack(
            pady=10
        )

    def apply_scale(self):
        card = self.card
        if not card or not card.overlays:
            return
        card.overlays[-1].scale = self.scale.get()
        self.parent.preview.preview_card(card)

    def add_base_ed(self, index):
        card = self.card
        # ed_path = filedialog.askopenfilename()
        key = self.ed_selector.keys[index]
        path = self.ed_selector.library[key][0]
        # tk_img = self.ed_selector.library[key][2]

        card.ed = EdSheeran(path)

        self.controller.update_preview()

    def add_overlay(self):
        card = self.card
        # overlay_path = filedialog.askopenfilename()

        for ov in [self.eye_selector, self.mouth_selector, self.accessories_selector]:
            key = ov.keys[ov.index]
            path = ov.library[key][0]
            new_overlay = Overlay(path, x=50, y=50, scale=self.scale)
            card.overlays.append(new_overlay)
            # self.parent.preview.draw_card(card)

        self.controller.update_preview()
