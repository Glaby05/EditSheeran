import tkinter as tk
from PIL import Image, ImageTk
import os
from views import Selector
from overlay_images import *

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("EditSheeran")
        self.geometry("1680x1050")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'assets', 'ed.ico')
        self.iconbitmap(icon_path)

        self.create_layout()

    def create_layout(self):
        self.attributes_frame = tk.Frame(self, bg="white", width=500)
        self.attributes_frame.pack(side="left", fill="y", ipadx=50)
        tk.Label(self.attributes_frame, text="Attributes").pack(pady=10)

        self.preview_frame = tk.Frame(self, bg="lightgray")
        self.preview_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.preview_frame, width=600, height=700, bg="white")
        self.canvas.pack(expand=True)

        self.photobook_frame = tk.Frame(self, bg="white", width=500)
        self.photobook_frame.pack(side="left", fill="y", ipadx=100)
        tk.Label(self.photobook_frame, text="Photobook").pack(pady=10)

        self.setup_attributes()

    def setup_attributes(self):
        selected_template = Selector.Selector(self.attributes_frame, "Templates", cards, self.controller.change_template)
        selected_template.pack(pady=10)

        selected_ed = Selector.Selector(self.attributes_frame, "Ed Base", eds, self.controller.add_accessory,
                                        drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_ed.pack(pady=10)

        selected_eyes = Selector.Selector(self.attributes_frame, "Eyes", eyes, self.controller.add_accessory,
                                          drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_eyes.pack(pady=10)

        selected_mouth = Selector.Selector(self.attributes_frame, "Mouth", mouths, self.controller.add_accessory,
                                           drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_mouth.pack(pady=10)

        selected_hat = Selector.Selector(self.attributes_frame, "Hats", accessories, self.controller.add_accessory,
                                         drop_target=self.canvas, on_drop=self.controller.add_accessory)
        selected_hat.pack(pady=10)

    def update_canvas(self, card_state, selected_index=None):
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

        for i, item in enumerate(overlays):
            try:
                path = item["image"]
                x = item.get("x", 200)
                y = item.get("y", 250)
                w = item.get("width",250)
                h = item.get("height", 250)

                if os.path.exists(path):
                    pil_overlay = Image.open(path)

                    pil_overlay = pil_overlay.resize((w,h))
                    tk_overlay = ImageTk.PhotoImage(pil_overlay)

                    tags = ("draggable", f"item_{i}")

                    self.canvas.create_image(x,y, image=tk_overlay, anchor="center", tags=tags)
                    self.current_images.append(tk_overlay)

                    self.canvas.tag_bind(f"item_{i}", "<Button-1>", lambda event, idx=i: self.controller.select_item(idx))
                    if i == selected_index:
                        self.resize_box(item)

                else:
                    print(f"Overlay not found: {path}")
            except Exception as e:
                print(f"Error loading overlay {item}: {e}")


    def resize_box(self, item):
        x, y = item["x"], item["y"]
        w, h = item["width"], item["height"]

        left = x - (w // 2)
        top = y - (h // 2)
        right = x + (w // 2)
        bottom = y + (h // 2)

        self.canvas.create_rectangle(left, top, right, bottom, outline="blue", dash=(5,5), width=2, tags="selection")

        handle_size = 10
        self.handle = self.canvas.create_rectangle(
            right - handle_size, bottom - handle_size,
            right + handle_size, bottom + handle_size,
            fill="blue", outline="white", tags="handle"
        )

        self.canvas.tag_bind("handle", "<ButtonPress-1>", self.on_resize_start)
        self.canvas.tag_bind("handle", "<B1-Motion>", self.on_resize_drag)
        self.canvas.tag_bind("handle", "<ButtonRelease-1>", self.on_resize_end)

    def on_resize_start(self, event):
        self.resize_start_x = event.x
        self.resize_start_y = event.y

        item = self.controller.get_selected_overlay()
        self.initial_size = item["width"]

        self.temp_rect = self.canvas.create_rectangle(0,0,0,0, outline="red", width=2, dash=(2,2))

    def on_resize_drag(self, event):
        item = self.controller.get_selected_overlay()
        center_x, center_y = item["x"], item["y"]
        horiz_dist = abs(event.x - center_x)

        new_size = horiz_dist * 2
        if new_size < 20:
            new_size = 20

        self.current_resize_value = new_size

        left = center_x - horiz_dist
        top = center_y - horiz_dist
        right = center_x + horiz_dist
        bottom = center_y + horiz_dist

        self.canvas.coords(self.temp_rect, left, top, right, bottom)

    def on_resize_end(self, event):
        self.canvas.delete(self.temp_rect)
        self.controller.resize_current_item(self.current_resize_value)