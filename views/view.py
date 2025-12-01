import tkinter as tk
from PIL import Image, ImageTk
import os
from views import Selector
from overlay_images import *

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.text_entry = None
        self.text_item_id = None
        self.title("EditSheeran")
        self.geometry("1680x1050")

        self.create_layout()

    def create_layout(self):
        self.attributes_frame = tk.Frame(self, bg="white", width=500)
        self.attributes_frame.pack(side="left", fill="y", ipadx=40)
        tk.Label(self.attributes_frame, text="Attributes").pack(pady=10)

        self.preview_frame = tk.Frame(self, bg="lightgray")
        self.preview_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.preview_frame, width=600, height=700, bg="white")
        self.canvas.pack(expand=True)

        self.photobook_frame = tk.Frame(self, bg="white", width=500)
        self.photobook_frame.pack(side="left", fill="y", ipadx=100)
        tk.Label(self.photobook_frame, text="Photobook").pack(pady=10)

        self.setup_attributes()
        self.setup_text_input()

    def setup_attributes(self):
        selected_template = Selector.Selector(self.attributes_frame, "Templates", cards, self.controller.change_template)
        selected_template.pack(pady=3)

        selected_ed = Selector.Selector(self.attributes_frame, "Ed Base", eds, self.controller.add_accessory,
                                        drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_ed.pack(pady=3)

        selected_eyes = Selector.Selector(self.attributes_frame, "Eyes", eyes, self.controller.add_accessory,
                                          drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_eyes.pack(pady=3)

        selected_mouth = Selector.Selector(self.attributes_frame, "Mouth", mouths, self.controller.add_accessory,
                                           drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_mouth.pack(pady=3)

        selected_hat = Selector.Selector(self.attributes_frame, "Hats", accessories, self.controller.add_accessory,
                                         drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_hat.pack(pady=3)

    def update_canvas(self, card_state, selected_index):
        # I'm leaving print statements for debugging
        self.canvas.delete("all")
        self.current_images = []

        base = card_state.get("base")

        if base and os.path.exists(base):
            try:
                pil_img = Image.open(base)
                pil_img = pil_img.resize((600, 700))
                tk_img = ImageTk.PhotoImage(pil_img)
                self.canvas.create_image(0,0, image = tk_img, anchor = "nw", tags="base")
                self.current_images.append(tk_img)
            except Exception as e:
                print(f"Error loading base image: {e}")
        else:
            print(f"Base image not found: {base}")

        overlays = card_state.get("overlays", [])

        for item in overlays:
            try:
                path = item["image"]
                x = item.get("x", 100)
                y = item.get("y", 150)
                w = item.get("width",100)
                h = item.get("height", 100)

                if os.path.exists(path):
                    pil_overlay = Image.open(path)

                    pil_overlay = pil_overlay.resize((w,h))
                    tk_overlay = ImageTk.PhotoImage(pil_overlay)

                    self.canvas.create_image(x,y, image=tk_overlay, anchor="center", tags="draggable")
                    self.current_images.append(tk_overlay)
                else:
                    print(f"Overlay not found: {path}")
            except Exception as e:
                print(f"Error loading overlay {item}: {e}")

    def setup_text_input(self):
        text_frame = tk.LabelFrame(self.attributes_frame, text="Add Custom Text")
        text_frame.pack(pady=15, padx=5, fill="x")

        # 1. Create the Entry Box
        self.text_entry = tk.Entry(text_frame, font=("Arial", 12))
        self.text_entry.insert(0, "Set Custom Greeting")
        self.text_entry.pack(fill="x", padx=10, pady=5)
        self.text_entry.bind("<KeyRelease>", self.update_canvas_text)
        add_btn = tk.Button(text_frame, text="Add Text to Canvas", command=self.add_initial_canvas_text)
        add_btn.pack(pady=5)

    def add_initial_canvas_text(self):
        if self.text_item_id:
            self.canvas.delete(self.text_item_id)
        initial_text = self.text_entry.get()
        self.text_item_id = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            300,
            text=initial_text,
            fill="black",
            font=("Arial", 30, "bold"),
            anchor="n",
            tags="draggable"
        )

    def update_canvas_text(self, event):
        if self.text_item_id:
            current_text = self.text_entry.get()
            self.canvas.itemconfigure(self.text_item_id, text=current_text)
        else:
            self.add_initial_canvas_text()