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

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'assets', 'ed.ico')
        self.iconbitmap(icon_path)

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

    def update_canvas(self, card_state, selected_index=None):
        # I'm leaving print statements for debugging
        self.canvas.delete("all")



        self.current_images = []

        delete_icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "delete_button.png")
        print("Delete icon path:", delete_icon_path)
        self.delete_icon = tk.PhotoImage(file=delete_icon_path)

        self.delete_button = tk.Button(
            self.canvas,
            image=self.delete_icon,
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.controller.del_current_item(self.controller.selected_index)
        )

        # Add it to the canvas, initially invisible
        self.delete_button_id = self.canvas.create_window(
            -1000, -1000,
            window=self.delete_button,
            anchor="center",

        )
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
                        # HANDLE ATTRIBUTE (ITEM) EVENTS
                        self.highlight_selected(item)
                        self.delete_handler(item)
                        self.move_handler(item)
                        self.resize_handler(item)

                else:
                    print(f"Overlay not found: {path}")
            except Exception as e:
                print(f"Error loading overlay {item}: {e}")


    def highlight_selected(self, item):
        x, y = item["x"], item["y"]
        w, h = item["width"], item["height"]

        left = x - (w // 2)
        top = y - (h // 2)
        right = x + (w // 2)
        bottom = y + (h // 2)

        self.canvas.create_rectangle(left, top, right, bottom, outline="blue", dash=(5,5), width=2)




    def resize_handler(self, item):

        x, y = item["x"], item["y"]
        w, h = item["width"], item["height"]

        right = x + (w // 2)
        bottom = y + (h // 2)

        handle_size = 10
        self.handle = self.canvas.create_rectangle(
            right - handle_size, bottom - handle_size,
            right + handle_size, bottom + handle_size,
            fill="blue", outline="white", tags="handle_resize"
        )

        self.canvas.tag_bind("handle_resize", "<ButtonPress-1>", self.on_resize_start)
        self.canvas.tag_bind("handle_resize", "<B1-Motion>", self.on_resize_drag)
        self.canvas.tag_bind("handle_resize", "<ButtonRelease-1>", self.on_resize_end)

    def on_resize_start(self, event):
        self.resize_start_x = event.x
        self.resize_start_y = event.y

        item = self.controller.get_selected_overlay()
        self.initial_size = item["width"]



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

    def move_handler(self, item):

        x, y = item["x"], item["y"]  # item & circ center
        # w, h = item["width"], item["height"]

        # diam = 20
        r = 10

        x1, y1 = x-r, y-r  # top left circ coor
        x2, y2 = x+r, y+r  # bottom right circ coor

        self.move_handle = self.canvas.create_oval(x1,y1,x2,y2,
                                                   fill="white", outline="green",
                                                   tags="handle_move")

        # Draw the horizontal line of the plus sign
        self.hor_handle = self.canvas.create_line(x-6,y , x+6,y,
                                                  fill="black", width=2, tags="hor_handle")
        # Draw the vertical line of the plus sign
        self.vert_handle = self.canvas.create_line(x,y-6 , x,y+6,
                                                   fill="black", width=2, tags="vert_handle")

        self.canvas.tag_bind("handle_move", "<ButtonPress-1>", self.on_move_start)
        self.canvas.tag_bind("handle_move", "<B1-Motion>", self.on_move_drag)
        self.canvas.tag_bind("handle_move", "<ButtonRelease-1>", self.on_move_end)

        self.canvas.tag_bind("hor_handle", "<ButtonPress-1>", self.on_move_start)
        self.canvas.tag_bind("hor_handle", "<B1-Motion>", self.on_move_drag)
        self.canvas.tag_bind("hor_handle", "<ButtonRelease-1>", self.on_move_end)

        self.canvas.tag_bind("vert_handle", "<ButtonPress-1>", self.on_move_start)
        self.canvas.tag_bind("vert_handle", "<B1-Motion>", self.on_move_drag)
        self.canvas.tag_bind("vert_handle", "<ButtonRelease-1>", self.on_move_end)

    def on_move_start(self, event):
        # self.move_start_x = event.x
        # self.move_start_y = event.y

        item = self.controller.get_selected_overlay()
        self.initial_x = item["x"]
        self.initial_y = item["y"]

        self.mouse_dist_x = event.x - self.initial_x
        self.mouse_dist_y = event.y - self.initial_y

        self.temp_rect = self.canvas.create_rectangle(0,0,0,0, outline="green", width=2, dash=(2,2))

    def on_move_drag(self, event):
        item = self.controller.get_selected_overlay()
        # mouse_dist_x = self.move_start_x - self.initial_x
        # mouse_dist_y = self.move_start_y - self.initial_y

        w, h = item["width"], item["height"]

        mouse_x_pos = event.x
        mouse_y_pos = event.y

        self.current_x = mouse_x_pos - self.mouse_dist_x
        self.current_y = mouse_y_pos - self.mouse_dist_y

        left = self.current_x - (w // 2)
        top = self.current_y - (h // 2)
        right = self.current_x + (w // 2)
        bottom = self.current_y + (h // 2)

        x1, y1 = self.current_x-5, self.current_y-5  # top left circ coor
        x2, y2 = self.current_x+5, self.current_y+5  # bottom right circ coor

        self.canvas.coords(self.temp_rect, left, top, right, bottom)
        self.canvas.coords(self.handle, x1,y1,x2,y2)
        # self.controller.move_current_item(self.current_x, self.current_y)

    def on_move_end(self, event):
        self.canvas.delete(self.temp_rect)
        self.controller.move_current_item(self.current_x, self.current_y)

    def delete_handler(self, item):

        if not item:
            self.canvas.coords(self.delete_button_id, -1000, -1000)
            return

        self.canvas.itemconfigure(self.delete_button_id, state="normal")

        x, y = item["x"], item["y"]
        w, h = item["width"], item["height"]

        left = x - (w // 2)
        top = y - (h // 2)

        # Move the button to the top-left corner of the selection box
        bx = left - 20
        by = top - 20

        self.canvas.coords(self.delete_button_id, bx, by)
        self.canvas.lift(self.delete_button_id)

        print("Placing delete button at:", bx, by)


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


