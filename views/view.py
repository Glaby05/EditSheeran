import tkinter as tk
from PIL import Image, ImageTk
import os
from views import Selector
from overlay_images import *
import json


BASE_DIR = os.path.dirname(__file__)
BASE_DIR1 = os.path.dirname(os.path.abspath(BASE_DIR))
PHOTBOOK_DIR = os.path.join(BASE_DIR1, "photobook")

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("EditSheeran")
        self.geometry("1680x1050")

        self.create_layout()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Card", command=self.controller.new_card)
        # file_menu.add_command(label="Open Base Image", command=self.controller.load_base)
        file_menu.add_command(label="Save to Photobook", command=self.controller.save_card)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

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
        self.create_photobook_area()

        self.setup_attributes()
        self.load_photobook()



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

    def update_canvas(self, card_state):
        # I'm leaving print statements for debugging

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
                x = item.get("x", 200)
                y = item.get("y", 250)
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


    def load_photobook(self):
        for widget in self.pb_inner.winfo_children():
            widget.destroy()

            # Loop through JSON files
        for filename in sorted(os.listdir(PHOTBOOK_DIR), reverse=True):
            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(PHOTBOOK_DIR, filename)

            try:
                with open(json_path, "r") as f:
                    data = json.load(f)

                thumb = self._create_thumbnail(data)
                if thumb is None:
                    continue

                # thumbnail button
                raw_name = data.get("name", None)

                if raw_name:
                    # if someone accidentally saved a path inside `name`, strip directories and extension
                    display_name = os.path.splitext(os.path.basename(raw_name))[0]
                else:
                    # fallback to the json filename (strip .json)
                    display_name = os.path.splitext(filename)[0]
                btn = tk.Button(
                    self.pb_inner,
                    image=thumb,
                    text= display_name,
                    compound="top",
                    command=lambda p=json_path: self.controller.load_card(p),
                    relief="flat"
                )
                btn.pack(side="top", pady=10)

            except:
                pass

    def create_photobook_area(self):
        # main photobook frame
        tk.Label(self.photobook_frame, text="Photobook").pack(pady=10)
        tk.Label(self.photobook_frame, text="Click a saved card to open & edit!").pack(pady=10)

        # canvas + scrollbar
        scroll_container = tk.Frame(self.photobook_frame, width=100, height=800)
        scroll_container.pack()

        #
        self.pb_canvas = tk.Canvas(scroll_container, bg="lavender", width=200, height=750)
        self.pb_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.pb_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.pb_canvas.configure(yscrollcommand=scrollbar.set)

        #inner frame inside the canvas ---
        self.pb_inner = tk.Frame(self.pb_canvas, bg="white")
        self.pb_canvas.create_window((0, 0), window=self.pb_inner, anchor="nw")

        #  scrolling update when widgets are added
        self.pb_inner.bind("<Configure>", lambda e:
        self.pb_canvas.configure(scrollregion=self.pb_canvas.bbox("all"))
                           )


        open_btn = tk.Button(self.photobook_frame, text="Open Photobook", command=self.load_photobook)
        open_btn.pack(pady=10)

        self.photobook_thumbs = []

    def _create_thumbnail(self, card_data):
        base_path = card_data.get("base")

        try:
            base = Image.open(base_path).convert("RGBA")
        except Exception as e:
            print("BAD BASE:", base_path, e)
            return None
        # bad base image

        # Thumbnail base size
        base = base.resize((160, 180))

        # Draw overlays (scaled down)
        for ov in card_data.get("overlays", []):
            try:
                img = Image.open(ov["image"]).convert("RGBA")
                w, h = ov["width"], ov["height"]
                img = img.resize((w // 2, h // 2))  # scale down for thumbnail

                x, y = ov["x"], ov["y"]
                base.paste(img, (x // 2, y // 2), img)

            except Exception as e:
                print("Thumbnail overlay failed:", e)

        tk_thumb = ImageTk.PhotoImage(base)
        self.photobook_thumbs.append(tk_thumb)  # keep alive
        return tk_thumb

