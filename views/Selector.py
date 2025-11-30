import tkinter as tk

from PIL import Image, ImageTk


class Selector(tk.Frame):
    def __init__(self, parent, title, items, on_select, drop_target=None, on_drop=None):
        super().__init__(parent, bg="lightgray", pady=10)
        self.items = list(items.items())
        self.callback = on_select
        self.on_drop = on_drop
        self.drop_target =drop_target
        self.current_index = 0

        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.ghost_window = None

        tk.Label(self, text=title, bg="White", font=("Arial", 10, "bold")).pack(pady=(0, 5))

        row = tk.Frame(self, bg="lightgray")
        row.pack()

        self.btn_prev = tk.Button(row, text="◀", command=self.prev)
        self.btn_prev.pack(side="left", padx=5)

        self.btn_img = tk.Button(row, width=100, height=100, bg="white", relief="flat")
        self.btn_img.pack(side="left", padx=5)

        self.btn_img.bind("<ButtonPress-1>", self.on_start_drag)
        self.btn_img.bind("<B1-Motion>", self.on_drag_motion)
        self.btn_img.bind("<ButtonRelease-1>", self.on_end_drag)

        self.btn_next = tk.Button(row, text="▶", command=self.next)
        self.btn_next.pack(side="left", padx=5)

        self.update_image()

    def on_start_drag(self, event):
        name, path = self.items[self.current_index]
        self.drag_data["item"] = path
        self.drag_data["start_x"] = event.x_root
        self.drag_data["start_y"] = event.y_root
        self.drag_data["is_dragging"] = False

    def on_drag_motion(self, event):
        if abs(event.x_root - self.drag_data["start_x"]) > 5 or \
            abs(event.y_root - self.drag_data["start_y"]) > 5:
            self.drag_data["is_dragging"] = True

        if not self.drag_data["is_dragging"]:
            return

        if not self.ghost_window:
            self.ghost_window = tk.Toplevel(self)
            self.ghost_window.overrideredirect(True)
            self.ghost_window.attributes("-alpha", 0.7)
            self.ghost_window.attributes("-topmost", True)
            img = tk.Label(self.ghost_window, image=self.btn_img.image, bg="white")
            img.pack()

        self.ghost_window.geometry(f"+{event.x_root}+{event.y_root}")

    def on_end_drag(self, event):
        if self.ghost_window:
            self.ghost_window.destroy()
            self.ghost_window = None

        if not self.drag_data["is_dragging"]:
            self.callback(self.drag_data["item"])
            return

        if self.drop_target:
            x = self.drop_target.winfo_rootx()
            y = self.drop_target.winfo_rooty()
            w = self.drop_target.winfo_width()
            h = self.drop_target.winfo_height()

            if (x <= event.x_root <= x + w) and (y <= event.y_root <= y + h):
                final_x = event.x_root - x
                final_y = event.y_root - y

                if self.on_drop:
                    self.on_drop(self.drag_data["item"], final_x, final_y)

    def update_image(self):
        if not self.items:
            return

        name, path = self.items[self.current_index]

        try:
            pil_img = Image.open(path)
            pil_img = pil_img.resize((100, 80))
            tk_img = ImageTk.PhotoImage(pil_img)

            self.btn_img.config(image=tk_img)

            self.btn_img.image = tk_img

        except Exception as e:
            print(f"Error loading the thumbnaill {path}: {e}")

    def next(self):
        self.current_index += 1
        if self.current_index >= len(self.items):
            self.current_index = 0
        self.update_image()

    def prev(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.items) - 1
        self.update_image()

    def on_click(self):
        name, path = self.items[self.current_index]
        self.callback(path)