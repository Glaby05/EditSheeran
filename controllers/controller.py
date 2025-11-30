from views.view import View
from models.model import Card, Photobook

class EditSheeranController:
    def __init__(self):
        self.photobook = Photobook()

        self.current_card = Card()

        self.view = View(self)

        self.refresh_preview()

    def refresh_preview(self):
        data = self.current_card.get_state()
        self.view.update_canvas(data)

    def change_template(self, path):
        self.current_card.set_base(path)
        self.refresh_preview()

    def add_accessory(self, path, x=None, y=None):
        if x is None:
            x = 200
        if y is None:
            y=250
        self.current_card.add_overlay(path, x, y)
        self.refresh_preview()

    def run(self):
        self.view.mainloop()

    def save_card(self):
        self.photobook.add_card(self.current_card)
        self.photobook.save_to_computer()

    def load_card(self, filename):
        print(f"Loading {filename}...")