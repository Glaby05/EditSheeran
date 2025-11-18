from views.preview_frame import PreviewFrame


class PhotobookFrame:
    # right screen of the app

    def __init__(self, parent):
        super().__init__(parent, width=250)

        # add some buttons

    def load_card(self, preview_frame: PreviewFrame):
        # load .json file to get the model, redraw model to preview latest version
        card = read_card_json(filename)
        parent.card = card
        parent.preview_frame.preview_card(card)
        pass
