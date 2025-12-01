from views.view import View
from models.model import Card, Photobook

class EditSheeranController:
    def __init__(self):
        self.photobook = Photobook()

        self.current_card = Card()

        self.selected_index = -1

        self.view = View(self)

        self.refresh_preview()

    def select_item(self, index):
        self.selected_index = index
        self.refresh_preview()

    def refresh_preview(self):
        data = self.current_card.get_state()
        self.view.update_canvas(data, self.selected_index)

    def change_template(self, path):
        self.current_card.set_base(path)
        self.refresh_preview()

    def add_accessory(self, path, x=None, y=None):
        if x is None:
            x = 300
        if y is None:
            y=350
        self.current_card.add_overlay(path, x, y)
        self.refresh_preview()

    def get_selected_overlay(self):
        if self.selected_index != -1:
            return self.current_card.overlays[self.selected_index]
        return None

    def resize_current_item(self, new_size):
        if self.selected_index != -1:
            self.current_card.update_overlay_size(self.selected_index, int(new_size))

            self.refresh_preview()

    def move_current_item(self, new_x, new_y):
        if self.selected_index != -1:
            self.current_card.update_overlay_coor(self.selected_index, int(new_x), int(new_y))
            self.refresh_preview()

    def del_current_item(self, i):
        if self.selected_index != -1:
            self.current_card.remove_overlay(i)
            self.refresh_preview()

    def run(self):
        self.view.mainloop()

    def save_card(self):
        self.photobook.add_card(self.current_card)
        self.photobook.save_to_computer()

    def load_card(self, filename):
        print(f"Loading {filename}...")
